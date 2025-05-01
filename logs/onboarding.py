#!/usr/bin/env python3
import os
import sys
from pathlib import Path
import json
from datetime import datetime
import subprocess
import argparse

# Ajout du répertoire parent au sys.path pour permettre l'import des modules
sys.path.append(str(Path(__file__).parent.parent))

# Import des modules de journalisation
from logs.init_logging import setup_logging, log_development_activity, log_audit

# Configuration du système de journalisation
loggers = setup_logging()
dev_logger = loggers['dev']
error_logger = loggers['error']
audit_logger = loggers['audit']

def log_section(title):
    """Affiche un titre de section bien formaté et le journalise"""
    separator = "=" * 80
    print(f"\n{separator}")
    print(f"  {title}")
    print(f"{separator}\n")
    
    log_development_activity(
        dev_logger,
        'onboarding',
        f'Exécution de la section: {title}'
    )

def check_environment():
    """Vérifie que l'environnement est correctement configuré"""
    log_section("Vérification de l'environnement")
    
    # Vérification des répertoires du projet
    required_dirs = [
        '/projects/TalentMatch/backend',
        '/projects/TalentMatch/frontend',
        '/projects/TalentMatch/logs'
    ]
    
    for directory in required_dirs:
        if os.path.isdir(directory):
            print(f"✅ Répertoire trouvé: {directory}")
        else:
            print(f"❌ Répertoire manquant: {directory}")
            return False
    
    # Vérification des fichiers de configuration
    required_files = [
        '/projects/TalentMatch/docker-compose.yml',
        '/projects/TalentMatch/README.md',
        '/projects/TalentMatch/product_backlog.md'
    ]
    
    for file in required_files:
        if os.path.isfile(file):
            print(f"✅ Fichier trouvé: {file}")
        else:
            print(f"❌ Fichier manquant: {file}")
            return False
    
    # Vérification de l'accès au système de journalisation
    try:
        log_development_activity(
            dev_logger,
            'environment',
            'Vérification de l\'environnement réussie'
        )
        print("✅ Système de journalisation accessible")
    except Exception as e:
        print(f"❌ Erreur d'accès au système de journalisation: {str(e)}")
        return False
    
    return True

def initialize_logging_system():
    """Initialise le système de journalisation"""
    log_section("Initialisation du système de journalisation")
    
    try:
        # Exécuter le script d'initialisation du système de journalisation
        result = subprocess.run(
            [sys.executable, '/projects/TalentMatch/logs/init_logging.py'],
            capture_output=True,
            text=True,
            check=True
        )
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur lors de l'initialisation du système de journalisation: {e}")
        print(f"Sortie d'erreur: {e.stderr}")
        return False

def initialize_development_tracker():
    """Initialise le tracker de développement"""
    log_section("Initialisation du tracker de développement")
    
    try:
        # Exécuter le script d'initialisation du tracker de développement
        result = subprocess.run(
            [sys.executable, '/projects/TalentMatch/logs/development_tracker.py'],
            capture_output=True,
            text=True,
            check=True
        )
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur lors de l'initialisation du tracker de développement: {e}")
        print(f"Sortie d'erreur: {e.stderr}")
        return False

def analyze_user_stories():
    """Analyse les user stories prioritaires"""
    log_section("Analyse des user stories prioritaires")
    
    try:
        # Exécuter le script d'analyse des user stories
        result = subprocess.run(
            [sys.executable, '/projects/TalentMatch/logs/user_story_analysis.py'],
            capture_output=True,
            text=True,
            check=True
        )
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur lors de l'analyse des user stories: {e}")
        print(f"Sortie d'erreur: {e.stderr}")
        return False

def create_development_plan():
    """Crée le plan de développement initial"""
    log_section("Création du plan de développement")
    
    try:
        # Exécuter le script de création du plan de développement
        result = subprocess.run(
            [sys.executable, '/projects/TalentMatch/logs/development_plan.py'],
            capture_output=True,
            text=True,
            check=True
        )
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur lors de la création du plan de développement: {e}")
        print(f"Sortie d'erreur: {e.stderr}")
        return False

def initialize_development():
    """Initialise l'environnement de développement"""
    log_section("Initialisation de l'environnement de développement")
    
    try:
        # Exécuter le script d'initialisation du développement
        result = subprocess.run(
            [sys.executable, '/projects/TalentMatch/logs/init_development.py'],
            capture_output=True,
            text=True,
            check=True
        )
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur lors de l'initialisation de l'environnement de développement: {e}")
        print(f"Sortie d'erreur: {e.stderr}")
        return False

