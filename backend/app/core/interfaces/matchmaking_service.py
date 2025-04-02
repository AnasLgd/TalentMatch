from typing import Protocol, List, Optional, Dict, Any
from datetime import date

class MatchmakingService(Protocol):
    """
    Service pour le matchmaking entre consultants et appels d'offres
    Partie de la fonctionnalité de collaboration inter-ESN (priorité maximale)
    """
    
    async def find_matches_for_tender(self, tender_id: int, 
                                     min_score: float = 0.6,
                                     include_partner_consultants: bool = True) -> List[Dict[str, Any]]:
        """
        Trouve les consultants qui correspondent à un appel d'offres
        Inclut les consultants des ESN partenaires si include_partner_consultants est True
        """
        ...
    
    async def find_matches_for_consultant(self, consultant_id: int,
                                         min_score: float = 0.6,
                                         include_partner_tenders: bool = True) -> List[Dict[str, Any]]:
        """
        Trouve les appels d'offres qui correspondent à un consultant
        Inclut les appels d'offres des ESN partenaires si include_partner_tenders est True
        """
        ...
    
    async def calculate_match_score(self, consultant_id: int, tender_id: int) -> float:
        """
        Calcule le score de correspondance entre un consultant et un appel d'offres
        """
        ...
    
    async def suggest_top_matches(self, company_id: int, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Suggère les meilleures correspondances pour une ESN
        """
        ...
    
    async def update_match_status(self, match_id: int, new_status: str) -> bool:
        """
        Met à jour le statut d'une correspondance
        """
        ...
