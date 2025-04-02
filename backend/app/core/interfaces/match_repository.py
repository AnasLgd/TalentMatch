from typing import Protocol, List, Optional, Dict, Any

from app.core.entities.match import Match, MatchCreate, MatchUpdate

class MatchRepository(Protocol):
    async def get_all(self) -> List[Match]:
        ...
    
    async def get_by_id(self, match_id: int) -> Optional[Match]:
        ...
    
    async def get_by_consultant_id(self, consultant_id: int) -> List[Match]:
        ...
    
    async def get_by_tender_id(self, tender_id: int) -> List[Match]:
        ...
    
    async def create(self, match: MatchCreate) -> Match:
        ...
    
    async def update(self, match_id: int, match: MatchUpdate) -> Optional[Match]:
        ...
    
    async def delete(self, match_id: int) -> bool:
        ...
    
    async def get_matches_by_status(self, status: str) -> List[Match]:
        ...
    
    async def get_matches_by_company_id(self, company_id: int) -> List[Match]:
        ...
    
    async def get_matches_above_threshold(self, threshold: float) -> List[Match]:
        ...
