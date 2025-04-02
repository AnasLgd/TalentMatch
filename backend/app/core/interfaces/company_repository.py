from typing import Protocol, List, Optional, Dict, Any

from app.core.entities.company import Company, CompanyCreate, CompanyUpdate

class CompanyRepository(Protocol):
    async def get_all(self) -> List[Company]:
        ...
    
    async def get_by_id(self, company_id: int) -> Optional[Company]:
        ...
    
    async def get_by_name(self, name: str) -> Optional[Company]:
        ...
    
    async def create(self, company: CompanyCreate) -> Company:
        ...
    
    async def update(self, company_id: int, company: CompanyUpdate) -> Optional[Company]:
        ...
    
    async def delete(self, company_id: int) -> bool:
        ...
    
    async def get_active_companies(self) -> List[Company]:
        ...
    
    async def search_companies(self, query: str) -> List[Company]:
        ...
    
    async def get_collaboration_partners(self, company_id: int) -> List[Company]:
        """Récupère toutes les entreprises avec lesquelles une entreprise a des collaborations actives"""
        ...
