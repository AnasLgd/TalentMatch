from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

from app.core.interfaces.consultant_repository import ConsultantRepository
from app.core.entities.consultant import Consultant, ConsultantCreate, ConsultantUpdate, AvailabilityStatus
from app.infrastructure.database.models import Consultant as ConsultantModel
from app.infrastructure.database.models import ConsultantSkill as ConsultantSkillModel
from app.infrastructure.database.models import User as UserModel
from app.infrastructure.database.models import Skill as SkillModel

class SQLAlchemyConsultantRepository(ConsultantRepository):
    """
    Implémentation SQLAlchemy du repository pour les consultants
    """
    
    def __init__(self, db: Session):
        self.db = db
    
    async def get_all(self) -> List[Consultant]:
        """Récupère tous les consultants"""
        consultants = self.db.query(ConsultantModel).all()
        return [await self._map_to_entity(consultant) for consultant in consultants]
    
    async def get_by_id(self, consultant_id: int) -> Optional[Consultant]:
        """Récupère un consultant par son ID"""
        consultant = self.db.query(ConsultantModel).filter(ConsultantModel.id == consultant_id).first()
        if not consultant:
            return None
        return await self._map_to_entity(consultant)
    
    async def get_by_user_id(self, user_id: int) -> Optional[Consultant]:
        """Récupère un consultant par l'ID de son utilisateur"""
        consultant = self.db.query(ConsultantModel).filter(ConsultantModel.user_id == user_id).first()
        if not consultant:
            return None
        return await self._map_to_entity(consultant)
    
    async def get_by_company_id(self, company_id: int) -> List[Consultant]:
        """Récupère tous les consultants d'une entreprise"""
        consultants = self.db.query(ConsultantModel).filter(ConsultantModel.company_id == company_id).all()
        return [await self._map_to_entity(consultant) for consultant in consultants]
    
    async def create(self, consultant: ConsultantCreate) -> Consultant:
        """Crée un nouveau consultant"""
        try:
            # Vérifier que l'utilisateur existe seulement si un user_id est fourni
            if consultant.user_id is not None:
                user = self.db.query(UserModel).filter(UserModel.id == consultant.user_id).first()
                if not user:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="L'utilisateur n'existe pas"
                    )
            
            # Créer le consultant
            db_consultant = ConsultantModel(
                user_id=consultant.user_id,
                company_id=consultant.company_id,
                title=consultant.title,
                years_experience=consultant.experience_years,
                status=consultant.availability_status,
                availability_date=consultant.availability_date,
                hourly_rate=consultant.hourly_rate,
                daily_rate=consultant.daily_rate,
                bio=consultant.bio,
                photo_url=consultant.photo_url,
                # Ajout des champs pour le nom et prénom
                first_name=consultant.first_name,
                last_name=consultant.last_name,
                # Les champs suivants ne sont pas dans le modèle de base de données
                # location=consultant.location,
                # remote_work=consultant.remote_work,
                # max_travel_distance=consultant.max_travel_distance
            )
            
            self.db.add(db_consultant)
            self.db.commit()
            self.db.refresh(db_consultant)
            
            return await self._map_to_entity(db_consultant)
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Erreur lors de la création du consultant"
            )
    
    async def update(self, consultant_id: int, consultant: ConsultantUpdate) -> Optional[Consultant]:
        """Met à jour un consultant existant"""
        db_consultant = self.db.query(ConsultantModel).filter(ConsultantModel.id == consultant_id).first()
        if not db_consultant:
            return None
        
        # Mettre à jour les champs
        update_data = consultant.dict(exclude_unset=True)
        
        for key, value in update_data.items():
            setattr(db_consultant, key, value)
        
        try:
            self.db.commit()
            self.db.refresh(db_consultant)
            return await self._map_to_entity(db_consultant)
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Erreur lors de la mise à jour du consultant"
            )
    
    async def delete(self, consultant_id: int) -> bool:
        """Supprime un consultant"""
        db_consultant = self.db.query(ConsultantModel).filter(ConsultantModel.id == consultant_id).first()
        if not db_consultant:
            return False
        
        self.db.delete(db_consultant)
        self.db.commit()
        return True
    
    async def get_skills(self, consultant_id: int) -> List[Dict[str, Any]]:
        """Récupère les compétences d'un consultant"""
        skills = self.db.query(
            ConsultantSkillModel, SkillModel
        ).join(
            SkillModel, ConsultantSkillModel.skill_id == SkillModel.id
        ).filter(
            ConsultantSkillModel.consultant_id == consultant_id
        ).all()
        
        result = []
        for consultant_skill, skill in skills:
            result.append({
                "id": skill.id,
                "name": skill.name,
                "category": skill.category.value,
                "description": skill.description,
                "proficiency_level": consultant_skill.proficiency_level.value,
                "years_experience": consultant_skill.years_experience,
                "details": consultant_skill.details
            })
        
        return result
    
    async def add_skill(self, consultant_id: int, skill_id: int, proficiency_level: str, 
                       years_experience: Optional[int] = None, details: Optional[str] = None) -> bool:
        """Ajoute une compétence à un consultant"""
        try:
            # Vérifier que le consultant existe
            consultant = self.db.query(ConsultantModel).filter(ConsultantModel.id == consultant_id).first()
            if not consultant:
                return False
            
            # Vérifier que la compétence existe
            skill = self.db.query(SkillModel).filter(SkillModel.id == skill_id).first()
            if not skill:
                return False
            
            # Vérifier si la compétence est déjà associée au consultant
            existing = self.db.query(ConsultantSkillModel).filter(
                ConsultantSkillModel.consultant_id == consultant_id,
                ConsultantSkillModel.skill_id == skill_id
            ).first()
            
            if existing:
                # Mettre à jour la compétence existante
                existing.proficiency_level = proficiency_level
                existing.years_experience = years_experience
                existing.details = details
            else:
                # Créer une nouvelle association
                db_consultant_skill = ConsultantSkillModel(
                    consultant_id=consultant_id,
                    skill_id=skill_id,
                    proficiency_level=proficiency_level,
                    years_experience=years_experience,
                    details=details
                )
                self.db.add(db_consultant_skill)
            
            self.db.commit()
            return True
        except Exception:
            self.db.rollback()
            return False
    
    async def remove_skill(self, consultant_id: int, skill_id: int) -> bool:
        """Supprime une compétence d'un consultant"""
        consultant_skill = self.db.query(ConsultantSkillModel).filter(
            ConsultantSkillModel.consultant_id == consultant_id,
            ConsultantSkillModel.skill_id == skill_id
        ).first()
        
        if not consultant_skill:
            return False
        
        self.db.delete(consultant_skill)
        self.db.commit()
        return True
    
    async def get_available_consultants(self) -> List[Consultant]:
        """Récupère les consultants disponibles"""
        consultants = self.db.query(ConsultantModel).filter(
            ConsultantModel.status == "AVAILABLE"
        ).all()
        return [await self._map_to_entity(consultant) for consultant in consultants]
    
    async def search_consultants(self, query: str, skills: Optional[List[int]] = None, 
                               company_id: Optional[int] = None, 
                               availability_status: Optional[str] = None) -> List[Consultant]:
        """Recherche des consultants par critères"""
        search = f"%{query}%"
        
        # Requête de base
        consultants_query = self.db.query(ConsultantModel).join(
            UserModel, ConsultantModel.user_id == UserModel.id
        ).filter(
            (UserModel.full_name.ilike(search)) |
            (ConsultantModel.title.ilike(search)) |
            (ConsultantModel.bio.ilike(search))
        )
        
        # Filtrer par entreprise
        if company_id:
            consultants_query = consultants_query.filter(ConsultantModel.company_id == company_id)
        
        # Filtrer par statut de disponibilité
        if availability_status:
            consultants_query = consultants_query.filter(ConsultantModel.status == availability_status)
        
        # Filtrer par compétences
        if skills and len(skills) > 0:
            for skill_id in skills:
                consultants_query = consultants_query.join(
                    ConsultantSkillModel, 
                    ConsultantModel.id == ConsultantSkillModel.consultant_id
                ).filter(
                    ConsultantSkillModel.skill_id == skill_id
                )
        
        consultants = consultants_query.all()
        return [await self._map_to_entity(consultant) for consultant in consultants]
    
    async def _map_to_entity(self, db_consultant: ConsultantModel) -> Consultant:
        """Convertit un modèle SQLAlchemy en entité"""
        # Récupérer les informations de l'utilisateur
        user = self.db.query(UserModel).filter(UserModel.id == db_consultant.user_id).first()
        
        user_data = {
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "role": user.role.value
        } if user else {}
        
        # Récupération des compétences du consultant de manière simplifiée
        # Nous allons récupérer les compétences directement depuis la relation skills
        skills_data = []
        if hasattr(db_consultant, 'skills') and db_consultant.skills:
            for skill in db_consultant.skills:
                skill_data = {
                    "id": skill.id,
                    "name": skill.name,
                    "level": "intermediate",  # Valeur par défaut
                    "years": 0  # Valeur par défaut
                }
                skills_data.append(skill_data)
        
        # Conversion de l'enum status vers availability_status
        availability_status = AvailabilityStatus.AVAILABLE
        if db_consultant.status:
            status_value = db_consultant.status.value
            # Mapping entre les valeurs d'enum
            if status_value == "AVAILABLE":
                availability_status = AvailabilityStatus.AVAILABLE
            elif status_value == "ON_MISSION":
                availability_status = AvailabilityStatus.ON_MISSION
            elif status_value == "UNAVAILABLE":
                availability_status = AvailabilityStatus.UNAVAILABLE

        # Créons l'entité consultant avec les champs qui existent vraiment
        # Priorité aux champs first_name et last_name du modèle consultant, sinon ceux de l'utilisateur
        first_name = db_consultant.first_name
        last_name = db_consultant.last_name
        
        # Si le consultant n'a pas de nom/prénom mais a un utilisateur associé,
        # on récupère depuis l'utilisateur (rétrocompatibilité)
        if user and (not first_name or not last_name):
            if not first_name and hasattr(user, 'first_name'):
                first_name = user.first_name
            if not last_name and hasattr(user, 'last_name'):
                last_name = user.last_name
        
        return Consultant(
            id=db_consultant.id,
            user_id=db_consultant.user_id,
            company_id=db_consultant.company_id,
            title=db_consultant.title,
            experience_years=db_consultant.years_experience,  # Mapping du champ years_experience -> experience_years
            availability_status=availability_status,  # Statut déjà converti ci-dessus
            availability_date=db_consultant.availability_date,
            hourly_rate=db_consultant.hourly_rate,
            daily_rate=db_consultant.daily_rate,
            bio=db_consultant.bio,
            # Ajout des champs first_name et last_name
            first_name=first_name,
            last_name=last_name,
            # Les champs suivants ne sont pas dans le modèle, on utilise des valeurs par défaut
            location=None,
            remote_work=False,
            max_travel_distance=None,
            photo_url=db_consultant.photo_url,
            created_at=db_consultant.created_at,
            updated_at=db_consultant.updated_at if hasattr(db_consultant, 'updated_at') else None,
            user=user_data,
            skills=skills_data
        )
