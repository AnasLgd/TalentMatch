from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

from app.core.interfaces.company_repository import CompanyRepository
from app.core.entities.company import Company, CompanyCreate, CompanyUpdate
from app.infrastructure.database.models import Company as CompanyModel

class SQLAlchemyCompanyRepository(CompanyRepository):
    """
    Implémentation SQLAlchemy du repository pour les entreprises
    """
    
    def __init__(self, db: Session):
        self.db = db
    
    async def get_all(self) -> List[Company]:
        """Récupère toutes les entreprises"""
        companies = self.db.query(CompanyModel).all()
        return [self._map_to_entity(company) for company in companies]
    
    async def get_by_id(self, company_id: int) -> Optional[Company]:
        """Récupère une entreprise par son ID"""
        company = self.db.query(CompanyModel).filter(CompanyModel.id == company_id).first()
        if not company:
            return None
        return self._map_to_entity(company)
    
    async def get_by_name(self, name: str) -> Optional[Company]:
        """Récupère une entreprise par son nom"""
        company = self.db.query(CompanyModel).filter(CompanyModel.name == name).first()
        if not company:
            return None
        return self._map_to_entity(company)
    
    async def create(self, company: CompanyCreate) -> Company:
        """Crée une nouvelle entreprise"""
        try:
            db_company = CompanyModel(
                name=company.name,
                description=company.description,
                website=company.website,
                address=company.address,
                city=company.city,
                postal_code=company.postal_code,
                country=company.country,
                is_active=True
            )
            
            self.db.add(db_company)
            self.db.commit()
            self.db.refresh(db_company)
            
            return self._map_to_entity(db_company)
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Une entreprise avec ce nom existe déjà"
            )
    
    async def update(self, company_id: int, company: CompanyUpdate) -> Optional[Company]:
        """Met à jour une entreprise existante"""
        db_company = self.db.query(CompanyModel).filter(CompanyModel.id == company_id).first()
        if not db_company:
            return None
        
        # Mettre à jour les champs
        update_data = company.dict(exclude_unset=True)
        
        for key, value in update_data.items():
            setattr(db_company, key, value)
        
        try:
            self.db.commit()
            self.db.refresh(db_company)
            return self._map_to_entity(db_company)
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Erreur lors de la mise à jour de l'entreprise"
            )
    
    async def delete(self, company_id: int) -> bool:
        """Supprime une entreprise"""
        db_company = self.db.query(CompanyModel).filter(CompanyModel.id == company_id).first()
        if not db_company:
            return False
        
        self.db.delete(db_company)
        self.db.commit()
        return True
    
    async def get_active_companies(self) -> List[Company]:
        """Récupère les entreprises actives"""
        companies = self.db.query(CompanyModel).filter(CompanyModel.is_active == True).all()
        return [self._map_to_entity(company) for company in companies]
    
    async def search_companies(self, query: str) -> List[Company]:
        """Recherche des entreprises par critères"""
        search = f"%{query}%"
        companies = self.db.query(CompanyModel).filter(
            (CompanyModel.name.ilike(search)) |
            (CompanyModel.description.ilike(search)) |
            (CompanyModel.city.ilike(search)) |
            (CompanyModel.country.ilike(search))
        ).all()
        return [self._map_to_entity(company) for company in companies]
    
    async def get_collaboration_partners(self, company_id: int) -> List[Company]:
        """Récupère toutes les entreprises avec lesquelles une entreprise a des collaborations actives"""
        # Cette méthode nécessite une requête plus complexe avec des jointures
        # Pour simplifier, nous allons utiliser une requête SQL brute
        
        query = """
        SELECT c.* FROM companies c
        JOIN collaborations collab ON 
            (collab.initiator_company_id = :company_id AND collab.partner_company_id = c.id)
            OR (collab.partner_company_id = :company_id AND collab.initiator_company_id = c.id)
        WHERE collab.status = 'active'
        """
        
        result = self.db.execute(query, {"company_id": company_id})
        companies = [CompanyModel(**dict(row)) for row in result]
        
        return [self._map_to_entity(company) for company in companies]
    
    def _map_to_entity(self, db_company: CompanyModel) -> Company:
        """Convertit un modèle SQLAlchemy en entité"""
        return Company(
            id=db_company.id,
            name=db_company.name,
            description=db_company.description,
            website=db_company.website,
            address=db_company.address,
            city=db_company.city,
            postal_code=db_company.postal_code,
            country=db_company.country,
            is_active=db_company.is_active,
            created_at=db_company.created_at,
            updated_at=db_company.updated_at
        )
