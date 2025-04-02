from typing import List, Optional, Dict, Any
from fastapi import Depends

from app.core.entities.match import Match, MatchCreate, MatchUpdate
from app.core.interfaces.match_repository import MatchRepository
from app.core.interfaces.consultant_repository import ConsultantRepository
from app.core.interfaces.tender_repository import TenderRepository
from app.core.interfaces.matchmaking_service import MatchmakingService

class MatchUseCase:
    """
    Cas d'utilisation pour la gestion des matchs entre consultants et appels d'offres
    Partie de la fonctionnalité de collaboration inter-ESN (priorité maximale)
    """
    
    def __init__(
        self,
        match_repository: MatchRepository,
        consultant_repository: ConsultantRepository,
        tender_repository: TenderRepository,
        matchmaking_service: MatchmakingService
    ):
        self.match_repository = match_repository
        self.consultant_repository = consultant_repository
        self.tender_repository = tender_repository
        self.matchmaking_service = matchmaking_service
    
    async def get_all_matches(self) -> List[Match]:
        """Récupère tous les matchs"""
        return await self.match_repository.get_all()
    
    async def get_match_by_id(self, match_id: int) -> Optional[Match]:
        """Récupère un match par son ID"""
        return await self.match_repository.get_by_id(match_id)
    
    async def get_matches_by_consultant(self, consultant_id: int) -> List[Match]:
        """Récupère tous les matchs d'un consultant"""
        return await self.match_repository.get_by_consultant_id(consultant_id)
    
    async def get_matches_by_tender(self, tender_id: int) -> List[Match]:
        """Récupère tous les matchs d'un appel d'offres"""
        return await self.match_repository.get_by_tender_id(tender_id)
    
    async def create_match(self, match_data: MatchCreate) -> Match:
        """Crée un nouveau match"""
        # Vérifier que le consultant existe
        consultant = await self.consultant_repository.get_by_id(match_data.consultant_id)
        if not consultant:
            raise ValueError("Le consultant n'existe pas")
        
        # Vérifier que l'appel d'offres existe
        tender = await self.tender_repository.get_by_id(match_data.tender_id)
        if not tender:
            raise ValueError("L'appel d'offres n'existe pas")
        
        # Vérifier qu'un match n'existe pas déjà
        existing_matches = await self.match_repository.get_by_consultant_id(match_data.consultant_id)
        for match in existing_matches:
            if match.tender_id == match_data.tender_id:
                raise ValueError("Un match existe déjà entre ce consultant et cet appel d'offres")
        
        # Si le score de match n'est pas fourni, le calculer
        if not match_data.match_score or match_data.match_score <= 0:
            match_data.match_score = await self.matchmaking_service.calculate_match_score(
                match_data.consultant_id, match_data.tender_id
            )
        
        return await self.match_repository.create(match_data)
    
    async def update_match(self, match_id: int, match_data: MatchUpdate) -> Optional[Match]:
        """Met à jour un match existant"""
        existing_match = await self.match_repository.get_by_id(match_id)
        if not existing_match:
            return None
        
        return await self.match_repository.update(match_id, match_data)
    
    async def delete_match(self, match_id: int) -> bool:
        """Supprime un match"""
        return await self.match_repository.delete(match_id)
    
    async def update_match_status(self, match_id: int, new_status: str) -> Optional[Match]:
        """Met à jour le statut d'un match"""
        existing_match = await self.match_repository.get_by_id(match_id)
        if not existing_match:
            return None
        
        update_data = MatchUpdate(status=new_status)
        return await self.match_repository.update(match_id, update_data)
    
    async def find_matches_for_tender(self, tender_id: int, 
                                     min_score: float = 0.6,
                                     include_partner_consultants: bool = True) -> List[Dict[str, Any]]:
        """
        Trouve les consultants qui correspondent à un appel d'offres
        Inclut les consultants des ESN partenaires si include_partner_consultants est True
        """
        return await self.matchmaking_service.find_matches_for_tender(
            tender_id, min_score, include_partner_consultants
        )
    
    async def find_matches_for_consultant(self, consultant_id: int,
                                         min_score: float = 0.6,
                                         include_partner_tenders: bool = True) -> List[Dict[str, Any]]:
        """
        Trouve les appels d'offres qui correspondent à un consultant
        Inclut les appels d'offres des ESN partenaires si include_partner_tenders est True
        """
        return await self.matchmaking_service.find_matches_for_consultant(
            consultant_id, min_score, include_partner_tenders
        )
    
    async def get_top_matches(self, company_id: int, limit: int = 10) -> List[Dict[str, Any]]:
        """Récupère les meilleurs matchs pour une entreprise"""
        return await self.matchmaking_service.suggest_top_matches(company_id, limit)
