from typing import Dict, Any, List, Optional
import os
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.use_cases.match_use_case import MatchUseCase
from app.adapters.n8n.workflow_service import N8nWorkflowService
from app.adapters.repositories.consultant_repository import SQLAlchemyConsultantRepository
from app.adapters.repositories.tender_repository import SQLAlchemyTenderRepository
from app.adapters.repositories.match_repository import SQLAlchemyMatchRepository
from app.infrastructure.database.session import get_db
from app.core.entities.match import MatchCreate, MatchUpdate

router = APIRouter(
    prefix="/api/v1/matches",
    tags=["Matching"]
)

@router.post("/find-for-consultant/{consultant_id}")
async def find_matches_for_consultant(
    consultant_id: int,
    db: Session = Depends(get_db)
):
    """
    Trouve les appels d'offres qui correspondent à un consultant en utilisant n8n
    """
    # Initialiser les repositories
    consultant_repository = SQLAlchemyConsultantRepository(db)
    tender_repository = SQLAlchemyTenderRepository(db)
    match_repository = SQLAlchemyMatchRepository(db)
    
    # Initialiser le service n8n
    n8n_service = N8nWorkflowService()
    
    # Initialiser le cas d'utilisation
    match_use_case = MatchUseCase(
        match_repository=match_repository,
        consultant_repository=consultant_repository,
        tender_repository=tender_repository,
        n8n_service=n8n_service
    )
    
    try:
        # Vérifier que le consultant existe
        consultant = await consultant_repository.get_by_id(consultant_id)
        if not consultant:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Consultant avec l'ID {consultant_id} non trouvé"
            )
        
        # Trouver les matchs via n8n
        matches = await n8n_service.match_consultant_with_tenders(consultant_id)
        
        # Créer les matchs en base de données
        created_matches = []
        for match_data in matches:
            match_create = MatchCreate(
                consultant_id=consultant_id,
                tender_id=match_data["tender_id"],
                match_score=match_data["score"],
                status="pending",
                notes=match_data.get("notes", "")
            )
            created_match = await match_use_case.create_match(match_create)
            created_matches.append(created_match)
        
        return created_matches
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la recherche de matchs pour le consultant: {str(e)}"
        )

@router.post("/find-for-tender/{tender_id}")
async def find_matches_for_tender(
    tender_id: int,
    db: Session = Depends(get_db)
):
    """
    Trouve les consultants qui correspondent à un appel d'offres en utilisant n8n
    """
    # Initialiser les repositories
    consultant_repository = SQLAlchemyConsultantRepository(db)
    tender_repository = SQLAlchemyTenderRepository(db)
    match_repository = SQLAlchemyMatchRepository(db)
    
    # Initialiser le service n8n
    n8n_service = N8nWorkflowService()
    
    # Initialiser le cas d'utilisation
    match_use_case = MatchUseCase(
        match_repository=match_repository,
        consultant_repository=consultant_repository,
        tender_repository=tender_repository,
        n8n_service=n8n_service
    )
    
    try:
        # Vérifier que l'appel d'offres existe
        tender = await tender_repository.get_by_id(tender_id)
        if not tender:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Appel d'offres avec l'ID {tender_id} non trouvé"
            )
        
        # Trouver les matchs via n8n
        matches = await n8n_service.find_consultants_for_tender(tender_id)
        
        # Créer les matchs en base de données
        created_matches = []
        for match_data in matches:
            match_create = MatchCreate(
                consultant_id=match_data["consultant_id"],
                tender_id=tender_id,
                match_score=match_data["score"],
                status="pending",
                notes=match_data.get("notes", "")
            )
            created_match = await match_use_case.create_match(match_create)
            created_matches.append(created_match)
        
        return created_matches
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la recherche de matchs pour l'appel d'offres: {str(e)}"
        )

@router.get("/")
async def get_matches(
    consultant_id: Optional[int] = None,
    tender_id: Optional[int] = None,
    status_filter: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Récupère les matchs, avec filtrage optionnel par consultant, appel d'offres et statut
    """
    # Initialiser les repositories
    consultant_repository = SQLAlchemyConsultantRepository(db)
    tender_repository = SQLAlchemyTenderRepository(db)
    match_repository = SQLAlchemyMatchRepository(db)
    
    # Initialiser le service n8n
    n8n_service = N8nWorkflowService()
    
    # Initialiser le cas d'utilisation
    match_use_case = MatchUseCase(
        match_repository=match_repository,
        consultant_repository=consultant_repository,
        tender_repository=tender_repository,
        n8n_service=n8n_service
    )
    
    try:
        # Récupérer les matchs selon les filtres
        if consultant_id:
            matches = await match_repository.get_by_consultant_id(consultant_id)
        elif tender_id:
            matches = await match_repository.get_by_tender_id(tender_id)
        elif status_filter:
            matches = await match_repository.get_by_status(status_filter)
        else:
            matches = await match_repository.get_all()
        
        return matches
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la récupération des matchs: {str(e)}"
        )

@router.get("/{match_id}")
async def get_match(
    match_id: int,
    db: Session = Depends(get_db)
):
    """
    Récupère un match par son ID
    """
    # Initialiser les repositories
    match_repository = SQLAlchemyMatchRepository(db)
    
    try:
        # Récupérer le match
        match = await match_repository.get_by_id(match_id)
        
        if not match:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Match avec l'ID {match_id} non trouvé"
            )
        
        return match
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la récupération du match: {str(e)}"
        )

@router.put("/{match_id}")
async def update_match(
    match_id: int,
    match: MatchUpdate,
    db: Session = Depends(get_db)
):
    """
    Met à jour un match existant
    """
    # Initialiser les repositories
    consultant_repository = SQLAlchemyConsultantRepository(db)
    tender_repository = SQLAlchemyTenderRepository(db)
    match_repository = SQLAlchemyMatchRepository(db)
    
    # Initialiser le service n8n
    n8n_service = N8nWorkflowService()
    
    # Initialiser le cas d'utilisation
    match_use_case = MatchUseCase(
        match_repository=match_repository,
        consultant_repository=consultant_repository,
        tender_repository=tender_repository,
        n8n_service=n8n_service
    )
    
    try:
        # Mettre à jour le match
        updated_match = await match_use_case.update_match(match_id, match)
        
        if not updated_match:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Match avec l'ID {match_id} non trouvé"
            )
        
        return updated_match
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la mise à jour du match: {str(e)}"
        )

@router.delete("/{match_id}")
async def delete_match(
    match_id: int,
    db: Session = Depends(get_db)
):
    """
    Supprime un match
    """
    # Initialiser les repositories
    match_repository = SQLAlchemyMatchRepository(db)
    
    try:
        # Supprimer le match
        success = await match_repository.delete(match_id)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Match avec l'ID {match_id} non trouvé"
            )
        
        return {"message": "Match supprimé avec succès"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la suppression du match: {str(e)}"
        )
