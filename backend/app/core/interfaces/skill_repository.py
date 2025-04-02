from typing import Protocol, List, Optional, Dict, Any

from app.core.entities.skill import Skill, SkillCreate, SkillUpdate

class SkillRepository(Protocol):
    async def get_all(self) -> List[Skill]:
        ...
    
    async def get_by_id(self, skill_id: int) -> Optional[Skill]:
        ...
    
    async def get_by_name(self, name: str) -> Optional[Skill]:
        ...
    
    async def get_by_category(self, category: str) -> List[Skill]:
        ...
    
    async def create(self, skill: SkillCreate) -> Skill:
        ...
    
    async def update(self, skill_id: int, skill: SkillUpdate) -> Optional[Skill]:
        ...
    
    async def delete(self, skill_id: int) -> bool:
        ...
    
    async def search_skills(self, query: str) -> List[Skill]:
        ...
    
    async def get_popular_skills(self, limit: int = 10) -> List[Skill]:
        """Récupère les compétences les plus demandées dans les appels d'offres"""
        ...
    
    async def get_consultant_skills(self, consultant_id: int) -> List[Dict[str, Any]]:
        """Récupère les compétences d'un consultant avec leur niveau de maîtrise"""
        ...
    
    async def get_tender_skills(self, tender_id: int) -> List[Dict[str, Any]]:
        """Récupère les compétences requises pour un appel d'offres avec leur importance"""
        ...
