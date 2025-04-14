from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import Generator

from app.core.config import settings

# Utilisation de la méthode existante qui force le port interne à 5432 pour les connexions Docker
SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

# Création du moteur SQLAlchemy
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Création d'une session locale
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base pour les modèles déclaratifs
Base = declarative_base()

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
