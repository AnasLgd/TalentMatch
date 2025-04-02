from typing import Protocol, List, Optional, Dict, Any
from datetime import date

class CollaborationService(Protocol):
    """
    Service pour la gestion des collaborations inter-ESN
    Priorité maximale selon le document MVP
    """
    
    async def initiate_collaboration(self, initiator_company_id: int, 
                                    partner_company_id: int,
                                    terms: Optional[str] = None) -> Dict[str, Any]:
        """
        Initie une collaboration entre deux ESN
        """
        ...
    
    async def accept_collaboration(self, collaboration_id: int) -> bool:
        """
        Accepte une proposition de collaboration
        """
        ...
    
    async def reject_collaboration(self, collaboration_id: int) -> bool:
        """
        Rejette une proposition de collaboration
        """
        ...
    
    async def terminate_collaboration(self, collaboration_id: int) -> bool:
        """
        Met fin à une collaboration active
        """
        ...
    
    async def get_collaboration_statistics(self, company_id: int) -> Dict[str, Any]:
        """
        Récupère des statistiques sur les collaborations d'une ESN
        """
        ...
    
    async def share_tender(self, tender_id: int, partner_company_ids: List[int]) -> bool:
        """
        Partage un appel d'offres avec des ESN partenaires
        """
        ...
    
    async def share_consultant_profile(self, consultant_id: int, 
                                      partner_company_ids: List[int],
                                      anonymize: bool = True) -> bool:
        """
        Partage un profil de consultant avec des ESN partenaires
        Option pour anonymiser les données personnelles
        """
        ...
