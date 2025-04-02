from typing import List, Optional, Dict, Any
from datetime import date, datetime
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import and_, or_
from fastapi import HTTPException, status

from app.core.interfaces.collaboration_repository import CollaborationRepository
from app.core.entities.collaboration import Collaboration, CollaborationCreate, CollaborationUpdate
from app.infrastructure.database.models import Collaboration as CollaborationModel
from app.infrastructure.database.models import Company as CompanyModel
from app.infrastructure.database.models import CollaborationStatus

class SQLAlchemyCollaborationRepository(CollaborationRepository):
    """
    Implémentation SQLAlchemy du repository pour les collaborations
    """
    
    def __init__(self, db: Session):
        self.db = db
    
    async def get_all(self) -> List[Collaboration]:
        """Récupère toutes les collaborations"""
        collaborations = self.db.query(CollaborationModel).all()
        return [self._map_to_entity(collab) for collab in collaborations]
    
    async def get_by_id(self, collaboration_id: int) -> Optional[Collaboration]:
        """Récupère une collaboration par son ID"""
        collaboration = self.db.query(CollaborationModel).filter(CollaborationModel.id == collaboration_id).first()
        if not collaboration:
            return None
        return self._map_to_entity(collaboration)
    
    async def get_by_initiator_company_id(self, company_id: int) -> List[Collaboration]:
        """Récupère toutes les collaborations où l'entreprise est initiatrice"""
        # Note: Adaptation nécessaire en fonction de la structure réelle du modèle
        # Exemple d'adaptation pour correspondre à l'interface tout en utilisant le modèle actuel:
        collaborations = self.db.query(CollaborationModel)\
            .join(CompanyModel, CollaborationModel.consultant.has(company_id=company_id))\
            .all()
        return [self._map_to_entity(collab) for collab in collaborations]
    
    async def get_by_partner_company_id(self, company_id: int) -> List[Collaboration]:
        """Récupère toutes les collaborations où l'entreprise est partenaire"""
        # Note: Adaptation nécessaire en fonction de la structure réelle du modèle
        collaborations = self.db.query(CollaborationModel)\
            .join(CompanyModel, CollaborationModel.tender.has(company_id=company_id))\
            .all()
        return [self._map_to_entity(collab) for collab in collaborations]
    
    async def get_by_company_id(self, company_id: int) -> List[Collaboration]:
        """Récupère toutes les collaborations où l'entreprise est soit initiatrice soit partenaire"""
        # Combinaison des deux méthodes précédentes
        collaborations_query = self.db.query(CollaborationModel)\
            .join(CollaborationModel.consultant)\
            .join(CollaborationModel.tender)\
            .filter(
                or_(
                    CollaborationModel.consultant.has(company_id=company_id),
                    CollaborationModel.tender.has(company_id=company_id)
                )
            )
        collaborations = collaborations_query.all()
        return [self._map_to_entity(collab) for collab in collaborations]
    
    async def create(self, collaboration: CollaborationCreate) -> Collaboration:
        """Crée une nouvelle collaboration"""
        try:
            # Adaptation pour convertir l'entité vers le modèle de BDD
            # Supposons que initiator_company correspond à la société du consultant
            # et partner_company à celle qui a publié l'appel d'offres
            # Note: Cette logique devrait être adaptée à votre cas d'usage spécifique
            
            # Pour l'instant, nous utilisons une approche simplifiée
            # en supposant que nous avons un match_id par défaut
            match_id = 1  # À remplacer par une logique appropriée
            
            # Conversion du statut
            db_status = CollaborationStatus.DRAFT
            if collaboration.status == "pending":
                db_status = CollaborationStatus.DRAFT
            elif collaboration.status == "active":
                db_status = CollaborationStatus.ACTIVE
            elif collaboration.status == "inactive":
                db_status = CollaborationStatus.COMPLETED
            
            db_collaboration = CollaborationModel(
                match_id=match_id,  # À remplacer par une vraie logique
                consultant_id=collaboration.initiator_company_id,  # Adaptation simplifiée
                tender_id=collaboration.partner_company_id,  # Adaptation simplifiée
                start_date=collaboration.start_date,
                end_date=collaboration.end_date,
                status=db_status,
                notes=collaboration.terms
            )
            
            self.db.add(db_collaboration)
            self.db.commit()
            self.db.refresh(db_collaboration)
            
            return self._map_to_entity(db_collaboration)
        except IntegrityError as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Erreur lors de la création de la collaboration: {str(e)}"
            )
    
    async def update(self, collaboration_id: int, collaboration: CollaborationUpdate) -> Optional[Collaboration]:
        """Met à jour une collaboration existante"""
        db_collaboration = self.db.query(CollaborationModel).filter(CollaborationModel.id == collaboration_id).first()
        if not db_collaboration:
            return None
        
        # Mise à jour des champs
        if collaboration.status is not None:
            # Conversion du statut
            if collaboration.status == "pending":
                db_collaboration.status = CollaborationStatus.DRAFT
            elif collaboration.status == "active":
                db_collaboration.status = CollaborationStatus.ACTIVE
            elif collaboration.status == "inactive":
                db_collaboration.status = CollaborationStatus.COMPLETED
        
        if collaboration.start_date is not None:
            db_collaboration.start_date = collaboration.start_date
        
        if collaboration.end_date is not None:
            db_collaboration.end_date = collaboration.end_date
        
        if collaboration.terms is not None:
            db_collaboration.notes = collaboration.terms
        
        try:
            self.db.commit()
            self.db.refresh(db_collaboration)
            return self._map_to_entity(db_collaboration)
        except IntegrityError as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Erreur lors de la mise à jour de la collaboration: {str(e)}"
            )
    
    async def delete(self, collaboration_id: int) -> bool:
        """Supprime une collaboration"""
        db_collaboration = self.db.query(CollaborationModel).filter(CollaborationModel.id == collaboration_id).first()
        if not db_collaboration:
            return False
        
        self.db.delete(db_collaboration)
        self.db.commit()
        return True
    
    async def get_by_status(self, status: str) -> List[Collaboration]:
        """Récupère les collaborations par statut"""
        # Conversion du statut
        db_status = None
        if status == "pending":
            db_status = CollaborationStatus.DRAFT
        elif status == "active":
            db_status = CollaborationStatus.ACTIVE
        elif status == "inactive":
            db_status = CollaborationStatus.COMPLETED
        
        if db_status is None:
            return []
        
        collaborations = self.db.query(CollaborationModel).filter(CollaborationModel.status == db_status).all()
        return [self._map_to_entity(collab) for collab in collaborations]
    
    async def get_active_collaborations(self, date_reference: Optional[date] = None) -> List[Collaboration]:
        """Récupère les collaborations actives à une date donnée (par défaut aujourd'hui)"""
        if date_reference is None:
            date_reference = datetime.now().date()
        
        collaborations = self.db.query(CollaborationModel).filter(
            and_(
                CollaborationModel.status == CollaborationStatus.ACTIVE,
                or_(
                    CollaborationModel.end_date.is_(None),
                    CollaborationModel.end_date >= date_reference
                ),
                or_(
                    CollaborationModel.start_date.is_(None),
                    CollaborationModel.start_date <= date_reference
                )
            )
        ).all()
        
        return [self._map_to_entity(collab) for collab in collaborations]
    
    def _map_to_entity(self, db_collaboration: CollaborationModel) -> Collaboration:
        """Convertit un modèle SQLAlchemy en entité"""
        # Récupération des informations des entreprises
        initiator_company = None
        partner_company = None
        
        if db_collaboration.consultant and db_collaboration.consultant.company:
            initiator_company = {
                "id": db_collaboration.consultant.company.id,
                "name": db_collaboration.consultant.company.name,
                "logo_url": db_collaboration.consultant.company.logo_url
            }
        
        if db_collaboration.tender and db_collaboration.tender.company:
            partner_company = {
                "id": db_collaboration.tender.company.id,
                "name": db_collaboration.tender.company.name,
                "logo_url": db_collaboration.tender.company.logo_url
            }
        
        # Conversion du statut
        entity_status = "pending"
        if db_collaboration.status == CollaborationStatus.ACTIVE:
            entity_status = "active"
        elif db_collaboration.status == CollaborationStatus.COMPLETED:
            entity_status = "inactive"
        
        return Collaboration(
            id=db_collaboration.id,
            initiator_company_id=db_collaboration.consultant_id,
            partner_company_id=db_collaboration.tender_id,
            status=entity_status,
            start_date=db_collaboration.start_date,
            end_date=db_collaboration.end_date,
            terms=db_collaboration.notes,
            initiator_company=initiator_company or {},
            partner_company=partner_company or {},
            created_at=db_collaboration.created_at,
            updated_at=db_collaboration.updated_at
        )
