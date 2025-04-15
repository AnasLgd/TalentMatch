from typing import Dict, Any, List, Optional
import os
import json
import uuid
from enum import Enum
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form, BackgroundTasks
from sqlalchemy.orm import Session
from datetime import datetime
from pydantic import BaseModel

from app.core.use_cases.cv_analysis_use_case import CVAnalysisUseCase
from app.adapters.services.cv_analysis_service import BasicCVAnalysisService
from app.adapters.n8n.workflow_service import N8nWorkflowService
from app.core.use_cases.consultant_use_case import ConsultantUseCase
from app.adapters.repositories.consultant_repository import ConsultantRepository
from app.adapters.repositories.skill_repository import SkillRepository
from app.infrastructure.database.session import get_db
from app.infrastructure.storage.minio_client import MinioClient

# Models for API
class CvFileStatus(str, Enum):
    UPLOADED = "uploaded"
    ANALYZING = "analyzing"
    ANALYZED = "analyzed" 
    ERROR = "error"

class CvUploadResponse(BaseModel):
    fileId: int
    status: CvFileStatus
    message: Optional[str] = None

class CvAnalysisResult(BaseModel):
    fileId: int
    candidate: dict

router = APIRouter(
    prefix="/api/v1/cv-analysis",
    tags=["CV Analysis"]
)

# In-memory storage for development (would be DB in production)
cv_files = {}
cv_results = {}

@router.post("/upload", response_model=CvUploadResponse)
async def upload_cv(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Upload a CV file
    """
    # Validate file type
    if not file.filename.lower().endswith(('.pdf', '.docx', '.doc')):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Format de fichier non supporté. Seuls les formats PDF, DOCX et DOC sont acceptés."
        )
    
    try:
        content = await file.read()
        if len(content) == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Le fichier est vide ou corrompu."
            )
            
        # Generate a unique file ID
        file_id = len(cv_files) + 1
        
        # Store file metadata
        file_type = file.filename.split('.')[-1].lower()
        file_size = len(content) / 1024  # Size in KB
        
        cv_files[file_id] = {
            "id": file_id,
            "name": file.filename,
            "size": f"{file_size:.2f} KB",
            "type": file_type,
            "status": CvFileStatus.UPLOADED,
            "progress": 0,
            "content": content,  # Store content in memory (would use object storage in production)
            "upload_time": datetime.now().isoformat()
        }
        
        return CvUploadResponse(
            fileId=file_id,
            status=CvFileStatus.UPLOADED,
            message="CV téléchargé avec succès"
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors du téléchargement du CV: {str(e)}"
        )

@router.get("/files")
async def get_cv_files(db: Session = Depends(get_db)):
    """
    Get list of uploaded CV files
    """
    # Convert cv_files dict to a list of files with relevant fields only (omit content)
    files = []
    for file_id, file_data in cv_files.items():
        file_info = {k: v for k, v in file_data.items() if k != 'content'}
        
        # Check if there are analysis results for this file
        if file_id in cv_results:
            file_info['candidate'] = cv_results[file_id]['candidate']
            
        files.append(file_info)
    
    return files

@router.get("/files/{file_id}")
async def get_cv_file(file_id: int, db: Session = Depends(get_db)):
    """
    Get a specific CV file
    """
    if file_id not in cv_files:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"CV avec ID {file_id} non trouvé"
        )
    
    # Return file info without content
    file_info = {k: v for k, v in cv_files[file_id].items() if k != 'content'}
    
    # Check if there are analysis results for this file
    if file_id in cv_results:
        file_info['candidate'] = cv_results[file_id]['candidate']
        
    return file_info

@router.post("/analyze/{file_id}")
async def analyze_cv_by_id(file_id: int, db: Session = Depends(get_db)):
    """
    Analyze a previously uploaded CV
    """
    if file_id not in cv_files:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"CV avec ID {file_id} non trouvé"
        )
    
    file_data = cv_files[file_id]
    content = file_data['content']
    file_type = file_data['type']
    
    # Update status to analyzing
    cv_files[file_id]['status'] = CvFileStatus.ANALYZING
    cv_files[file_id]['progress'] = 25
    
    # Initialiser le service d'analyse de CV
    cv_analysis_service = BasicCVAnalysisService()
    
    # Initialiser le cas d'utilisation
    cv_analysis_use_case = CVAnalysisUseCase(cv_analysis_service)
    
    try:
        # Analyser le CV
        if file_type in ['pdf']:
            result = await cv_analysis_use_case.analyze_pdf(content)
        elif file_type in ['docx', 'doc']:
            result = await cv_analysis_use_case.analyze_docx(content)
        else:
            raise ValueError(f"Format de fichier non supporté: {file_type}")
        
        # Update status to analyzed
        cv_files[file_id]['status'] = CvFileStatus.ANALYZED
        cv_files[file_id]['progress'] = 100
        
        # Store analysis results
        cv_results[file_id] = {
            'fileId': file_id,
            'candidate': result
        }
        
        # Return updated file info
        return {
            **{k: v for k, v in cv_files[file_id].items() if k != 'content'},
            'candidate': result
        }
    except Exception as e:
        # Update status to error
        cv_files[file_id]['status'] = CvFileStatus.ERROR
        cv_files[file_id]['progress'] = 0
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de l'analyse du CV: {str(e)}"
        )

@router.get("/results/{file_id}", response_model=CvAnalysisResult)
async def get_cv_analysis_result(file_id: int, db: Session = Depends(get_db)):
    """
    Get analysis results for a CV
    """
    if file_id not in cv_results:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Résultats d'analyse pour le CV ID {file_id} non trouvés"
        )
    
    return cv_results[file_id]

@router.get("/status/{file_id}")
async def check_cv_status(file_id: int, db: Session = Depends(get_db)):
    """
    Check the status of a CV analysis
    """
    if file_id not in cv_files:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"CV avec ID {file_id} non trouvé"
        )
    
    return {"status": cv_files[file_id]['status']}

@router.delete("/files/{file_id}")
async def delete_cv_file(file_id: int, db: Session = Depends(get_db)):
    """
    Delete a CV file
    """
    if file_id not in cv_files:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"CV avec ID {file_id} non trouvé"
        )
    
    # Remove the file and its analysis results
    del cv_files[file_id]
    if file_id in cv_results:
        del cv_results[file_id]
    
    return {"message": f"CV avec ID {file_id} supprimé avec succès"}

@router.post("/upload-analyze", response_model=CvAnalysisResult)
async def upload_and_analyze_cv(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Upload and analyze a CV in one operation
    """
    # Validate file type
    if not file.filename.lower().endswith(('.pdf', '.docx', '.doc')):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Format de fichier non supporté. Seuls les formats PDF, DOCX et DOC sont acceptés."
        )
    
    try:
        content = await file.read()
        if len(content) == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Le fichier est vide ou corrompu."
            )
            
        # Generate a unique file ID
        file_id = len(cv_files) + 1
        
        # Store file metadata
        file_type = file.filename.split('.')[-1].lower()
        file_size = len(content) / 1024  # Size in KB
        
        cv_files[file_id] = {
            "id": file_id,
            "name": file.filename,
            "size": f"{file_size:.2f} KB",
            "type": file_type,
            "status": CvFileStatus.ANALYZING,
            "progress": 50,
            "content": content,  # Store content in memory (would use object storage in production)
            "upload_time": datetime.now().isoformat()
        }
        
        # Initialiser le service d'analyse de CV
        cv_analysis_service = BasicCVAnalysisService()
        
        # Initialiser le cas d'utilisation
        cv_analysis_use_case = CVAnalysisUseCase(cv_analysis_service)
        
        # Analyser le CV
        if file_type in ['pdf']:
            result = await cv_analysis_use_case.analyze_pdf(content)
        elif file_type in ['docx', 'doc']:
            result = await cv_analysis_use_case.analyze_docx(content)
        else:
            raise ValueError(f"Format de fichier non supporté: {file_type}")
        
        # Update status to analyzed
        cv_files[file_id]['status'] = CvFileStatus.ANALYZED
        cv_files[file_id]['progress'] = 100
        
        # Format candidate data for frontend
        candidate_data = {
            "name": result.get("name", ""),
            "email": result.get("email", ""),
            "phone": result.get("phone", ""),
            "skills": result.get("skills", []),
            "experience": result.get("experience", []),
            "education": result.get("education", [])
        }
        
        # Store analysis results
        cv_results[file_id] = {
            'fileId': file_id,
            'candidate': candidate_data
        }
        
        return CvAnalysisResult(
            fileId=file_id,
            candidate=candidate_data
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors du téléchargement et de l'analyse du CV: {str(e)}"
        )

