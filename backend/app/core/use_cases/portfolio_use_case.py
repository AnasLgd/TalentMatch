from typing import List, Optional, Dict, Any
from fastapi import Depends

from app.core.entities.portfolio import Portfolio, PortfolioCreate, PortfolioUpdate
from app.core.interfaces.portfolio_repository import PortfolioRepository
from app.core.interfaces.consultant_repository import ConsultantRepository
from app.core.interfaces.tender_repository import TenderRepository
from app.core.interfaces.cv_analysis_service import CVAnalysisService

class PortfolioUseCase:
    """
    Cas d'utilisation pour la gestion des dossiers de compétences
    """
    
    def __init__(
        self,
        portfolio_repository: PortfolioRepository,
        consultant_repository: ConsultantRepository,
        tender_repository: TenderRepository,
        cv_analysis_service: CVAnalysisService
    ):
        self.portfolio_repository = portfolio_repository
        self.consultant_repository = consultant_repository
        self.tender_repository = tender_repository
        self.cv_analysis_service = cv_analysis_service
    
    async def get_all_portfolios(self) -> List[Portfolio]:
        """Récupère tous les dossiers de compétences"""
        return await self.portfolio_repository.get_all()
    
    async def get_portfolio_by_id(self, portfolio_id: int) -> Optional[Portfolio]:
        """Récupère un dossier de compétences par son ID"""
        return await self.portfolio_repository.get_by_id(portfolio_id)
    
    async def get_portfolios_by_consultant(self, consultant_id: int) -> List[Portfolio]:
        """Récupère tous les dossiers de compétences d'un consultant"""
        return await self.portfolio_repository.get_by_consultant_id(consultant_id)
    
    async def get_portfolios_by_tender(self, tender_id: int) -> List[Portfolio]:
        """Récupère tous les dossiers de compétences pour un appel d'offres"""
        return await self.portfolio_repository.get_by_tender_id(tender_id)
    
    async def create_portfolio(self, portfolio_data: PortfolioCreate) -> Portfolio:
        """Crée un nouveau dossier de compétences"""
        # Vérifier que le consultant existe
        consultant = await self.consultant_repository.get_by_id(portfolio_data.consultant_id)
        if not consultant:
            raise ValueError("Le consultant n'existe pas")
        
        # Vérifier que l'appel d'offres existe
        tender = await self.tender_repository.get_by_id(portfolio_data.tender_id)
        if not tender:
            raise ValueError("L'appel d'offres n'existe pas")
        
        # Générer le contenu du dossier de compétences si non fourni
        if not portfolio_data.content:
            # Récupérer les données du consultant
            consultant_skills = await self.consultant_repository.get_skills(portfolio_data.consultant_id)
            
            consultant_data = {
                "id": consultant.id,
                "name": f"{consultant.user.get('first_name', '')} {consultant.user.get('last_name', '')}",
                "title": consultant.title,
                "experience_years": consultant.experience_years,
                "bio": consultant.bio,
                "skills": consultant_skills
            }
            
            # Récupérer les données de l'appel d'offres
            tender_skills = await self.tender_repository.get_skills(portfolio_data.tender_id)
            
            tender_data = {
                "id": tender.id,
                "title": tender.title,
                "description": tender.description,
                "skills": tender_skills
            }
            
            # Générer le contenu du dossier de compétences
            portfolio_data.content = await self.cv_analysis_service.generate_skill_portfolio(
                consultant_data, tender_data
            )
        
        return await self.portfolio_repository.create(portfolio_data)
    
    async def update_portfolio(self, portfolio_id: int, 
                              portfolio_data: PortfolioUpdate) -> Optional[Portfolio]:
        """Met à jour un dossier de compétences existant"""
        existing_portfolio = await self.portfolio_repository.get_by_id(portfolio_id)
        if not existing_portfolio:
            return None
        
        return await self.portfolio_repository.update(portfolio_id, portfolio_data)
    
    async def delete_portfolio(self, portfolio_id: int) -> bool:
        """Supprime un dossier de compétences"""
        return await self.portfolio_repository.delete(portfolio_id)
    
    async def export_portfolio_to_pdf(self, portfolio_id: int) -> bytes:
        """Exporte un dossier de compétences au format PDF"""
        portfolio = await self.portfolio_repository.get_by_id(portfolio_id)
        if not portfolio:
            raise ValueError("Le dossier de compétences n'existe pas")
        
        return await self.portfolio_repository.export_to_pdf(portfolio_id)
    
    async def finalize_portfolio(self, portfolio_id: int) -> Optional[Portfolio]:
        """Finalise un dossier de compétences (change son statut en 'final')"""
        existing_portfolio = await self.portfolio_repository.get_by_id(portfolio_id)
        if not existing_portfolio:
            return None
        
        update_data = PortfolioUpdate(status="final")
        return await self.portfolio_repository.update(portfolio_id, update_data)
    
    async def create_new_version(self, portfolio_id: int) -> Optional[Portfolio]:
        """Crée une nouvelle version d'un dossier de compétences existant"""
        existing_portfolio = await self.portfolio_repository.get_by_id(portfolio_id)
        if not existing_portfolio:
            return None
        
        # Créer une nouvelle version avec le même contenu
        new_portfolio_data = PortfolioCreate(
            consultant_id=existing_portfolio.consultant_id,
            tender_id=existing_portfolio.tender_id,
            content=existing_portfolio.content,
            version=existing_portfolio.version + 1,
            status="draft"
        )
        
        return await self.portfolio_repository.create(new_portfolio_data)
