from fastapi import APIRouter, UploadFile, File, HTTPException, status, Depends, Form
from typing import Optional
from app.infrastructure.storage.minio_client import MinioClient, get_minio_client
import uuid
import logging

logger = logging.getLogger(__name__)

# Configuration des types MIME autorisés et de la taille maximale
ALLOWED_IMAGE_TYPES = ["image/jpeg", "image/png", "image/jpg"]
MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5 MB

# Définition du routeur
router = APIRouter(
    prefix="/upload",
    tags=["upload"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", status_code=status.HTTP_201_CREATED)
async def upload_file(
    file: UploadFile = File(...),
    folder: str = Form("general"),
    minio_client: MinioClient = Depends(get_minio_client)
):
    """
    Upload un fichier et renvoie l'URL publique
    
    Args:
        file: Fichier à uploader
        folder: Dossier de destination (optionnel)
    
    Returns:
        URL publique du fichier
    """
    logger.info(f"Tentative d'upload du fichier: {file.filename}, type: {file.content_type}, dossier: {folder}")
    
    # Vérifier le type de fichier
    if file.content_type not in ALLOWED_IMAGE_TYPES:
        logger.warning(f"Type de fichier non autorisé: {file.content_type}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "message": f"Type de fichier non autorisé. Types autorisés: {', '.join(ALLOWED_IMAGE_TYPES)}",
                "code": "FORMAT_INVALID"
            }
        )
    
    # Vérifier la taille du fichier
    contents = await file.read()
    if len(contents) > MAX_IMAGE_SIZE:
        logger.warning(f"Taille de fichier dépassée: {len(contents)} bytes")
        await file.seek(0)  # Réinitialiser le curseur après lecture
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "message": f"Taille de fichier dépassée. Maximum: {MAX_IMAGE_SIZE/1024/1024} MB",
                "code": "SIZE_EXCEEDED"
            }
        )
    
    # Générer un nom unique pour le fichier
    original_filename = file.filename
    extension = original_filename.split(".")[-1] if "." in original_filename else ""
    unique_filename = f"{uuid.uuid4()}.{extension}" if extension else f"{uuid.uuid4()}"
    object_name = f"{folder}/{unique_filename}" if folder else unique_filename
    
    logger.info(f"Nom d'objet généré: {object_name}")
    
    # Uploader vers MinIO
    try:
        url = await minio_client.upload_file(
            object_name=object_name,
            file_data=contents,
            content_type=file.content_type
        )
        logger.info(f"Upload réussi: {url}")
        return {"url": url}
    except Exception as e:
        logger.error(f"Erreur lors de l'upload: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "message": f"Erreur lors de l'upload: {str(e)}",
                "code": "UPLOAD_ERROR"
            }
        )