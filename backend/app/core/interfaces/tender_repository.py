from typing import Protocol, List, Optional, Dict, Any

from app.core.entities.tender import Tender, TenderCreate, TenderUpdate

class TenderRepository(Protocol):
    async def get_all(self) -> List[Tender]:
        ...
    
    async def get_by_id(self, tender_id: int) -> Optional[Tender]:
        ...
    
    async def get_by_company_id(self, company_id: int) -> List[Tender]:
        ...
    
    async def create(self, tender: TenderCreate) -> Tender:
        ...
    
    async def update(self, tender_id: int, tender: TenderUpdate) -> Optional[Tender]:
        ...
    
    async def delete(self, tender_id: int) -> bool:
        ...
    
    async def add_skill(self, tender_id: int, skill_id: int, importance: str, 
                       details: Optional[str] = None) -> bool:
        ...
    
    async def remove_skill(self, tender_id: int, skill_id: int) -> bool:
        ...
    
    async def update_skill(self, tender_id: int, skill_id: int, importance: Optional[str] = None,
                          details: Optional[str] = None) -> bool:
        ...
    
    async def get_skills(self, tender_id: int) -> List[Dict[str, Any]]:
        ...
    
    async def get_active_tenders(self) -> List[Tender]:
        ...
    
    async def search_tenders(self, query: str, skills: Optional[List[int]] = None, 
                            company_id: Optional[int] = None, status: Optional[str] = None) -> List[Tender]:
        ...
