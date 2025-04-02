from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.entities.consultant import ConsultantCreate, ConsultantUpdate, ConsultantResponse
from app.core.use_cases.consultant_use_case import ConsultantUseCase
from app.infrastructure.database.session import get_db
from app.adapters.repositories.consultant_repository import ConsultantRepository

router = APIRouter(
    prefix="/api/consultants",
    tags=["consultants"],
    responses={404: {"description": "Consultant non trouvé"}},
)

def get_consultant_use_case(db: Session = Depends(get_db)):
    repository = ConsultantRepository(db)
    return ConsultantUseCase(repository)

@router.post("/", response_model=ConsultantResponse, status_code=status.HTTP_201_CREATED)
async def create_consultant(
    consultant: ConsultantCreate,
    use_case: ConsultantUseCase = Depends(get_consultant_use_case)
):
    """
    Crée un nouveau consultant.
    """
    return await use_case.create_consultant(consultant)

@router.get("/", response_model=List[ConsultantResponse])
async def get_consultants(
    company_id: Optional[int] = None,
    skill_id: Optional[int] = None,
    availability: Optional[bool] = None,
    skip: int = 0,
    limit: int = 100,
    use_case: ConsultantUseCase = Depends(get_consultant_use_case)
):
    """
    Récupère la liste des consultants avec filtres optionnels.
    """
    return await use_case.get_consultants(
        company_id=company_id,
        skill_id=skill_id,
        availability=availability,
        skip=skip,
        limit=limit
    )

@router.get("/{consultant_id}", response_model=ConsultantResponse)
async def get_consultant(
    consultant_id: int,
    use_case: ConsultantUseCase = Depends(get_consultant_use_case)
):
    """
    Récupère un consultant par son ID.
    """
    consultant = await use_case.get_consultant(consultant_id)
    if not consultant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Consultant avec l'ID {consultant_id} non trouvé"
        )
    return consultant

@router.put("/{consultant_id}", response_model=ConsultantResponse)
async def update_consultant(
    consultant_id: int,
    consultant: ConsultantUpdate,
    use_case: ConsultantUseCase = Depends(get_consultant_use_case)
):
    """
    Met à jour un consultant existant.
    """
    updated_consultant = await use_case.update_consultant(consultant_id, consultant)
    if not updated_consultant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Consultant avec l'ID {consultant_id} non trouvé"
        )
    return updated_consultant

@router.delete("/{consultant_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_consultant(
    consultant_id: int,
    use_case: ConsultantUseCase = Depends(get_consultant_use_case)
):
    """
    Supprime un consultant.
    """
    success = await use_case.delete_consultant(consultant_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Consultant avec l'ID {consultant_id} non trouvé"
        )
    return None

@router.get("/{consultant_id}/skills", response_model=List[dict])
async def get_consultant_skills(
    consultant_id: int,
    use_case: ConsultantUseCase = Depends(get_consultant_use_case)
):
    """
    Récupère les compétences d'un consultant.
    """
    skills = await use_case.get_consultant_skills(consultant_id)
    if skills is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Consultant avec l'ID {consultant_id} non trouvé"
        )
    return skills

@router.post("/{consultant_id}/skills/{skill_id}")
async def add_skill_to_consultant(
    consultant_id: int,
    skill_id: int,
    level: int,
    use_case: ConsultantUseCase = Depends(get_consultant_use_case)
):
    """
    Ajoute une compétence à un consultant avec un niveau spécifié.
    """
    success = await use_case.add_skill_to_consultant(consultant_id, skill_id, level)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Consultant avec l'ID {consultant_id} ou compétence avec l'ID {skill_id} non trouvé"
        )
    return {"status": "success", "message": "Compétence ajoutée au consultant"}

@router.delete("/{consultant_id}/skills/{skill_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_skill_from_consultant(
    consultant_id: int,
    skill_id: int,
    use_case: ConsultantUseCase = Depends(get_consultant_use_case)
):
    """
    Supprime une compétence d'un consultant.
    """
    success = await use_case.remove_skill_from_consultant(consultant_id, skill_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Consultant avec l'ID {consultant_id} ou compétence avec l'ID {skill_id} non trouvé"
        )
    return None

@router.get("/{consultant_id}/availability", response_model=dict)
async def get_consultant_availability(
    consultant_id: int,
    use_case: ConsultantUseCase = Depends(get_consultant_use_case)
):
    """
    Récupère la disponibilité d'un consultant.
    """
    availability = await use_case.get_consultant_availability(consultant_id)
    if availability is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Consultant avec l'ID {consultant_id} non trouvé"
        )
    return availability

@router.put("/{consultant_id}/availability")
async def update_consultant_availability(
    consultant_id: int,
    availability_data: dict,
    use_case: ConsultantUseCase = Depends(get_consultant_use_case)
):
    """
    Met à jour la disponibilité d'un consultant.
    """
    success = await use_case.update_consultant_availability(consultant_id, availability_data)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Consultant avec l'ID {consultant_id} non trouvé"
        )
    return {"status": "success", "message": "Disponibilité du consultant mise à jour"}
