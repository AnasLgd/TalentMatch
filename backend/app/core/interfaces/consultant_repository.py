from typing import Protocol, List, Optional, Dict, Any
from datetime import date

from app.core.entities.consultant import Consultant, ConsultantCreate, ConsultantUpdate
from app.core.entities.skill import Skill

class ConsultantRepository(Protocol):
    async def get_all(self) -> List[Consultant]:
        ...
    
    async def get_by_id(self, consultant_id: int) -> Optional[Consultant]:
        ...
    
    async def get_by_user_id(self, user_id: int) -> Optional[Consultant]:
        ...
    
    async def get_by_company_id(self, company_id: int) -> List[Consultant]:
        ...
    
    async def create(self, consultant: ConsultantCreate) -> Consultant:
        ...
    
    async def update(self, consultant_id: int, consultant: ConsultantUpdate) -> Optional[Consultant]:
        ...
    
    async def delete(self, consultant_id: int) -> bool:
        ...
    
    async def add_skill(self, consultant_id: int, skill_id: int, proficiency_level: str, 
                        years_experience: Optional[int] = None, details: Optional[str] = None) -> bool:
        ...
    
    async def remove_skill(self, consultant_id: int, skill_id: int) -> bool:
        ...
    
    async def update_skill(self, consultant_id: int, skill_id: int, proficiency_level: Optional[str] = None,
                          years_experience: Optional[int] = None, details: Optional[str] = None) -> bool:
        ...
    
    async def get_skills(self, consultant_id: int) -> List[Dict[str, Any]]:
        ...
    
    async def get_available_consultants(self, from_date: Optional[date] = None, 
                                       to_date: Optional[date] = None) -> List[Consultant]:
        ...
    
    async def search_consultants(self, query: str, skills: Optional[List[int]] = None, 
                                company_id: Optional[int] = None) -> List[Consultant]:
        ...
