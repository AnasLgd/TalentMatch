from pydantic import BaseSettings
from typing import Optional, Dict, Any, List
import os
from dotenv import load_dotenv

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

class Settings(BaseSettings):
    # Informations sur l'application
    APP_NAME: str = os.getenv("APP_NAME", "TalentMatch")
    API_V1_STR: str = os.getenv("API_V1_STR", "/api/v1")
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    
    # Configuration de la base de données PostgreSQL
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "postgres" if os.getenv("ENVIRONMENT") == "development" else "localhost")
    POSTGRES_PORT: str = "5432"  # Port interne dans le conteneur, fixé à 5432 pour éviter les problèmes de connexion
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "talentmatch")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "talentmatch_password")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "talentmatch")
    
    # Construction de l'URL de connexion à la base de données
    @property
    def DATABASE_URL(self) -> str:
        # Force the port to be 5432 (internal Docker container port)
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:5432/{self.POSTGRES_DB}"
    
    # Configuration de MinIO (stockage compatible S3)
    MINIO_HOST: str = os.getenv("MINIO_HOST", "minio" if os.getenv("ENVIRONMENT") == "development" else "localhost")
    MINIO_PORT: str = os.getenv("MINIO_PORT", "9000")
    MINIO_ACCESS_KEY: str = os.getenv("MINIO_ACCESS_KEY", os.getenv("MINIO_ROOT_USER", "talentmatch"))
    MINIO_SECRET_KEY: str = os.getenv("MINIO_SECRET_KEY", os.getenv("MINIO_ROOT_PASSWORD", "talentmatch_password"))
    MINIO_BUCKET: str = os.getenv("MINIO_BUCKET", "talentmatch")
    MINIO_USE_SSL: bool = os.getenv("MINIO_USE_SSL", "false").lower() == "true"
    
    # Configuration de Redis (cache)
    REDIS_HOST: str = os.getenv("REDIS_HOST", "redis" if os.getenv("ENVIRONMENT") == "development" else "localhost")
    REDIS_PORT: str = os.getenv("REDIS_PORT", "6379")
    REDIS_PASSWORD: Optional[str] = os.getenv("REDIS_PASSWORD", "talentmatch_password")
    REDIS_DB: int = int(os.getenv("REDIS_DB", "0"))
    
    # Construction de l'URL de connexion à Redis
    @property
    def REDIS_URL(self) -> str:
        password_part = f":{self.REDIS_PASSWORD}@" if self.REDIS_PASSWORD else ""
        return f"redis://{password_part}{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"
    
    # Configuration de n8n
    N8N_HOST: str = os.getenv("N8N_HOST", "n8n" if os.getenv("ENVIRONMENT") == "development" else "localhost")
    N8N_PORT: str = os.getenv("N8N_PORT", "5678")  # Port interne dans le conteneur
    N8N_API_KEY: str = os.getenv("N8N_API_KEY", "talentmatch_apikey")
    N8N_ENCRYPTION_KEY: str = os.getenv("N8N_ENCRYPTION_KEY", "supersecretkey")
    
    # Construction de l'URL d'accès à n8n
    @property
    def N8N_URL(self) -> str:
        return f"http://{self.N8N_HOST}:{self.N8N_PORT}"
    
    # Configuration de sécurité
    SECRET_KEY: str = os.getenv("SECRET_KEY", "supersecretkey")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "10080"))  # 7 jours par défaut
    
    # Configuration CORS
    @property
    def CORS_ORIGINS(self) -> List[str]:
        cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:3000")
        if cors_origins == "*":
            return ["*"]
        return [origin.strip() for origin in cors_origins.split(",")]
    
    class Config:
        env_file = ".env"
        case_sensitive = True

    # Méthode pour obtenir l'URL de la base de données compatible avec SQLAlchemy
    def get_sqlalchemy_database_url(self) -> str:
        return self.DATABASE_URL

settings = Settings()