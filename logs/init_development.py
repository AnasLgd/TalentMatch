import sys
import os
from pathlib import Path

# Ajout du répertoire parent au sys.path pour permettre l'import des modules
sys.path.append(str(Path(__file__).parent.parent))

# Import des modules de journalisation et de suivi de développement
from logs.init_logging import setup_logging, log_development_activity
from logs.development_tracker import DevelopmentTracker, TaskStatus, TaskPriority

# Configuration du système de journalisation
loggers = setup_logging()
dev_logger = loggers['dev']
error_logger = loggers['error']
audit_logger = loggers['audit']

# Initialisation du tracker de développement
tracker = DevelopmentTracker()

def initialize_onboarding_tasks():
    """Initialise les tâches d'onboarding pour le projet"""
    
    # Tâches d'analyse
    analysis_task = tracker.add_task(
        title="Analyse approfondie de l'architecture et du code",
        description="Compréhension détaillée de l'architecture hexagonale et des patterns utilisés",
        component="global",
        priority=TaskPriority.HIGH,
        status=TaskStatus.IN_PROGRESS,
        notes="Analyse en cours des composants principaux"
    )
    
    # Tâches d'infrastructure
    tracker.add_task(
        title="Configuration de l'environnement de développement local",
        description="Installation et configuration de l'environnement Docker",
        component="infrastructure",
        priority=TaskPriority.HIGH,
        status=TaskStatus.PLANNED,
        dependencies=[]
    )
    
    # Tâches de vérification
    tracker.add_task(
        title="Vérification des tests existants",
        description="Analyse des tests actuels et de la couverture de code",
        component="testing",
        priority=TaskPriority.MEDIUM,
        status=TaskStatus.PLANNED,
        dependencies=[analysis_task]
    )
    
    # Tâches de documentation
    tracker.add_task(
        title="Mise à jour de la documentation d'onboarding",
        description="Documenter le processus d'onboarding pour les futurs développeurs",
        component="documentation",
        priority=TaskPriority.MEDIUM,
        status=TaskStatus.PLANNED
    )
    
    # Tâches de développement - basées sur le backlog
    tracker.add_task(
        title="Analyse des épics prioritaires",
        description="Identification des user stories à implémenter en priorité",
        component="product",
        priority=TaskPriority.HIGH,
        status=TaskStatus.PLANNED,
        dependencies=[analysis_task]
    )
    
    # Log des activités
    log_development_activity(
        dev_logger,
        'onboarding',
        'Initialisation des tâches d\'onboarding',
        {
            'tasks_count': 5,
            'priority_high': 3,
            'priority_medium': 2
        }
    )
    
    print("Tâches d'onboarding initialisées avec succès.")

def print_report():
    """Affiche un rapport détaillé sur les tâches"""
    report = tracker.generate_report()
    print("\n=== RAPPORT DES TÂCHES ===")
    print(f"Total des tâches: {report['total_tasks']}")
    
    print("\nStatut des tâches:")
    for status, count in report['by_status'].items():
        print(f"  {status}: {count}")
    
    print("\nPriorité des tâches:")
    for priority, count in report['by_priority'].items():
        print(f"  {priority}: {count}")
    
    print("\nTâches par composant:")
    for component, count in report['by_component'].items():
        print(f"  {component}: {count}")
    
    if report['by_user_story']:
        print("\nTâches par user story:")
        for story, count in report['by_user_story'].items():
            if story:  # Ignorer les None
                print(f"  {story}: {count}")
    
    print(f"\nRapport généré le: {report['generated_at']}")
    print("===========================\n")

def initialize_user_story_tasks(user_story, title, description, tasks):
    """
    Initialise les tâches pour une user story spécifique
    
    Args:
        user_story (str): Identifiant de la user story (ex: "US1.2")
        title (str): Titre de la user story
        description (str): Description de la user story
        tasks (list): Liste des tâches à créer, chaque tâche étant un dictionnaire
            avec title, description, component, priority, et dependencies (optionnel)
    """
    print(f"\nInitialisation des tâches pour {user_story}: {title}")
    
    # Créer une tâche principale pour la user story
    main_task_id = tracker.add_task(
        title=f"Implémentation de {user_story}",
        description=f"{title}\n\n{description}",
        component="product",
        user_story=user_story,
        priority=TaskPriority.HIGH,
        status=TaskStatus.PLANNED
    )
    
    # Créer les sous-tâches
    task_ids = []
    for task in tasks:
        dependencies = task.get("dependencies", [])
        # Ajouter la tâche principale comme dépendance
        if main_task_id not in dependencies:
            dependencies.append(main_task_id)
            
        task_id = tracker.add_task(
            title=task["title"],
            description=task["description"],
            component=task["component"],
            user_story=user_story,
            priority=task.get("priority", TaskPriority.MEDIUM),
            status=TaskStatus.PLANNED,
            dependencies=dependencies
        )
        task_ids.append(task_id)
    
    # Log des activités
    log_development_activity(
        dev_logger,
        'planning',
        f'Initialisation des tâches pour {user_story}',
        {
            'user_story': user_story,
            'tasks_count': len(tasks) + 1
        }
    )
    
    print(f"Tâches pour {user_story} initialisées avec succès.")
    return main_task_id, task_ids

if __name__ == "__main__":
    print("Initialisation du système de développement...")
    initialize_onboarding_tasks()
    print_report()
    
    print("Système de développement initialisé avec succès.")
