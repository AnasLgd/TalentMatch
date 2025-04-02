from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

from app.core.interfaces.tender_repository import TenderRepository
from app.core.entities.tender import Tender, TenderCreate, TenderUpdate
from app.infrastructure.database.models import Tender as TenderModel
from app.infrastructure.database.models import TenderSkill as TenderSkillModel
from app.infrastructure.database.models import Skill as SkillModel

class SQLAlchemyTenderRepository(TenderRepository):
    """
    Implémentation SQLAlchemy du repository pour les appels d'offres
    """
    
    def __init__(self, db: Session):
        self.db = db
    
    async def get_all(self) -> List[Tender]:
        """Récupère tous les appels d'offres"""
        tenders = self.db.query(TenderModel).all()
        return [self._map_to_entity(tender) for tender in tenders]
    
    async def get_by_id(self, tender_id: int) -> Optional[Tender]:
        """Récupère un appel d'offres par son ID"""
        tender = self.db.query(TenderModel).filter(TenderModel.id == tender_id).first()
        if not tender:
            return None
        return self._map_to_entity(tender)
    
    async def get_by_company_id(self, company_id: int) -> List[Tender]:
        """Récupère tous les appels d'offres d'une entreprise"""
        tenders = self.db.query(TenderModel).filter(TenderModel.company_id == company_id).all()
        return [self._map_to_entity(tender) for tender in tenders]
    
    async def create(self, tender: TenderCreate) -> Tender:
        """Crée un nouvel appel d'offres"""
        try:
            db_tender = TenderModel(
                company_id=tender.company_id,
                title=tender.title,
                client_name=tender.client_name,
                description=tender.description,
                start_date=tender.start_date,
                end_date=tender.end_date,
                status=tender.status,
                location=tender.location,
                remote_work=tender.remote_work,
                budget=tender.budget,
                required_consultants=tender.required_consultants
            )
            
            self.db.add(db_tender)
            self.db.commit()
            self.db.refresh(db_tender)
            
            return self._map_to_entity(db_tender)
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Erreur lors de la création de l'appel d'offres"
            )
    
    async def update(self, tender_id: int, tender: TenderUpdate) -> Optional[Tender]:
        """Met à jour un appel d'offres existant"""
        db_tender = self.db.query(TenderModel).filter(TenderModel.id == tender_id).first()
        if not db_tender:
            return None
        
        # Mettre à jour les champs
        update_data = tender.dict(exclude_unset=True)
        
        for key, value in update_data.items():
            setattr(db_tender, key, value)
        
        try:
            self.db.commit()
            self.db.refresh(db_tender)
            return self._map_to_entity(db_tender)
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Erreur lors de la mise à jour de l'appel d'offres"
            )
    
    async def delete(self, tender_id: int) -> bool:
        """Supprime un appel d'offres"""
        db_tender = self.db.query(TenderModel).filter(TenderModel.id == tender_id).first()
        if not db_tender:
            return False
        
        self.db.delete(db_tender)
        self.db.commit()
        return True
    
    async def get_skills(self, tender_id: int) -> List[Dict[str, Any]]:
        """Récupère les compétences requises pour un appel d'offres"""
        skills = self.db.query(
            TenderSkillModel, SkillModel
        ).join(
            SkillModel, TenderSkillModel.skill_id == SkillModel.id
        ).filter(
            TenderSkillModel.tender_id == tender_id
        ).all()
        
        result = []
        for tender_skill, skill in skills:
            result.append({
                "id": skill.id,
                "name": skill.name,
                "category": skill.category,  # Catégorie sous forme de chaîne (pas d'enum.value)
                "description": skill.description,
                "importance": tender_skill.importance,
                "details": tender_skill.details
            })
        
        return result
    
    async def add_skill(self, tender_id: int, skill_id: int, importance: str, 
                       details: Optional[str] = None) -> bool:
        """Ajoute une compétence requise à un appel d'offres"""
        try:
            # Vérifier que l'appel d'offres existe
            tender = self.db.query(TenderModel).filter(TenderModel.id == tender_id).first()
            if not tender:
                return False
            
            # Vérifier que la compétence existe
            skill = self.db.query(SkillModel).filter(SkillModel.id == skill_id).first()
            if not skill:
                return False
            
            # Vérifier si la compétence est déjà associée à l'appel d'offres
            existing = self.db.query(TenderSkillModel).filter(
                TenderSkillModel.tender_id == tender_id,
                TenderSkillModel.skill_id == skill_id
            ).first()
            
            if existing:
                # Mettre à jour la compétence existante
                existing.importance = importance
                existing.details = details
            else:
                # Créer une nouvelle association
                db_tender_skill = TenderSkillModel(
                    tender_id=tender_id,
                    skill_id=skill_id,
                    importance=importance,
                    details=details
                )
                self.db.add(db_tender_skill)
            
            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            print(f"Erreur lors de l'ajout de compétence: {str(e)}")
            return False
    
    async def update_skill(self, tender_id: int, skill_id: int, importance: str, 
                          details: Optional[str] = None) -> bool:
        """Met à jour une compétence requise pour un appel d'offres"""
        tender_skill = self.db.query(TenderSkillModel).filter(
            TenderSkillModel.tender_id == tender_id,
            TenderSkillModel.skill_id == skill_id
        ).first()
        
        if not tender_skill:
            return False
        
        tender_skill.importance = importance
        tender_skill.details = details
        
        try:
            self.db.commit()
            return True
        except Exception:
            self.db.rollback()
            return False
    
    async def remove_skill(self, tender_id: int, skill_id: int) -> bool:
        """Supprime une compétence requise d'un appel d'offres"""
        tender_skill = self.db.query(TenderSkillModel).filter(
            TenderSkillModel.tender_id == tender_id,
            TenderSkillModel.skill_id == skill_id
        ).first()
        
        if not tender_skill:
            return False
        
        self.db.delete(tender_skill)
        self.db.commit()
        return True
    
    async def get_active_tenders(self) -> List[Tender]:
        """Récupère les appels d'offres actifs"""
        tenders = self.db.query(TenderModel).filter(TenderModel.status == "open").all()
        return [self._map_to_entity(tender) for tender in tenders]
    
    async def search_tenders(self, query: str, skills: Optional[List[int]] = None, 
                            company_id: Optional[int] = None, status: Optional[str] = None) -> List[Tender]:
        """Recherche des appels d'offres par critères"""
        search = f"%{query}%"
        
        # Requête de base
        tenders_query = self.db.query(TenderModel).filter(
            (TenderModel.title.ilike(search)) |
            (TenderModel.description.ilike(search)) |
            (TenderModel.client_name.ilike(search))
        )
        
        # Filtrer par entreprise
        if company_id:
            tenders_query = tenders_query.filter(TenderModel.company_id == company_id)
        
        # Filtrer par statut
        if status:
            tenders_query = tenders_query.filter(TenderModel.status == status)
        
        # Filtrer par compétences
        if skills and len(skills) > 0:
            for skill_id in skills:
                tenders_query = tenders_query.join(
                    TenderSkillModel, 
                    TenderModel.id == TenderSkillModel.tender_id
                ).filter(
                    TenderSkillModel.skill_id == skill_id
                )
        
        tenders = tenders_query.all()
        return [self._map_to_entity(tender) for tender in tenders]
    
    def _map_to_entity(self, db_tender: TenderModel) -> Tender:
        """Convertit un modèle SQLAlchemy en entité"""
        return Tender(
            id=db_tender.id,
            company_id=db_tender.company_id,
            title=db_tender.title,
            client_name=db_tender.client_name,
            description=db_tender.description,
            start_date=db_tender.start_date,
            end_date=db_tender.end_date,
            status=db_tender.status.value,
            location=db_tender.location,
            remote_work=db_tender.remote_work,
            budget=db_tender.budget,
            required_consultants=db_tender.required_consultants,
            created_at=db_tender.created_at,
            updated_at=db_tender.updated_at
        )
