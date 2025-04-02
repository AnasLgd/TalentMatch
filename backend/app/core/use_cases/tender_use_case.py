from typing import List, Optional, Dict, Any
from fastapi import Depends

from app.core.entities.tender import Tender, TenderCreate, TenderUpdate
from app.core.interfaces.tender_repository import TenderRepository
from app.core.interfaces.skill_repository import SkillRepository
from app.core.interfaces.company_repository import CompanyRepository
from app.core.interfaces.collaboration_repository import CollaborationRepository

class TenderUseCase:
    """
    Cas d'utilisation pour la gestion des appels d'offres
    Priorité moyenne selon le document MVP
    """
    
    def __init__(
        self,
        tender_repository: TenderRepository,
        skill_repository: SkillRepository,
        company_repository: CompanyRepository,
        collaboration_repository: CollaborationRepository
    ):
        self.tender_repository = tender_repository
        self.skill_repository = skill_repository
        self.company_repository = company_repository
        self.collaboration_repository = collaboration_repository
    
    async def get_all_tenders(self) -> List[Tender]:
        """Récupère tous les appels d'offres"""
        return await self.tender_repository.get_all()
    
    async def get_tender_by_id(self, tender_id: int) -> Optional[Tender]:
        """Récupère un appel d'offres par son ID"""
        return await self.tender_repository.get_by_id(tender_id)
    
    async def get_tenders_by_company(self, company_id: int) -> List[Tender]:
        """Récupère tous les appels d'offres d'une entreprise"""
        return await self.tender_repository.get_by_company_id(company_id)
    
    async def create_tender(self, tender_data: TenderCreate) -> Tender:
        """Crée un nouvel appel d'offres"""
        # Vérifier que l'entreprise existe
        company = await self.company_repository.get_by_id(tender_data.company_id)
        if not company:
            raise ValueError("L'entreprise n'existe pas")
        
        # Créer l'appel d'offres
        tender = await self.tender_repository.create(tender_data)
        
        # Ajouter les compétences si fournies
        if tender_data.skills:
            for skill_data in tender_data.skills:
                skill_id = skill_data.get("skill_id")
                importance = skill_data.get("importance")
                details = skill_data.get("details")
                
                # Vérifier que la compétence existe
                skill = await self.skill_repository.get_by_id(skill_id)
                if not skill:
                    continue
                
                await self.tender_repository.add_skill(
                    tender.id, skill_id, importance, details
                )
        
        return tender
    
    async def update_tender(self, tender_id: int, 
                           tender_data: TenderUpdate) -> Optional[Tender]:
        """Met à jour un appel d'offres existant"""
        existing_tender = await self.tender_repository.get_by_id(tender_id)
        if not existing_tender:
            return None
        
        # Mettre à jour les informations de l'appel d'offres
        updated_tender = await self.tender_repository.update(tender_id, tender_data)
        
        # Mettre à jour les compétences si fournies
        if tender_data.skills:
            # Récupérer les compétences actuelles
            current_skills = await self.tender_repository.get_skills(tender_id)
            current_skill_ids = [skill["skill_id"] for skill in current_skills]
            
            # Traiter les nouvelles compétences
            for skill_data in tender_data.skills:
                skill_id = skill_data.get("skill_id")
                importance = skill_data.get("importance")
                details = skill_data.get("details")
                
                # Vérifier que la compétence existe
                skill = await self.skill_repository.get_by_id(skill_id)
                if not skill:
                    continue
                
                # Ajouter ou mettre à jour la compétence
                if skill_id in current_skill_ids:
                    await self.tender_repository.update_skill(
                        tender_id, skill_id, importance, details
                    )
                else:
                    await self.tender_repository.add_skill(
                        tender_id, skill_id, importance, details
                    )
        
        return updated_tender
    
    async def delete_tender(self, tender_id: int) -> bool:
        """Supprime un appel d'offres"""
        return await self.tender_repository.delete(tender_id)
    
    async def get_tender_skills(self, tender_id: int) -> List[Dict[str, Any]]:
        """Récupère les compétences requises pour un appel d'offres"""
        return await self.tender_repository.get_skills(tender_id)
    
    async def add_tender_skill(self, tender_id: int, skill_id: int, 
                              importance: str, details: Optional[str] = None) -> bool:
        """Ajoute une compétence requise à un appel d'offres"""
        # Vérifier que l'appel d'offres existe
        tender = await self.tender_repository.get_by_id(tender_id)
        if not tender:
            raise ValueError("L'appel d'offres n'existe pas")
        
        # Vérifier que la compétence existe
        skill = await self.skill_repository.get_by_id(skill_id)
        if not skill:
            raise ValueError("La compétence n'existe pas")
        
        return await self.tender_repository.add_skill(
            tender_id, skill_id, importance, details
        )
    
    async def remove_tender_skill(self, tender_id: int, skill_id: int) -> bool:
        """Supprime une compétence requise d'un appel d'offres"""
        return await self.tender_repository.remove_skill(tender_id, skill_id)
    
    async def get_active_tenders(self) -> List[Tender]:
        """Récupère les appels d'offres actifs"""
        return await self.tender_repository.get_active_tenders()
    
    async def search_tenders(self, query: str, skills: Optional[List[int]] = None, 
                            company_id: Optional[int] = None, status: Optional[str] = None) -> List[Tender]:
        """Recherche des appels d'offres par critères"""
        return await self.tender_repository.search_tenders(query, skills, company_id, status)
    
    async def share_tender_with_partners(self, tender_id: int, partner_company_ids: List[int]) -> bool:
        """
        Partage un appel d'offres avec des entreprises partenaires
        Fonctionnalité clé pour la collaboration inter-ESN (priorité maximale)
        """
        # Vérifier que l'appel d'offres existe
        tender = await self.tender_repository.get_by_id(tender_id)
        if not tender:
            raise ValueError("L'appel d'offres n'existe pas")
        
        # Vérifier que l'entreprise propriétaire de l'appel d'offres a des collaborations actives avec les partenaires
        for partner_id in partner_company_ids:
            # Vérifier que l'entreprise partenaire existe
            partner = await self.company_repository.get_by_id(partner_id)
            if not partner:
                continue
            
            # Vérifier qu'une collaboration active existe
            collaborations = await self.collaboration_repository.get_by_company_id(tender.company_id)
            has_active_collaboration = False
            
            for collab in collaborations:
                if ((collab.initiator_company_id == tender.company_id and collab.partner_company_id == partner_id) or
                    (collab.initiator_company_id == partner_id and collab.partner_company_id == tender.company_id)) and \
                   collab.status == "active":
                    has_active_collaboration = True
                    break
            
            if not has_active_collaboration:
                continue
            
            # Logique de partage à implémenter dans l'adaptateur
            # Pour le MVP, on pourrait simplement créer une copie de l'appel d'offres pour l'entreprise partenaire
            # avec une référence à l'appel d'offres original
            
        return True
