from typing import Protocol, List, Optional, Dict, Any

from app.core.entities.portfolio import Portfolio, PortfolioCreate, PortfolioUpdate

class PortfolioRepository(Protocol):
    async def get_all(self) -> List[Portfolio]:
        ...
    
    async def get_by_id(self, portfolio_id: int) -> Optional[Portfolio]:
        ...
    
    async def get_by_consultant_id(self, consultant_id: int) -> List[Portfolio]:
        ...
    
    async def get_by_tender_id(self, tender_id: int) -> List[Portfolio]:
        ...
    
    async def create(self, portfolio: PortfolioCreate) -> Portfolio:
        ...
    
    async def update(self, portfolio_id: int, portfolio: PortfolioUpdate) -> Optional[Portfolio]:
        ...
    
    async def delete(self, portfolio_id: int) -> bool:
        ...
    
    async def get_by_status(self, status: str) -> List[Portfolio]:
        ...
    
    async def get_by_company_id(self, company_id: int) -> List[Portfolio]:
        ...
    
    async def export_to_pdf(self, portfolio_id: int) -> bytes:
        ...
