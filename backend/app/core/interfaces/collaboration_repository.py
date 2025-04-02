from typing import Protocol, List, Optional, Dict, Any
from datetime import date

from app.core.entities.collaboration import Collaboration, CollaborationCreate, CollaborationUpdate

class CollaborationRepository(Protocol):
    async def get_all(self) -> List[Collaboration]:
        ...
    
    async def get_by_id(self, collaboration_id: int) -> Optional[Collaboration]:
        ...
    
    async def get_by_initiator_company_id(self, company_id: int) -> List[Collaboration]:
        ...
    
    async def get_by_partner_company_id(self, company_id: int) -> List[Collaboration]:
        ...
    
    async def get_by_company_id(self, company_id: int) -> List[Collaboration]:
        """Récupère toutes les collaborations où l'entreprise est soit initiatrice soit partenaire"""
        ...
    
    async def create(self, collaboration: CollaborationCreate) -> Collaboration:
        ...
    
    async def update(self, collaboration_id: int, collaboration: CollaborationUpdate) -> Optional[Collaboration]:
        ...
    
    async def delete(self, collaboration_id: int) -> bool:
        ...
    
    async def get_by_status(self, status: str) -> List[Collaboration]:
        ...
    
    async def get_active_collaborations(self, date_reference: Optional[date] = None) -> List[Collaboration]:
        """Récupère les collaborations actives à une date donnée (par défaut aujourd'hui)"""
        ...