@router.post("/create-consultant")
async def create_consultant_from_cv(
    data: dict,
    db: Session = Depends(get_db)
):
    """
    Create a consultant from an analyzed CV
    """
    file_id = data.get("file_id")
    company_id = data.get("company_id")
    
    if not file_id or not company_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Les paramètres file_id et company_id sont requis"
        )
    
    if file_id not in cv_results:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Résultats d'analyse pour le CV ID {file_id} non trouvés"
        )
    
    try:
        # Get analysis results
        analysis_result = cv_results[file_id]
        candidate_data = analysis_result['candidate']
        
        # Create a consultant from the candidate data
        consultant_repo = ConsultantRepository(db)
        skill_repo = SkillRepository(db)
        consultant_use_case = ConsultantUseCase(consultant_repo, skill_repo)
        
        # Generate a random user_id for demonstration (in production, would use actual user)
        user_id = 1  # Default to a demo user
        
        # Create consultant object
        consultant_data = {
            "user_id": user_id,
            "company_id": company_id,
            "title": "Consultant",  # Default title
            "experience_years": 0,  # Default experience
            "availability_status": "available",  # Default status
            "bio": "",  # Could extract from CV in a more advanced implementation
            "skills": candidate_data.get("skills", [])
        }
        
        # Create the consultant
        consultant_id = await consultant_use_case.create_consultant(consultant_data)
        
        return {"consultant_id": consultant_id}
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la création du consultant: {str(e)}"
        )

# Keep existing endpoints
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
