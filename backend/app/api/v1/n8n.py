from typing import Dict, Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form, BackgroundTasks
from sqlalchemy.orm import Session
import uuid
from datetime import datetime

from app.core.interfaces.n8n_integration_service import N8nIntegrationService
from app.adapters.services.agent_ia_maison_service import AgentIAMaisonService
from app.infrastructure.database.session import get_db
from app.infrastructure.database.models import WorkflowExecution, WorkflowStatus
from app.core.interfaces.rag_service import RAGService

router = APIRouter(
    prefix="/api/v1/n8n",
    tags=["n8n Integration"]
)

# Dépendance pour obtenir le service n8n
async def get_n8n_service():
    # Cette fonction devrait être implémentée pour retourner une instance du service n8n
    # Pour l'instant, nous utilisons une implémentation fictive
    from app.adapters.n8n.workflow_service import N8nWorkflowService
    return N8nWorkflowService()

# Dépendance pour obtenir le service d'agent IA maison
async def get_agent_ia_service(
    n8n_service: N8nIntegrationService = Depends(get_n8n_service),
    rag_service: RAGService = Depends(lambda: RAGService())
):
    return AgentIAMaisonService(n8n_service, rag_service)

@router.get("/status")
async def get_n8n_status(
    n8n_service: N8nIntegrationService = Depends(get_n8n_service),
    db: Session = Depends(get_db)
):
    """
    Vérifie le statut de l'intégration n8n
    """
    try:
        status = await n8n_service.initialize_workflow_engine()
        return {
            "status": "connected" if status else "disconnected",
            "message": "n8n est correctement configuré et connecté" if status else "Impossible de se connecter à n8n"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la vérification du statut n8n: {str(e)}"
        )

@router.get("/workflows")
async def get_workflows(
    n8n_service: N8nIntegrationService = Depends(get_n8n_service),
    db: Session = Depends(get_db)
):
    """
    Récupère la liste des workflows n8n disponibles
    """
    try:
        # Cette méthode devrait être implémentée dans le service n8n
        workflows = await n8n_service.get_workflows()
        return workflows
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la récupération des workflows: {str(e)}"
        )

@router.post("/workflows")
async def create_workflow(
    workflow_definition: Dict[str, Any],
    n8n_service: N8nIntegrationService = Depends(get_n8n_service),
    db: Session = Depends(get_db)
):
    """
    Crée un nouveau workflow n8n
    """
    try:
        if "name" not in workflow_definition:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Le workflow doit avoir un nom"
            )
        
        workflow_id = await n8n_service.register_workflow(
            workflow_definition["name"],
            workflow_definition
        )
        
        return {
            "workflow_id": workflow_id,
            "message": "Workflow créé avec succès"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la création du workflow: {str(e)}"
        )

@router.post("/workflows/{workflow_id}/execute")
async def execute_workflow(
    workflow_id: str,
    input_data: Dict[str, Any],
    background_tasks: BackgroundTasks,
    n8n_service: N8nIntegrationService = Depends(get_n8n_service),
    db: Session = Depends(get_db)
):
    """
    Exécute un workflow n8n
    """
    try:
        # Créer un enregistrement d'exécution de workflow
        workflow_execution = WorkflowExecution(
            workflow_id=workflow_id,
            workflow_name=input_data.get("workflow_name", "Unknown"),
            status=WorkflowStatus.PENDING,
            input_data=input_data,
            resume_id=input_data.get("resume_id"),
            match_id=input_data.get("match_id"),
            portfolio_id=input_data.get("portfolio_id")
        )
        
        db.add(workflow_execution)
        db.commit()
        db.refresh(workflow_execution)
        
        # Exécuter le workflow en arrière-plan
        background_tasks.add_task(
            execute_workflow_background,
            workflow_id,
            input_data,
            workflow_execution.id,
            n8n_service,
            db
        )
        
        return {
            "execution_id": workflow_execution.id,
            "status": "pending",
            "message": "Exécution du workflow démarrée"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de l'exécution du workflow: {str(e)}"
        )

async def execute_workflow_background(
    workflow_id: str,
    input_data: Dict[str, Any],
    execution_id: int,
    n8n_service: N8nIntegrationService,
    db: Session
):
    """
    Exécute un workflow n8n en arrière-plan
    """
    try:
        # Mettre à jour le statut de l'exécution
        execution = db.query(WorkflowExecution).filter(WorkflowExecution.id == execution_id).first()
        if not execution:
            return
        
        execution.status = WorkflowStatus.RUNNING
        db.commit()
        
        # Exécuter le workflow
        result = await n8n_service.execute_workflow(workflow_id, input_data)
        
        # Mettre à jour l'exécution avec le résultat
        execution.status = WorkflowStatus.COMPLETED
        execution.output_data = result
        execution.completed_at = datetime.now()
        db.commit()
    except Exception as e:
        # En cas d'erreur, mettre à jour le statut
        execution = db.query(WorkflowExecution).filter(WorkflowExecution.id == execution_id).first()
        if execution:
            execution.status = WorkflowStatus.FAILED
            execution.error_message = str(e)
            execution.completed_at = datetime.now()
            db.commit()

