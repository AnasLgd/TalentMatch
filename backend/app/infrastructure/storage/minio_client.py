from minio import Minio
from minio.error import S3Error
from fastapi import Depends
from app.core.config import settings
from typing import Optional, Dict, Any
import logging
import io
import json

logger = logging.getLogger(__name__)

class MinioClient:
    def __init__(self):
        """
        Initialisation du client MinIO avec les paramètres de configuration
        """
        self.client = Minio(
            endpoint=settings.MINIO_ENDPOINT,
            access_key=settings.MINIO_ACCESS_KEY,
            secret_key=settings.MINIO_SECRET_KEY,
            secure=settings.MINIO_SECURE
        )
        self.bucket_name = settings.MINIO_BUCKET_NAME
        self._ensure_bucket_exists()
    
    def _ensure_bucket_exists(self):
        """S'assure que le bucket existe, le crée sinon"""
        try:
            if not self.client.bucket_exists(self.bucket_name):
                self.client.make_bucket(self.bucket_name)
                # Configurer une politique publique pour permettre l'accès aux objets
                policy = {
                    "Version": "2012-10-17",
                    "Statement": [
                        {
                            "Effect": "Allow",
                            "Principal": {"AWS": "*"},
                            "Action": ["s3:GetObject"],
                            "Resource": [f"arn:aws:s3:::{self.bucket_name}/*"]
                        }
                    ]
                }
                self.client.set_bucket_policy(self.bucket_name, json.dumps(policy))
                logger.info(f"Bucket {self.bucket_name} créé avec succès")
        except S3Error as e:
            logger.error(f"Erreur MinIO lors de la vérification/création du bucket: {e}")
            raise
    
    async def upload_file(self, object_name: str, file_data: bytes, content_type: str) -> str:
        """
        Upload un fichier et renvoie son URL
        
        Args:
            object_name: Nom de l'objet dans MinIO
            file_data: Données binaires du fichier
            content_type: Type MIME du fichier
        
        Returns:
            URL de l'objet
        """
        try:
            # Créer un objet io.BytesIO à partir des données binaires
            file_data_io = io.BytesIO(file_data)
            
            # Upload vers MinIO
            self.client.put_object(
                bucket_name=self.bucket_name,
                object_name=object_name,
                data=file_data_io,
                length=len(file_data),
                content_type=content_type
            )
            
            # Construire l'URL
            if hasattr(settings, 'MINIO_PUBLIC_URL') and settings.MINIO_PUBLIC_URL:
                url = f"{settings.MINIO_PUBLIC_URL}/{self.bucket_name}/{object_name}"
            else:
                url = f"http{'s' if settings.MINIO_SECURE else ''}://{settings.MINIO_ENDPOINT}/{self.bucket_name}/{object_name}"
            
            logger.info(f"Fichier uploadé avec succès: {url}")
            return url
        except S3Error as e:
            logger.error(f"Erreur lors de l'upload vers MinIO: {e}")
            raise
    
    async def delete_file(self, object_name: str) -> bool:
        """
        Supprime un fichier
        
        Args:
            object_name: Nom de l'objet à supprimer
            
        Returns:
            True si la suppression a réussi, False sinon
        """
        try:
            self.client.remove_object(self.bucket_name, object_name)
            logger.info(f"Fichier supprimé avec succès: {object_name}")
            return True
        except S3Error as e:
            logger.error(f"Erreur lors de la suppression du fichier {object_name}: {e}")
            return False
    
    async def generate_presigned_url(self, object_name: str, expires: int = 3600) -> str:
        """
        Génère une URL présignée pour accéder temporairement à un fichier
        
        Args:
            object_name: Nom de l'objet
            expires: Durée de validité en secondes
            
        Returns:
            URL présignée
        """
        try:
            url = self.client.presigned_get_object(
                bucket_name=self.bucket_name,
                object_name=object_name,
                expires=expires
            )
            logger.info(f"URL présignée générée pour {object_name}")
            return url
        except S3Error as e:
            logger.error(f"Erreur lors de la génération de l'URL présignée pour {object_name}: {e}")
            raise

    async def list_files(self, prefix: str = "") -> list:
        """
        Liste les fichiers dans un répertoire
        
        Args:
            prefix: Préfixe pour filtrer les objets
            
        Returns:
            Liste des noms d'objets
        """
        try:
            objects = self.client.list_objects(self.bucket_name, prefix=prefix, recursive=True)
            return [obj.object_name for obj in objects]
        except S3Error as e:
            logger.error(f"Erreur lors de la liste des fichiers avec préfixe {prefix}: {e}")
            raise

# Dépendance FastAPI pour l'injection
def get_minio_client() -> MinioClient:
    """
    Factory pour l'injection de dépendance du client MinIO
    """
    return MinioClient()