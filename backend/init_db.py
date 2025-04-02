#!/usr/bin/env python
import os
import sys
import time
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError

# Ajouter le répertoire parent au PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def wait_for_db(db_url, max_retries=5, retry_interval=3):
    """Attendre que la base de données soit disponible"""
    print("Vérification de la connexion à la base de données...")
    
    engine = create_engine(db_url)
    retries = 0
    
    while retries < max_retries:
        try:
            # Test de connexion simple
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            print("✅ Connexion à la base de données établie!")
            return True
        except OperationalError as e:
            retries += 1
            if retries >= max_retries:
                print(f"❌ Échec de connexion à la base de données après {max_retries} tentatives")
                print(f"Erreur: {e}")
                return False
            print(f"⏳ Tentative {retries}/{max_retries}: La base de données n'est pas encore disponible. Nouvelle tentative dans {retry_interval} secondes...")
            time.sleep(retry_interval)
    
    return False

def init_db():
    """
    Initialise la base de données en créant toutes les tables
    depuis les modèles SQLAlchemy.
    """
    try:
        from app.core.config import settings
        from app.infrastructure.database.models import Base
        
        print("Initialisation de la base de données...")
        
        # Construction de l'URL de connexion
        db_url = f"postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"
        
        print(f"Connexion à {settings.POSTGRES_DB} sur {settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}")
        
        # Attendre que la base de données soit disponible
        if not wait_for_db(db_url):
            return False
        
        # Création du moteur SQLAlchemy
        engine = create_engine(db_url)
        
        # Création de toutes les tables
        print("Création des tables...")
        Base.metadata.create_all(engine)
        print("✅ Base de données initialisée avec succès!")
        return True
    except Exception as e:
        print(f"❌ Erreur lors de l'initialisation de la base de données: {str(e)}")
        return False

if __name__ == "__main__":
    success = init_db()
    sys.exit(0 if success else 1)