@router.get("/executions")
async def get_workflow_executions(
    workflow_id: Optional[str] = None,
    status: Optional[str] = None,
    limit: int = 100,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    """
    Récupère la liste des exécutions de workflows
    """
    try:
        query = db.query(WorkflowExecution)
        
        if workflow_id:
            query = query.filter(WorkflowExecution.workflow_id == workflow_id)
        
        if status:
            query = query.filter(WorkflowExecution.status == status)
        
        total = query.count()
        executions = query.order_by(WorkflowExecution.created_at.desc()).offset(offset).limit(limit).all()
        
        return {
            "total": total,
            "offset": offset,
            "limit": limit,
            "executions": [
                {
                    "id": execution.id,
                    "workflow_id": execution.workflow_id,
                    "workflow_name": execution.workflow_name,
                    "status": execution.status.value,
                    "started_at": execution.started_at,
                    "completed_at": execution.completed_at,
                    "resume_id": execution.resume_id,
                    "match_id": execution.match_id,
                    "portfolio_id": execution.portfolio_id
                }
                for execution in executions
            ]
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la récupération des exécutions: {str(e)}"
        )

@router.get("/executions/{execution_id}")
async def get_workflow_execution(
    execution_id: int,
    db: Session = Depends(get_db)
):
    """
    Récupère les détails d'une exécution de workflow
    """
    try:
        execution = db.query(WorkflowExecution).filter(WorkflowExecution.id == execution_id).first()
        
        if not execution:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Exécution avec l'ID {execution_id} non trouvée"
            )
        
        return {
            "id": execution.id,
            "workflow_id": execution.workflow_id,
            "workflow_name": execution.workflow_name,
            "status": execution.status.value,
            "input_data": execution.input_data,
            "output_data": execution.output_data,
            "error_message": execution.error_message,
            "started_at": execution.started_at,
            "completed_at": execution.completed_at,
            "resume_id": execution.resume_id,
            "match_id": execution.match_id,
            "portfolio_id": execution.portfolio_id
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la récupération de l'exécution: {str(e)}"
        )

@router.post("/cv-analysis")
async def analyze_cv(
    file: UploadFile = File(...),
    background_tasks: BackgroundTasks = BackgroundTasks(),
    agent_service: AgentIAMaisonService = Depends(get_agent_ia_service),
    db: Session = Depends(get_db)
):
    """
    Analyse un CV avec l'agent IA maison
    """
    try:
        # Vérifier le type de fichier
        if not file.filename.lower().endswith(('.pdf', '.docx', '.doc', '.txt')):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Format de fichier non supporté. Seuls les formats PDF, DOCX, DOC et TXT sont acceptés."
            )
        
        # Lire le contenu du fichier
        content = await file.read()
        
        # Créer un ID unique pour cette analyse
        analysis_id = str(uuid.uuid4())
        
        # Lancer l'analyse en arrière-plan
        background_tasks.add_task(
            analyze_cv_background,
            content,
            file.filename,
            analysis_id,
            agent_service,
            db
        )
        
        return {
            "analysis_id": analysis_id,
            "status": "processing",
            "message": "Analyse du CV démarrée"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de l'analyse du CV: {str(e)}"
        )

async def analyze_cv_background(
    file_content: bytes,
    file_name: str,
    analysis_id: str,
    agent_service: AgentIAMaisonService,
    db: Session
):
    """
    Analyse un CV en arrière-plan
    """
    try:
        # Extraire les données du CV
        cv_data = await agent_service.extract_cv_data(file_content, file_name)
        
        # Analyser les compétences
        skills_analysis = await agent_service.analyze_skills(cv_data)
        
        # TODO: Sauvegarder les résultats dans la base de données
        
        # Pour l'instant, nous ne faisons rien avec les résultats
        pass
    except Exception as e:
        # Gérer les erreurs
        print(f"Erreur lors de l'analyse du CV: {str(e)}")

