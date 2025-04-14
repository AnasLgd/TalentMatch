from typing import List, Optional, Dict, Any
from fastapi import Depends

from app.core.entities.consultant import Consultant, ConsultantCreate, ConsultantUpdate
from app.core.entities.skill import Skill
from app.core.interfaces.consultant_repository import ConsultantRepository
from app.core.interfaces.skill_repository import SkillRepository
from app.core.interfaces.user_repository import UserRepository
from app.core.interfaces.company_repository import CompanyRepository

class ConsultantUseCase:
    """
    Cas d'utilisation pour la gestion des consultants
    """
    
    def __init__(
        self,
        consultant_repository: ConsultantRepository,
        skill_repository: SkillRepository,
        user_repository: UserRepository,
        company_repository: CompanyRepository
    ):
        self.consultant_repository = consultant_repository
        self.skill_repository = skill_repository
        self.user_repository = user_repository
        self.company_repository = company_repository
    
    async def get_all_consultants(
        self,
        company_id: Optional[int] = None,
        skill_id: Optional[int] = None,
        availability: Optional[bool] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Consultant]:
        """
        Récupère tous les consultants, avec filtres optionnels
        """
        # 1. Base: on récupère tous les consultants
        consultants = await self.consultant_repository.get_all()

        # 2. Filtres
        if company_id is not None:
            # ex : on peut récupérer la liste via get_by_company_id
            consultants = await self.consultant_repository.get_by_company_id(company_id)

        # si tu veux filtrer par skill_id => consultant_repository.search_consultants
        # si tu veux filtrer par availability => 
        #   ex. re-filtrer localement, ou un repository method get_by_availability

        # 3. skip / limit
        # s'il s'agit d'une simple liste Python:
        # consultants = consultants[skip : skip + limit]
        # ou s'il s'agit d'une query, on peut le faire avant un .all() (dans le repo)

        return consultants
    
    async def get_consultant_by_id(self, consultant_id: int) -> Optional[Consultant]:
        """Récupère un consultant par son ID"""
        return await self.consultant_repository.get_by_id(consultant_id)
    
    async def get_consultants_by_company(self, company_id: int) -> List[Consultant]:
        """Récupère tous les consultants d'une entreprise"""
        return await self.consultant_repository.get_by_company_id(company_id)
    
    async def create_consultant(self, consultant_data: ConsultantCreate) -> Consultant:
        """Crée un nouveau consultant"""
        # Vérifier que l'utilisateur existe
        user = await self.user_repository.get_by_id(consultant_data.user_id)
        if not user:
            raise ValueError("L'utilisateur n'existe pas")
        
        # Vérifier que l'entreprise existe
        company = await self.company_repository.get_by_id(consultant_data.company_id)
        if not company:
            raise ValueError("L'entreprise n'existe pas")
        
        # Vérifier que l'utilisateur n'est pas déjà un consultant
        existing_consultant = await self.consultant_repository.get_by_user_id(consultant_data.user_id)
        if existing_consultant:
            raise ValueError("Cet utilisateur est déjà un consultant")
        
        # Créer le consultant
        consultant = await self.consultant_repository.create(consultant_data)
        
        # Ajouter les compétences si fournies
        if consultant_data.skills:
            for skill_data in consultant_data.skills:
                skill_id = skill_data.get("skill_id")
                proficiency_level = skill_data.get("proficiency_level")
                years_experience = skill_data.get("years_experience")
                details = skill_data.get("details")
                
                # Vérifier que la compétence existe
                skill = await self.skill_repository.get_by_id(skill_id)
                if not skill:
                    continue
                
                await self.consultant_repository.add_skill(
                    consultant.id, skill_id, proficiency_level, years_experience, details
                )
        
        return consultant
    
    async def update_consultant(self, consultant_id: int, 
                               consultant_data: ConsultantUpdate) -> Optional[Consultant]:
        """Met à jour un consultant existant"""
        existing_consultant = await self.consultant_repository.get_by_id(consultant_id)
        if not existing_consultant:
            return None
        
        # Mettre à jour les informations du consultant
        updated_consultant = await self.consultant_repository.update(consultant_id, consultant_data)
        
        # Mettre à jour les compétences si fournies
        if consultant_data.skills:
            # Récupérer les compétences actuelles
            current_skills = await self.consultant_repository.get_skills(consultant_id)
            current_skill_ids = [skill["skill_id"] for skill in current_skills]
            
            # Traiter les nouvelles compétences
            for skill_data in consultant_data.skills:
                skill_id = skill_data.get("skill_id")
                proficiency_level = skill_data.get("proficiency_level")
                years_experience = skill_data.get("years_experience")
                details = skill_data.get("details")
                
                # Vérifier que la compétence existe
                skill = await self.skill_repository.get_by_id(skill_id)
                if not skill:
                    continue
                
                # Ajouter ou mettre à jour la compétence
                if skill_id in current_skill_ids:
                    await self.consultant_repository.update_skill(
                        consultant_id, skill_id, proficiency_level, years_experience, details
                    )
                else:
                    await self.consultant_repository.add_skill(
                        consultant_id, skill_id, proficiency_level, years_experience, details
                    )
        
        return updated_consultant
    
    async def delete_consultant(self, consultant_id: int) -> bool:
        """Supprime un consultant"""
        return await self.consultant_repository.delete(consultant_id)
    
    async def get_consultant_skills(self, consultant_id: int) -> List[Dict[str, Any]]:
        """Récupère les compétences d'un consultant"""
        return await self.consultant_repository.get_skills(consultant_id)
    
    async def add_consultant_skill(self, consultant_id: int, skill_id: int, 
                                  proficiency_level: str, years_experience: Optional[int] = None, 
                                  details: Optional[str] = None) -> bool:
        """Ajoute une compétence à un consultant"""
        # Vérifier que le consultant existe
        consultant = await self.consultant_repository.get_by_id(consultant_id)
        if not consultant:
            raise ValueError("Le consultant n'existe pas")
        
        # Vérifier que la compétence existe
        skill = await self.skill_repository.get_by_id(skill_id)
        if not skill:
            raise ValueError("La compétence n'existe pas")
        
        return await self.consultant_repository.add_skill(
            consultant_id, skill_id, proficiency_level, years_experience, details
        )
    
    async def remove_consultant_skill(self, consultant_id: int, skill_id: int) -> bool:
        """Supprime une compétence d'un consultant"""
        return await self.consultant_repository.remove_skill(consultant_id, skill_id)
    
    async def get_available_consultants(self) -> List[Consultant]:
        """Récupère les consultants disponibles"""
        return await self.consultant_repository.get_available_consultants()
    
    async def search_consultants(self, query: str, skills: Optional[List[int]] = None, 
                               company_id: Optional[int] = None) -> List[Consultant]:
        """Recherche des consultants par critères"""
        return await self.consultant_repository.search_consultants(query, skills, company_id)