def create_onboarding_summary():
    """Crée un résumé du processus d'onboarding"""
    log_section("Création du résumé d'onboarding")
    
    summary = {
        "project": "TalentMatch",
        "onboarding_date": datetime.now().isoformat(),
        "status": "success",
        "components": {
            "logging_system": True,
            "development_tracker": True,
            "user_story_analysis": True,
            "development_plan": True,
            "development_environment": True
        },
        "next_steps": [
            "Exécuter 'docker-compose up' pour démarrer les services",
            "Accéder au dashboard à http://localhost:3001/dashboard",
            "Suivre le plan de développement dans logs/development_plan.json",
            "Commencer par les tâches du Sprint 1"
        ]
    }
    
    # Écrire le résumé dans un fichier
    summary_path = '/projects/TalentMatch/logs/onboarding_summary.json'
    with open(summary_path, 'w') as f:
        json.dump(summary, f, indent=2)
    
    print(f"✅ Résumé d'onboarding créé: {summary_path}")
    
    # Créer aussi une version lisible du résumé
    readable_path = '/projects/TalentMatch/logs/onboarding_summary.md'
    with open(readable_path, 'w') as f:
        f.write("# Résumé du processus d'onboarding TalentMatch\n\n")
        f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write("## Statut des composants\n\n")
        for component, status in summary["components"].items():
            status_icon = "✅" if status else "❌"
            f.write(f"- {status_icon} {component.replace('_', ' ').title()}\n")
        
        f.write("\n## Prochaines étapes\n\n")
        for i, step in enumerate(summary["next_steps"], 1):
            f.write(f"{i}. {step}\n")
        
        f.write("\n## Structure du projet\n\n")
        f.write("Le projet TalentMatch est organisé selon une architecture hexagonale avec les composants suivants:\n\n")
        f.write("- **Frontend**: React, TypeScript, Tailwind CSS, Shadcn UI\n")
        f.write("- **Backend**: FastAPI (Python) avec architecture hexagonale\n")
        f.write("- **Services**: PostgreSQL, MinIO, Redis, n8n\n")
        f.write("- **Infrastructure**: Docker, Docker Compose\n\n")
        
        f.write("## Développement actif\n\n")
        f.write("Les principales user stories en cours de développement sont:\n\n")
        f.write("- **US1.1**: Création de profil consultant\n")
        f.write("- **US2.1**: Création d'appel d'offres\n\n")
        
        f.write("Les user stories suivantes sont dans le backlog pour le prochain sprint:\n\n")
        f.write("- **US1.2**: Téléchargement et analyse de CV\n")
        f.write("- **US3.1**: Matching automatique\n")
        f.write("- **US4.1**: Création de partenariats\n\n")
        
        f.write("## Journalisation et suivi\n\n")
        f.write("Un système complet de journalisation et de suivi a été mis en place:\n\n")
        f.write("- Logs de développement: `/projects/TalentMatch/logs/development.log`\n")
        f.write("- Logs d'erreurs: `/projects/TalentMatch/logs/error.log`\n")
        f.write("- Logs d'audit: `/projects/TalentMatch/logs/audit.log`\n")
        f.write("- Suivi des tâches: `/projects/TalentMatch/logs/development_tasks.json`\n")
        f.write("- Plan de développement: `/projects/TalentMatch/logs/development_plan.json`\n\n")
        
        f.write("Pour suivre l'avancement du développement, consultez régulièrement ces fichiers.\n")
    
    print(f"✅ Résumé d'onboarding lisible créé: {readable_path}")
    return True

def run_onboarding():
    """Exécute le processus complet d'onboarding"""
    log_section("DÉMARRAGE DU PROCESSUS D'ONBOARDING")
    
    # Vérification de l'environnement
    if not check_environment():
        print("❌ Vérification de l'environnement échouée, arrêt du processus d'onboarding.")
        return False
    
    # Initialisation du système de journalisation
    if not initialize_logging_system():
        print("❌ Initialisation du système de journalisation échouée, arrêt du processus d'onboarding.")
        return False
    
    # Initialisation du tracker de développement
    if not initialize_development_tracker():
        print("❌ Initialisation du tracker de développement échouée, arrêt du processus d'onboarding.")
        return False
    
    # Analyse des user stories
    if not analyze_user_stories():
        print("❌ Analyse des user stories échouée, arrêt du processus d'onboarding.")
        return False
    
    # Création du plan de développement
    if not create_development_plan():
        print("❌ Création du plan de développement échouée, arrêt du processus d'onboarding.")
        return False
    
    # Initialisation de l'environnement de développement
    if not initialize_development():
        print("❌ Initialisation de l'environnement de développement échouée, arrêt du processus d'onboarding.")
        return False
    
    # Création du résumé d'onboarding
    if not create_onboarding_summary():
        print("❌ Création du résumé d'onboarding échouée.")
        return False
    
    log_section("PROCESSUS D'ONBOARDING TERMINÉ AVEC SUCCÈS")
    print("\nLe processus d'onboarding s'est terminé avec succès!")
    print("Consultez le résumé dans /projects/TalentMatch/logs/onboarding_summary.md")
    print("\nPour démarrer le développement:")
    print("1. Exécutez 'docker-compose up' pour démarrer les services")
    print("2. Accédez au dashboard à http://localhost:3001/dashboard")
    print("3. Suivez le plan de développement dans logs/development_plan.json")
    print("4. Commencez par les tâches du Sprint 1")
    
    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script d'onboarding pour le projet TalentMatch")
    parser.add_argument("--check-only", action="store_true", help="Vérifier seulement l'environnement sans exécuter l'onboarding complet")
    
    args = parser.parse_args()
    
    if args.check_only:
        check_environment()
    else:
        run_onboarding()
