from typing import Dict, Any, List, Optional
import os
import json
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session

from app.core.interfaces.rag_service import RAGService
from app.infrastructure.database.session import get_db

router = APIRouter(
    prefix="/api/v1/rag",
    tags=["RAG Agents"]
)

@router.post("/index-document")
async def index_document(
    file: UploadFile = File(...),
    document_type: str = Form(...),
    metadata: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    """
    Indexe un document dans la base de connaissances pour l'approche RAG
    
    Args:
        file: Fichier à indexer (PDF, DOCX, TXT)
        document_type: Type de document (cv, tender, portfolio, etc.)
        metadata: Métadonnées du document au format JSON
    """
    # Vérifier le type de fichier
    if not file.filename.lower().endswith(('.pdf', '.docx', '.txt')):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Format de fichier non supporté. Seuls les formats PDF, DOCX et TXT sont acceptés."
        )
    
    # Initialiser le service RAG
    rag_service = RAGService()
    
    try:
        # Lire le contenu du fichier
        content = await file.read()
        
        # Convertir les métadonnées en dictionnaire
        metadata_dict = {}
        if metadata:
            try:
                metadata_dict = json.loads(metadata)
            except json.JSONDecodeError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Format de métadonnées invalide. Les métadonnées doivent être au format JSON."
                )
        
        # Indexer le document
        document_id = await rag_service.index_document(content, file.filename, document_type, metadata_dict)
        
        return {
            "document_id": document_id,
            "message": "Document indexé avec succès"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de l'indexation du document: {str(e)}"
        )

@router.post("/query")
async def query_rag(
    query: Dict[str, Any],
    db: Session = Depends(get_db)
):
    """
    Interroge la base de connaissances avec l'approche RAG
    
    Args:
        query: Requête contenant le texte de la question et les filtres optionnels
    """
    # Initialiser le service RAG
    rag_service = RAGService()
    
    try:
        # Vérifier que la requête contient le texte de la question
        if "text" not in query or not query["text"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La requête doit contenir le texte de la question."
            )
        
        # Extraire les paramètres de la requête
        text = query["text"]
        filters = query.get("filters", {})
        top_k = query.get("top_k", 5)
        
        # Interroger la base de connaissances
        results = await rag_service.query(text, filters, top_k)
        
        return results
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de l'interrogation de la base de connaissances: {str(e)}"
        )

@router.post("/generate")
async def generate_with_rag(
    request: Dict[str, Any],
    db: Session = Depends(get_db)
):
    """
    Génère une réponse avec l'approche RAG
    
    Args:
        request: Requête contenant le texte de la question, les filtres optionnels et les paramètres de génération
    """
    # Initialiser le service RAG
    rag_service = RAGService()
    
    try:
        # Vérifier que la requête contient le texte de la question
        if "text" not in request or not request["text"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La requête doit contenir le texte de la question."
            )
        
        # Extraire les paramètres de la requête
        text = request["text"]
        filters = request.get("filters", {})
        generation_params = request.get("generation_params", {})
        
        # Générer une réponse
        response = await rag_service.generate(text, filters, generation_params)
        
        return response
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la génération de la réponse: {str(e)}"
        )

@router.get("/documents")
async def get_documents(
    document_type: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Récupère la liste des documents indexés dans la base de connaissances
    
    Args:
        document_type: Type de document à filtrer (optionnel)
    """
    # Initialiser le service RAG
    rag_service = RAGService()
    
    try:
        # Récupérer les documents
        documents = await rag_service.get_documents(document_type)
        
        return documents
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la récupération des documents: {str(e)}"
        )

@router.get("/documents/{document_id}")
async def get_document(
    document_id: str,
    db: Session = Depends(get_db)
):
    """
    Récupère un document indexé dans la base de connaissances
    
    Args:
        document_id: Identifiant du document
    """
    # Initialiser le service RAG
    rag_service = RAGService()
    
    try:
        # Récupérer le document
        document = await rag_service.get_document(document_id)
        
        if not document:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Document avec l'ID {document_id} non trouvé"
            )
        
        return document
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la récupération du document: {str(e)}"
        )

@router.delete("/documents/{document_id}")
async def delete_document(
    document_id: str,
    db: Session = Depends(get_db)
):
    """
    Supprime un document indexé dans la base de connaissances
    
    Args:
        document_id: Identifiant du document
    """
    # Initialiser le service RAG
    rag_service = RAGService()
    
    try:
        # Supprimer le document
        success = await rag_service.delete_document(document_id)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Document avec l'ID {document_id} non trouvé"
            )
        
        return {"message": "Document supprimé avec succès"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la suppression du document: {str(e)}"
        )
