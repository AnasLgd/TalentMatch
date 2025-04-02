from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.entities.tender import TenderCreate, TenderUpdate, TenderResponse
from app.core.use_cases.tender_use_case import TenderUseCase
from app.infrastructure.database.session import get_db
from app.adapters.repositories.tender_repository import TenderRepository

router = APIRouter(
    prefix="/api/tenders",
    tags=["tenders"],
    responses={404: {"description": "Appel d'offres non trouvé"}},
)

def get_tender_use_case(db: Session = Depends(get_db)):
    repository = TenderRepository(db)
    return TenderUseCase(repository)

@router.post("/", response_model=TenderResponse, status_code=status.HTTP_201_CREATED)
async def create_tender(
    tender: TenderCreate,
    use_case: TenderUseCase = Depends(get_tender_use_case)
):
    """
    Crée un nouvel appel d'offres.
    """
    return await use_case.create_tender(tender)

@router.get("/", response_model=List[TenderResponse])
async def get_tenders(
    company_id: Optional[int] = None,
    skill_id: Optional[int] = None,
    status: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    use_case: TenderUseCase = Depends(get_tender_use_case)
):
    """
    Récupère la liste des appels d'offres avec filtres optionnels.
    """
    return await use_case.get_tenders(
        company_id=company_id,
        skill_id=skill_id,
        status=status,
        skip=skip,
        limit=limit
    )

@router.get("/{tender_id}", response_model=TenderResponse)
async def get_tender(
    tender_id: int,
    use_case: TenderUseCase = Depends(get_tender_use_case)
):
    """
    Récupère un appel d'offres par son ID.
    """
    tender = await use_case.get_tender(tender_id)
    if not tender:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Appel d'offres avec l'ID {tender_id} non trouvé"
        )
    return tender

@router.put("/{tender_id}", response_model=TenderResponse)
async def update_tender(
    tender_id: int,
    tender: TenderUpdate,
    use_case: TenderUseCase = Depends(get_tender_use_case)
):
    """
    Met à jour un appel d'offres existant.
    """
    updated_tender = await use_case.update_tender(tender_id, tender)
    if not updated_tender:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Appel d'offres avec l'ID {tender_id} non trouvé"
        )
    return updated_tender

@router.delete("/{tender_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_tender(
    tender_id: int,
    use_case: TenderUseCase = Depends(get_tender_use_case)
):
    """
    Supprime un appel d'offres.
    """
    success = await use_case.delete_tender(tender_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Appel d'offres avec l'ID {tender_id} non trouvé"
        )
    return None

@router.get("/{tender_id}/skills", response_model=List[dict])
async def get_tender_skills(
    tender_id: int,
    use_case: TenderUseCase = Depends(get_tender_use_case)
):
    """
    Récupère les compétences requises pour un appel d'offres.
    """
    skills = await use_case.get_tender_skills(tender_id)
    if skills is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Appel d'offres avec l'ID {tender_id} non trouvé"
        )
    return skills

@router.post("/{tender_id}/skills/{skill_id}")
async def add_skill_to_tender(
    tender_id: int,
    skill_id: int,
    level: int,
    use_case: TenderUseCase = Depends(get_tender_use_case)
):
    """
    Ajoute une compétence requise à un appel d'offres avec un niveau spécifié.
    """
    success = await use_case.add_skill_to_tender(tender_id, skill_id, level)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Appel d'offres avec l'ID {tender_id} ou compétence avec l'ID {skill_id} non trouvé"
        )
    return {"status": "success", "message": "Compétence ajoutée à l'appel d'offres"}

@router.delete("/{tender_id}/skills/{skill_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_skill_from_tender(
    tender_id: int,
    skill_id: int,
    use_case: TenderUseCase = Depends(get_tender_use_case)
):
    """
    Supprime une compétence requise d'un appel d'offres.
    """
    success = await use_case.remove_skill_from_tender(tender_id, skill_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Appel d'offres avec l'ID {tender_id} ou compétence avec l'ID {skill_id} non trouvé"
        )
    return None

@router.post("/{tender_id}/share")
async def share_tender(
    tender_id: int,
    company_ids: List[int],
    use_case: TenderUseCase = Depends(get_tender_use_case)
):
    """
    Partage un appel d'offres avec d'autres entreprises (ESN).
    """
    success = await use_case.share_tender(tender_id, company_ids)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Appel d'offres avec l'ID {tender_id} non trouvé ou problème avec les entreprises spécifiées"
        )
    return {"status": "success", "message": "Appel d'offres partagé avec succès"}

@router.get("/{tender_id}/matches", response_model=List[dict])
async def get_tender_matches(
    tender_id: int,
    min_score: Optional[float] = 0.0,
    skip: int = 0,
    limit: int = 100,
    use_case: TenderUseCase = Depends(get_tender_use_case)
):
    """
    Récupère les correspondances (matches) pour un appel d'offres.
    """
    matches = await use_case.get_tender_matches(tender_id, min_score=min_score, skip=skip, limit=limit)
    if matches is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Appel d'offres avec l'ID {tender_id} non trouvé"
        )
    return matches

@router.post("/{tender_id}/run-matching")
async def run_matching_for_tender(
    tender_id: int,
    use_case: TenderUseCase = Depends(get_tender_use_case)
):
    """
    Lance le processus de matching pour un appel d'offres.
    """
    success = await use_case.run_matching(tender_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Appel d'offres avec l'ID {tender_id} non trouvé ou problème lors du matching"
        )
    return {"status": "success", "message": "Processus de matching lancé avec succès"}
