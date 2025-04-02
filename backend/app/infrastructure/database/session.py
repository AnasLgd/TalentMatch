from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from typing import Generator

from app.core.config import settings

# Création de l'URL de connexion à la base de données
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"

# Création du moteur SQLAlchemy
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Création d'une session locale
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base pour les modèles déclaratifs
Base = declarative_base()

@contextmanager
def get_db() -> Generator:
    """
    Fournit une session de base de données et assure sa fermeture après utilisation.
    À utiliser avec un bloc with.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_db_session():
    """
    Fournit une session de base de données pour l'injection de dépendance FastAPI.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
