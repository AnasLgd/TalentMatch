from typing import Dict, Any, List, Optional
import os
import json
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session

from app.core.use_cases.collaboration_use_case import CollaborationUseCase
from app.adapters.n8n.workflow_service import N8nWorkflowService
from app.adapters.repositories.company_repository import SQLAlchemyCompanyRepository
from app.adapters.repositories.collaboration_repository import SQLAlchemyCollaborationRepository
from app.infrastructure.database.session import get_db
from app.core.entities.collaboration import CollaborationCreate, CollaborationUpdate

router = APIRouter(
    prefix="/api/v1/collaborations",
    tags=["Collaborations"]
)

@router.post("/")
async def create_collaboration(
    collaboration: CollaborationCreate,
    db: Session = Depends(get_db)
):
    """
    Crée une nouvelle collaboration entre deux entreprises
    """
    # Initialiser les repositories
    company_repository = SQLAlchemyCompanyRepository(db)
    collaboration_repository = SQLAlchemyCollaborationRepository(db)
    
    # Initialiser le service n8n
    n8n_service = N8nWorkflowService()
    
    # Initialiser le cas d'utilisation
    collaboration_use_case = CollaborationUseCase(
        collaboration_repository=collaboration_repository,
        company_repository=company_repository,
        n8n_service=n8n_service
    )
    
    try:
        # Créer la collaboration
        result = await collaboration_use_case.create_collaboration(collaboration)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la création de la collaboration: {str(e)}"
        )

@router.get("/")
async def get_collaborations(
    company_id: Optional[int] = None,
    status_filter: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Récupère les collaborations, avec filtrage optionnel par entreprise et statut
    """
    # Initialiser les repositories
    company_repository = SQLAlchemyCompanyRepository(db)
    collaboration_repository = SQLAlchemyCollaborationRepository(db)
    
    # Initialiser le service n8n
    n8n_service = N8nWorkflowService()
    
    # Initialiser le cas d'utilisation
    collaboration_use_case = CollaborationUseCase(
        collaboration_repository=collaboration_repository,
        company_repository=company_repository,
        n8n_service=n8n_service
    )
    
    try:
        # Récupérer les collaborations
        if company_id:
            if status_filter:
                collaborations = await collaboration_use_case.get_company_collaborations_by_status(company_id, status_filter)
            else:
                collaborations = await collaboration_use_case.get_company_collaborations(company_id)
        else:
            if status_filter:
                collaborations = await collaboration_use_case.get_collaborations_by_status(status_filter)
            else:
                collaborations = await collaboration_use_case.get_all_collaborations()
        
        return collaborations
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la récupération des collaborations: {str(e)}"
        )

@router.get("/{collaboration_id}")
async def get_collaboration(
    collaboration_id: int,
    db: Session = Depends(get_db)
):
    """
    Récupère une collaboration par son ID
    """
    # Initialiser les repositories
    company_repository = SQLAlchemyCompanyRepository(db)
    collaboration_repository = SQLAlchemyCollaborationRepository(db)
    
    # Initialiser le service n8n
    n8n_service = N8nWorkflowService()
    
    # Initialiser le cas d'utilisation
    collaboration_use_case = CollaborationUseCase(
        collaboration_repository=collaboration_repository,
        company_repository=company_repository,
        n8n_service=n8n_service
    )
    
    try:
        # Récupérer la collaboration
        collaboration = await collaboration_use_case.get_collaboration(collaboration_id)
        
        if not collaboration:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Collaboration avec l'ID {collaboration_id} non trouvée"
            )
        
        return collaboration
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la récupération de la collaboration: {str(e)}"
        )

@router.put("/{collaboration_id}")
async def update_collaboration(
    collaboration_id: int,
    collaboration: CollaborationUpdate,
    db: Session = Depends(get_db)
):
    """
    Met à jour une collaboration existante
    """
    # Initialiser les repositories
    company_repository = SQLAlchemyCompanyRepository(db)
    collaboration_repository = SQLAlchemyCollaborationRepository(db)
    
    # Initialiser le service n8n
    n8n_service = N8nWorkflowService()
    
    # Initialiser le cas d'utilisation
    collaboration_use_case = CollaborationUseCase(
        collaboration_repository=collaboration_repository,
        company_repository=company_repository,
        n8n_service=n8n_service
    )
    
    try:
        # Mettre à jour la collaboration
        updated_collaboration = await collaboration_use_case.update_collaboration(collaboration_id, collaboration)
        
        if not updated_collaboration:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Collaboration avec l'ID {collaboration_id} non trouvée"
            )
        
        return updated_collaboration
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la mise à jour de la collaboration: {str(e)}"
        )

@router.delete("/{collaboration_id}")
async def delete_collaboration(
    collaboration_id: int,
    db: Session = Depends(get_db)
):
    """
    Supprime une collaboration
    """
    # Initialiser les repositories
    company_repository = SQLAlchemyCompanyRepository(db)
    collaboration_repository = SQLAlchemyCollaborationRepository(db)
    
    # Initialiser le service n8n
    n8n_service = N8nWorkflowService()
    
    # Initialiser le cas d'utilisation
    collaboration_use_case = CollaborationUseCase(
        collaboration_repository=collaboration_repository,
        company_repository=company_repository,
        n8n_service=n8n_service
    )
    
    try:
        # Supprimer la collaboration
        success = await collaboration_use_case.delete_collaboration(collaboration_id)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Collaboration avec l'ID {collaboration_id} non trouvée"
            )
        
        return {"message": "Collaboration supprimée avec succès"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la suppression de la collaboration: {str(e)}"
        )

@router.post("/{collaboration_id}/process-with-n8n")
async def process_collaboration_with_n8n(
    collaboration_id: int,
    db: Session = Depends(get_db)
):
    """
    Traite une collaboration avec n8n
    """
    # Initialiser les repositories
    company_repository = SQLAlchemyCompanyRepository(db)
    collaboration_repository = SQLAlchemyCollaborationRepository(db)
    
    # Initialiser le service n8n
    n8n_service = N8nWorkflowService()
    
    # Initialiser le cas d'utilisation
    collaboration_use_case = CollaborationUseCase(
        collaboration_repository=collaboration_repository,
        company_repository=company_repository,
        n8n_service=n8n_service
    )
    
    try:
        # Récupérer la collaboration
        collaboration = await collaboration_use_case.get_collaboration(collaboration_id)
        
        if not collaboration:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Collaboration avec l'ID {collaboration_id} non trouvée"
            )
        
        # Traiter la collaboration avec n8n
        result = await n8n_service.initiate_collaboration(
            collaboration.initiator_company_id,
            collaboration.partner_company_id,
            {
                "status": collaboration.status,
                "terms": collaboration.terms,
                "start_date": str(collaboration.start_date) if collaboration.start_date else None,
                "end_date": str(collaboration.end_date) if collaboration.end_date else None
            }
        )
        
        return {
            "collaboration": collaboration,
            "n8n_result": result
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors du traitement de la collaboration avec n8n: {str(e)}"
        )
