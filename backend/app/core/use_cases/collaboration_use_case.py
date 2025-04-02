from typing import List, Optional, Dict, Any
from fastapi import Depends

from app.core.entities.collaboration import Collaboration, CollaborationCreate, CollaborationUpdate
from app.core.interfaces.collaboration_repository import CollaborationRepository
from app.core.interfaces.company_repository import CompanyRepository

class CollaborationUseCase:
    """
    Cas d'utilisation pour la gestion des collaborations inter-ESN
    Priorité maximale selon le document MVP
    """
    
    def __init__(
        self,
        collaboration_repository: CollaborationRepository,
        company_repository: CompanyRepository
    ):
        self.collaboration_repository = collaboration_repository
        self.company_repository = company_repository
    
    async def get_all_collaborations(self) -> List[Collaboration]:
        """Récupère toutes les collaborations"""
        return await self.collaboration_repository.get_all()
    
    async def get_collaboration_by_id(self, collaboration_id: int) -> Optional[Collaboration]:
        """Récupère une collaboration par son ID"""
        return await self.collaboration_repository.get_by_id(collaboration_id)
    
    async def get_company_collaborations(self, company_id: int) -> List[Collaboration]:
        """Récupère toutes les collaborations d'une entreprise (initiatrice ou partenaire)"""
        return await self.collaboration_repository.get_by_company_id(company_id)
    
    async def create_collaboration(self, collaboration_data: CollaborationCreate) -> Collaboration:
        """Crée une nouvelle collaboration"""
        # Vérifier que les entreprises existent
        initiator = await self.company_repository.get_by_id(collaboration_data.initiator_company_id)
        partner = await self.company_repository.get_by_id(collaboration_data.partner_company_id)
        
        if not initiator or not partner:
            raise ValueError("L'une des entreprises n'existe pas")
        
        # Vérifier qu'une collaboration n'existe pas déjà entre ces entreprises
        existing_collaborations = await self.collaboration_repository.get_by_company_id(collaboration_data.initiator_company_id)
        for collab in existing_collaborations:
            if (collab.initiator_company_id == collaboration_data.initiator_company_id and 
                collab.partner_company_id == collaboration_data.partner_company_id) or \
               (collab.initiator_company_id == collaboration_data.partner_company_id and 
                collab.partner_company_id == collaboration_data.initiator_company_id):
                raise ValueError("Une collaboration existe déjà entre ces entreprises")
        
        return await self.collaboration_repository.create(collaboration_data)
    
    async def update_collaboration(self, collaboration_id: int, 
                                  collaboration_data: CollaborationUpdate) -> Optional[Collaboration]:
        """Met à jour une collaboration existante"""
        existing_collaboration = await self.collaboration_repository.get_by_id(collaboration_id)
        if not existing_collaboration:
            return None
        
        return await self.collaboration_repository.update(collaboration_id, collaboration_data)
    
    async def delete_collaboration(self, collaboration_id: int) -> bool:
        """Supprime une collaboration"""
        return await self.collaboration_repository.delete(collaboration_id)
    
    async def activate_collaboration(self, collaboration_id: int) -> Optional[Collaboration]:
        """Active une collaboration (change son statut en 'active')"""
        existing_collaboration = await self.collaboration_repository.get_by_id(collaboration_id)
        if not existing_collaboration:
            return None
        
        update_data = CollaborationUpdate(status="active")
        return await self.collaboration_repository.update(collaboration_id, update_data)
    
    async def deactivate_collaboration(self, collaboration_id: int) -> Optional[Collaboration]:
        """Désactive une collaboration (change son statut en 'inactive')"""
        existing_collaboration = await self.collaboration_repository.get_by_id(collaboration_id)
        if not existing_collaboration:
            return None
        
        update_data = CollaborationUpdate(status="inactive")
        return await self.collaboration_repository.update(collaboration_id, update_data)
    
    async def get_collaboration_partners(self, company_id: int) -> List[Dict[str, Any]]:
        """Récupère les entreprises partenaires d'une entreprise"""
        collaborations = await self.collaboration_repository.get_by_company_id(company_id)
        partners = []
        
        for collab in collaborations:
            if collab.status != "active":
                continue
                
            partner_id = collab.partner_company_id
            if collab.initiator_company_id != company_id:
                partner_id = collab.initiator_company_id
                
            partner = await self.company_repository.get_by_id(partner_id)
            if partner:
                partners.append({
                    "company": partner,
                    "collaboration_id": collab.id,
                    "collaboration_status": collab.status,
                    "start_date": collab.start_date,
                    "end_date": collab.end_date
                })
        
        return partners
