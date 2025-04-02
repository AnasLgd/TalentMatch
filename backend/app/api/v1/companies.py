from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.entities.company import CompanyCreate, CompanyUpdate, CompanyResponse
from app.core.use_cases.user_use_case import UserUseCase
from app.infrastructure.database.session import get_db
from app.adapters.repositories.company_repository import CompanyRepository

router = APIRouter(
    prefix="/api/companies",
    tags=["companies"],
    responses={404: {"description": "Entreprise non trouvée"}},
)

def get_company_repository(db: Session = Depends(get_db)):
    return CompanyRepository(db)

@router.post("/", response_model=CompanyResponse, status_code=status.HTTP_201_CREATED)
async def create_company(
    company: CompanyCreate,
    repository: CompanyRepository = Depends(get_company_repository)
):
    """
    Crée une nouvelle entreprise (ESN).
    """
    return await repository.create(company)

@router.get("/", response_model=List[CompanyResponse])
async def get_companies(
    name: Optional[str] = None,
    city: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    repository: CompanyRepository = Depends(get_company_repository)
):
    """
    Récupère la liste des entreprises avec filtres optionnels.
    """
    return await repository.get_all(name=name, city=city, skip=skip, limit=limit)

@router.get("/{company_id}", response_model=CompanyResponse)
async def get_company(
    company_id: int,
    repository: CompanyRepository = Depends(get_company_repository)
):
    """
    Récupère une entreprise par son ID.
    """
    company = await repository.get_by_id(company_id)
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Entreprise avec l'ID {company_id} non trouvée"
        )
    return company

@router.put("/{company_id}", response_model=CompanyResponse)
async def update_company(
    company_id: int,
    company: CompanyUpdate,
    repository: CompanyRepository = Depends(get_company_repository)
):
    """
    Met à jour une entreprise existante.
    """
    updated_company = await repository.update(company_id, company)
    if not updated_company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Entreprise avec l'ID {company_id} non trouvée"
        )
    return updated_company

@router.delete("/{company_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_company(
    company_id: int,
    repository: CompanyRepository = Depends(get_company_repository)
):
    """
    Supprime une entreprise.
    """
    success = await repository.delete(company_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Entreprise avec l'ID {company_id} non trouvée"
        )
    return None

@router.get("/{company_id}/consultants", response_model=List[dict])
async def get_company_consultants(
    company_id: int,
    skip: int = 0,
    limit: int = 100,
    repository: CompanyRepository = Depends(get_company_repository)
):
    """
    Récupère les consultants d'une entreprise.
    """
    consultants = await repository.get_consultants(company_id, skip=skip, limit=limit)
    if consultants is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Entreprise avec l'ID {company_id} non trouvée"
        )
    return consultants

@router.get("/{company_id}/collaborations", response_model=List[dict])
async def get_company_collaborations(
    company_id: int,
    skip: int = 0,
    limit: int = 100,
    repository: CompanyRepository = Depends(get_company_repository)
):
    """
    Récupère les collaborations d'une entreprise.
    """
    collaborations = await repository.get_collaborations(company_id, skip=skip, limit=limit)
    if collaborations is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Entreprise avec l'ID {company_id} non trouvée"
        )
    return collaborations

@router.get("/{company_id}/tenders", response_model=List[dict])
async def get_company_tenders(
    company_id: int,
    status: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    repository: CompanyRepository = Depends(get_company_repository)
):
    """
    Récupère les appels d'offres d'une entreprise.
    """
    tenders = await repository.get_tenders(company_id, status=status, skip=skip, limit=limit)
    if tenders is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Entreprise avec l'ID {company_id} non trouvée"
        )
    return tenders

@router.get("/{company_id}/stats", response_model=dict)
async def get_company_stats(
    company_id: int,
    repository: CompanyRepository = Depends(get_company_repository)
):
    """
    Récupère les statistiques d'une entreprise.
    """
    stats = await repository.get_stats(company_id)
    if stats is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Entreprise avec l'ID {company_id} non trouvée"
        )
    return stats
