from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

from app.core.interfaces.match_repository import MatchRepository
from app.core.entities.match import Match, MatchCreate, MatchUpdate
from app.infrastructure.database.models import Match as MatchModel
from app.infrastructure.database.models import Consultant as ConsultantModel
from app.infrastructure.database.models import Tender as TenderModel

class SQLAlchemyMatchRepository(MatchRepository):
    """
    Implémentation SQLAlchemy du repository pour les matchs entre consultants et appels d'offres
    """
    
    def __init__(self, db: Session):
        self.db = db
    
    async def get_all(self) -> List[Match]:
        """Récupère tous les matchs"""
        matches = self.db.query(MatchModel).all()
        return [self._map_to_entity(match) for match in matches]
    
    async def get_by_id(self, match_id: int) -> Optional[Match]:
        """Récupère un match par son ID"""
        match = self.db.query(MatchModel).filter(MatchModel.id == match_id).first()
        if not match:
            return None
        return self._map_to_entity(match)
    
    async def get_by_consultant_id(self, consultant_id: int) -> List[Match]:
        """Récupère tous les matchs d'un consultant"""
        matches = self.db.query(MatchModel).filter(MatchModel.consultant_id == consultant_id).all()
        return [self._map_to_entity(match) for match in matches]
    
    async def get_by_tender_id(self, tender_id: int) -> List[Match]:
        """Récupère tous les matchs d'un appel d'offres"""
        matches = self.db.query(MatchModel).filter(MatchModel.tender_id == tender_id).all()
        return [self._map_to_entity(match) for match in matches]
    
    async def create(self, match: MatchCreate) -> Match:
        """Crée un nouveau match"""
        try:
            # Vérifier que le consultant existe
            consultant = self.db.query(ConsultantModel).filter(ConsultantModel.id == match.consultant_id).first()
            if not consultant:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Le consultant n'existe pas"
                )
            
            # Vérifier que l'appel d'offres existe
            tender = self.db.query(TenderModel).filter(TenderModel.id == match.tender_id).first()
            if not tender:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="L'appel d'offres n'existe pas"
                )
            
            # Vérifier qu'un match n'existe pas déjà
            existing_match = self.db.query(MatchModel).filter(
                MatchModel.consultant_id == match.consultant_id,
                MatchModel.tender_id == match.tender_id
            ).first()
            
            if existing_match:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Un match existe déjà entre ce consultant et cet appel d'offres"
                )
            
            db_match = MatchModel(
                consultant_id=match.consultant_id,
                tender_id=match.tender_id,
                match_score=match.match_score,
                status=match.status,
                notes=match.notes
            )
            
            self.db.add(db_match)
            self.db.commit()
            self.db.refresh(db_match)
            
            return self._map_to_entity(db_match)
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Erreur lors de la création du match"
            )
    
    async def update(self, match_id: int, match: MatchUpdate) -> Optional[Match]:
        """Met à jour un match existant"""
        db_match = self.db.query(MatchModel).filter(MatchModel.id == match_id).first()
        if not db_match:
            return None
        
        # Mettre à jour les champs
        update_data = match.dict(exclude_unset=True)
        
        for key, value in update_data.items():
            setattr(db_match, key, value)
        
        try:
            self.db.commit()
            self.db.refresh(db_match)
            return self._map_to_entity(db_match)
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Erreur lors de la mise à jour du match"
            )
    
    async def delete(self, match_id: int) -> bool:
        """Supprime un match"""
        db_match = self.db.query(MatchModel).filter(MatchModel.id == match_id).first()
        if not db_match:
            return False
        
        self.db.delete(db_match)
        self.db.commit()
        return True
    
    async def get_by_status(self, status: str) -> List[Match]:
        """Récupère les matchs par statut"""
        matches = self.db.query(MatchModel).filter(MatchModel.status == status).all()
        return [self._map_to_entity(match) for match in matches]
    
    async def get_by_company_id(self, company_id: int) -> List[Match]:
        """Récupère les matchs pour une entreprise (via les consultants ou les appels d'offres)"""
        # Récupérer les matchs via les consultants de l'entreprise
        consultant_matches = self.db.query(MatchModel).join(
            ConsultantModel, MatchModel.consultant_id == ConsultantModel.id
        ).filter(
            ConsultantModel.company_id == company_id
        ).all()
        
        # Récupérer les matchs via les appels d'offres de l'entreprise
        tender_matches = self.db.query(MatchModel).join(
            TenderModel, MatchModel.tender_id == TenderModel.id
        ).filter(
            TenderModel.company_id == company_id
        ).all()
        
        # Combiner les résultats et éliminer les doublons
        all_matches = {match.id: match for match in consultant_matches + tender_matches}
        
        return [self._map_to_entity(match) for match in all_matches.values()]
    
    def _map_to_entity(self, db_match: MatchModel) -> Match:
        """Convertit un modèle SQLAlchemy en entité"""
        return Match(
            id=db_match.id,
            consultant_id=db_match.consultant_id,
            tender_id=db_match.tender_id,
            match_score=db_match.match_score,
            status=db_match.status.value,
            notes=db_match.notes,
            created_at=db_match.created_at,
            updated_at=db_match.updated_at
        )