@router.post("/match")
async def match_consultant_tender(
    match_request: Dict[str, Any],
    background_tasks: BackgroundTasks = BackgroundTasks(),
    agent_service: AgentIAMaisonService = Depends(get_agent_ia_service),
    db: Session = Depends(get_db)
):
    """
    Effectue le matching entre un consultant et un appel d'offres
    """
    try:
        # Vérifier les données requises
        if "consultant_id" not in match_request or "tender_id" not in match_request:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Les IDs du consultant et de l'appel d'offres sont requis"
            )
        
        # Créer un ID unique pour ce matching
        match_id = str(uuid.uuid4())
        
        # Lancer le matching en arrière-plan
        background_tasks.add_task(
            match_background,
            match_request["consultant_id"],
            match_request["tender_id"],
            match_id,
            agent_service,
            db
        )
        
        return {
            "match_id": match_id,
            "status": "processing",
            "message": "Matching démarré"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors du matching: {str(e)}"
        )

async def match_background(
    consultant_id: int,
    tender_id: int,
    match_id: str,
    agent_service: AgentIAMaisonService,
    db: Session
):
    """
    Effectue le matching en arrière-plan
    """
    try:
        # TODO: Récupérer les données du consultant et de l'appel d'offres depuis la base de données
        
        # Pour l'instant, nous utilisons des données fictives
        consultant_data = {
            "id": consultant_id,
            "skills": [
                {"name": "Python", "level": "expert", "years_experience": 5},
                {"name": "JavaScript", "level": "intermediate", "years_experience": 3}
            ]
        }
        
        tender_data = {
            "id": tender_id,
            "skills": [
                {"name": "Python", "importance": "required"},
                {"name": "JavaScript", "importance": "preferred"}
            ]
        }
        
        # Effectuer le matching
        match_result = await agent_service.match_consultant_with_tender(consultant_data, tender_data)
        
        # TODO: Sauvegarder les résultats dans la base de données
        
        # Pour l'instant, nous ne faisons rien avec les résultats
        pass
    except Exception as e:
        # Gérer les erreurs
        print(f"Erreur lors du matching: {str(e)}")

@router.post("/portfolio")
async def generate_portfolio(
    portfolio_request: Dict[str, Any],
    background_tasks: BackgroundTasks = BackgroundTasks(),
    agent_service: AgentIAMaisonService = Depends(get_agent_ia_service),
    db: Session = Depends(get_db)
):
    """
    Génère un portfolio pour un consultant en fonction d'un appel d'offres
    """
    try:
        # Vérifier les données requises
        if "consultant_id" not in portfolio_request or "tender_id" not in portfolio_request:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Les IDs du consultant et de l'appel d'offres sont requis"
            )
        
        # Créer un ID unique pour cette génération
        portfolio_id = str(uuid.uuid4())
        
        # Lancer la génération en arrière-plan
        background_tasks.add_task(
            generate_portfolio_background,
            portfolio_request["consultant_id"],
            portfolio_request["tender_id"],
            portfolio_id,
            agent_service,
            db
        )
        
        return {
            "portfolio_id": portfolio_id,
            "status": "processing",
            "message": "Génération du portfolio démarrée"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la génération du portfolio: {str(e)}"
        )

async def generate_portfolio_background(
    consultant_id: int,
    tender_id: int,
    portfolio_id: str,
    agent_service: AgentIAMaisonService,
    db: Session
):
    """
    Génère un portfolio en arrière-plan
    """
    try:
        # TODO: Récupérer les données du consultant et de l'appel d'offres depuis la base de données
        
        # Pour l'instant, nous utilisons des données fictives
        consultant_data = {
            "id": consultant_id,
            "first_name": "John",
            "last_name": "Doe",
            "title": "Développeur Full Stack",
            "skills": [
                {"name": "Python", "level": "expert", "years_experience": 5},
                {"name": "JavaScript", "level": "intermediate", "years_experience": 3}
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
            "title": "Développeur Full Stack pour projet e-commerce",
            "skills": [
                {"name": "Python", "importance": "required"},
                {"name": "JavaScript", "importance": "preferred"}
            ]
        }
        
        # Générer le portfolio
        portfolio_result = await agent_service.generate_consultant_portfolio(consultant_data, tender_data)
        
        # TODO: Sauvegarder les résultats dans la base de données
        
        # Pour l'instant, nous ne faisons rien avec les résultats
        pass
    except Exception as e:
        # Gérer les erreurs
        print(f"Erreur lors de la génération du portfolio: {str(e)}")

@router.post("/initialize-workflows")
async def initialize_workflows(
    agent_service: AgentIAMaisonService = Depends(get_agent_ia_service),
    db: Session = Depends(get_db)
):
    """
    Initialise les workflows n8n nécessaires pour les agents IA maison
    """
    try:
        # Initialiser les workflows
        created_workflows = await agent_service.initialize_workflows()
        
        return {
            "created_workflows": created_workflows,
            "message": "Workflows initialisés avec succès"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de l'initialisation des workflows: {str(e)}"
        )
