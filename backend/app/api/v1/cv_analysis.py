from typing import Dict, Any, List, Optional
import os
import json
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session

from app.core.use_cases.cv_analysis_use_case import CVAnalysisUseCase
from app.adapters.services.cv_analysis_service import BasicCVAnalysisService
from app.adapters.n8n.workflow_service import N8nWorkflowService
from app.infrastructure.database.session import get_db

router = APIRouter(
    prefix="/api/v1/cv",
    tags=["CV Analysis"]
)

@router.post("/analyze")
async def analyze_cv(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Analyse un CV et extrait les informations pertinentes
    """
    # Vérifier le type de fichier
    if not file.filename.lower().endswith(('.pdf', '.docx')):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Format de fichier non supporté. Seuls les formats PDF et DOCX sont acceptés."
        )
    
    # Initialiser le service d'analyse de CV
    cv_analysis_service = BasicCVAnalysisService()
    
    # Initialiser le cas d'utilisation
    cv_analysis_use_case = CVAnalysisUseCase(cv_analysis_service)
    
    try:
        # Lire le contenu du fichier
        content = await file.read()
        
        # Analyser le CV
        if file.filename.lower().endswith('.pdf'):
            result = await cv_analysis_use_case.analyze_pdf(content)
        else:  # .docx
            result = await cv_analysis_use_case.analyze_docx(content)
        
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de l'analyse du CV: {str(e)}"
        )

@router.post("/analyze-with-n8n")
async def analyze_cv_with_n8n(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Analyse un CV avec n8n et extrait les informations pertinentes
    """
    # Vérifier le type de fichier
    if not file.filename.lower().endswith(('.pdf', '.docx')):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Format de fichier non supporté. Seuls les formats PDF et DOCX sont acceptés."
        )
    
    # Initialiser le service d'analyse de CV
    cv_analysis_service = BasicCVAnalysisService()
    
    # Initialiser le service n8n
    n8n_service = N8nWorkflowService()
    
    # Initialiser le cas d'utilisation
    cv_analysis_use_case = CVAnalysisUseCase(cv_analysis_service)
    
    try:
        # Lire le contenu du fichier
        content = await file.read()
        
        # Analyser le CV localement d'abord
        if file.filename.lower().endswith('.pdf'):
            result = await cv_analysis_use_case.analyze_pdf(content)
        else:  # .docx
            result = await cv_analysis_use_case.analyze_docx(content)
        
        # Préparer les données pour n8n
        n8n_data = await cv_analysis_service.prepare_n8n_workflow_data(result)
        
        # Traiter avec n8n
        n8n_result = await n8n_service.process_cv(n8n_data)
        
        # Combiner les résultats
        final_result = {
            **result,
            "n8n_processing": n8n_result
        }
        
        return final_result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de l'analyse du CV avec n8n: {str(e)}"
        )

@router.post("/generate-portfolio/{consultant_id}/{tender_id}")
async def generate_portfolio(
    consultant_id: int,
    tender_id: int,
    db: Session = Depends(get_db)
):
    """
    Génère un dossier de compétences pour un consultant en fonction d'un appel d'offres
    """
    # Initialiser le service d'analyse de CV
    cv_analysis_service = BasicCVAnalysisService()
    
    # Initialiser le cas d'utilisation
    cv_analysis_use_case = CVAnalysisUseCase(cv_analysis_service)
    
    try:
        # Récupérer les données du consultant et de l'appel d'offres
        # Dans une implémentation réelle, ces données seraient récupérées depuis la base de données
        consultant_data = {
            "id": consultant_id,
            "name": "John Doe",
            "title": "Développeur Full Stack",
            "experience_years": 5,
            "bio": "Développeur passionné avec une expertise en JavaScript et Python.",
            "skills": [
                {
                    "name": "JavaScript",
                    "category": "programming_language",
                    "proficiency_level": "expert",
                    "years_experience": 5
                },
                {
                    "name": "Python",
                    "category": "programming_language",
                    "proficiency_level": "advanced",
                    "years_experience": 3
                },
                {
                    "name": "React",
                    "category": "framework",
                    "proficiency_level": "expert",
                    "years_experience": 4
                }
            ],
            "experiences": [
                {
                    "title": "Développeur Full Stack",
                    "company": "Tech Solutions",
                    "start_date": "Janvier 2020",
                    "end_date": "Présent",
                    "description": "Développement d'applications web avec React et Node.js."
                }
            ],
            "education": [
                {
                    "degree": "Master en Informatique",
                    "institution": "Université de Paris",
                    "year": 2019
                }
            ]
        }
        
        tender_data = {
            "id": tender_id,
            "title": "Développeur React",
            "description": "Nous recherchons un développeur React expérimenté pour un projet de 6 mois.",
            "skills": [
                {
                    "name": "React",
                    "importance": "required"
                },
                {
                    "name": "JavaScript",
                    "importance": "required"
                },
                {
                    "name": "TypeScript",
                    "importance": "preferred"
                }
            ]
        }
        
        # Générer le dossier de compétences
        portfolio = await cv_analysis_use_case.generate_portfolio(consultant_data, tender_data)
        
        return {"portfolio": portfolio}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la génération du dossier de compétences: {str(e)}"
        )

@router.get("/n8n/workflows")
async def get_n8n_workflows():
    """
    Récupère la liste des workflows n8n disponibles
    """
    n8n_service = N8nWorkflowService()
    
    try:
        workflows = await n8n_service.get_workflows()
        return workflows
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la récupération des workflows n8n: {str(e)}"
        )

@router.post("/n8n/execute/{workflow_id}")
async def execute_n8n_workflow(
    workflow_id: str,
    data: Dict[str, Any]
):
    """
    Exécute un workflow n8n avec les données fournies
    """
    n8n_service = N8nWorkflowService()
    
    try:
        result = await n8n_service.execute_workflow(workflow_id, data)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de l'exécution du workflow n8n: {str(e)}"
        )
