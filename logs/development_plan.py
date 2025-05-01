import sys
import os
from pathlib import Path
import json
from datetime import datetime, timedelta

# Ajout du répertoire parent au sys.path pour permettre l'import des modules
sys.path.append(str(Path(__file__).parent.parent))

# Import des modules de journalisation et de suivi de développement
from logs.init_logging import setup_logging, log_development_activity
from logs.development_tracker import DevelopmentTracker, TaskStatus, TaskPriority
from logs.user_story_analysis import UserStoryAnalyzer

# Configuration du système de journalisation
loggers = setup_logging()
dev_logger = loggers['dev']
error_logger = loggers['error']
audit_logger = loggers['audit']

# Initialisation du tracker de développement et de l'analyseur de user stories
tracker = DevelopmentTracker()
analyzer = UserStoryAnalyzer()

class DevelopmentPlanner:
    def __init__(self, plan_file='/projects/TalentMatch/logs/development_plan.json'):
        self.plan_file = plan_file
        self.plan = self._load_plan()
        
    def _load_plan(self):
        if os.path.exists(self.plan_file):
            with open(self.plan_file, 'r') as f:
                return json.load(f)
        else:
            # Initialiser avec une structure vide
            initial_data = {
                "sprints": [],
                "current_sprint": None,
                "backlog": [],
                "last_updated": datetime.now().isoformat()
            }
            self._save_plan(initial_data)
            return initial_data
    
    def _save_plan(self, data):
        data["last_updated"] = datetime.now().isoformat()
        with open(self.plan_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def create_sprint(self, name, start_date, end_date, description=None, goals=None):
        """
        Crée un nouveau sprint dans le plan de développement
        
        Args:
            name (str): Nom du sprint
            start_date (str): Date de début au format YYYY-MM-DD
            end_date (str): Date de fin au format YYYY-MM-DD
            description (str, optional): Description du sprint
            goals (list, optional): Objectifs du sprint
            
        Returns:
            dict: Sprint créé
        """
        sprint = {
            "id": len(self.plan["sprints"]) + 1,
            "name": name,
            "start_date": start_date,
            "end_date": end_date,
            "description": description,
            "goals": goals or [],
            "user_stories": [],
            "tasks": [],
            "status": "planned",
            "created_at": datetime.now().isoformat()
        }
        
        self.plan["sprints"].append(sprint)
        self._save_plan(self.plan)
        
        log_development_activity(
            dev_logger,
            'planning',
            f'Création du sprint {name}',
            {
                'sprint_id': sprint["id"],
                'start_date': start_date,
                'end_date': end_date
            }
        )
        
        print(f"Sprint {name} créé avec succès.")
        return sprint
    
    def set_current_sprint(self, sprint_id):
        """
        Définit le sprint courant
        
        Args:
            sprint_id (int): ID du sprint
            
        Returns:
            bool: True si le sprint a été défini, False sinon
        """
        for sprint in self.plan["sprints"]:
            if sprint["id"] == sprint_id:
                self.plan["current_sprint"] = sprint_id
                self._save_plan(self.plan)
                
                log_development_activity(
                    dev_logger,
                    'planning',
                    f'Définition du sprint courant',
                    {
                        'sprint_id': sprint_id,
                        'sprint_name': sprint["name"]
                    }
                )
                
                print(f"Sprint courant défini: {sprint['name']}")
                return True
        
        print(f"Sprint avec ID {sprint_id} non trouvé")
        return False
    
    def add_user_story_to_sprint(self, sprint_id, user_story_id, priority=TaskPriority.HIGH):
        """
        Ajoute une user story à un sprint
        
        Args:
            sprint_id (int): ID du sprint
            user_story_id (str): ID de la user story
            priority (TaskPriority): Priorité de la user story dans le sprint
            
        Returns:
            bool: True si l'ajout a réussi, False sinon
        """
        # Vérifier que la user story existe
        user_story = analyzer.get_user_story_analysis(user_story_id)
        if not user_story:
            print(f"User story {user_story_id} non trouvée")
            return False
        
        # Trouver le sprint
        sprint = None
        for s in self.plan["sprints"]:
            if s["id"] == sprint_id:
                sprint = s
                break
        
        if not sprint:
            print(f"Sprint avec ID {sprint_id} non trouvé")
            return False
        
        # Vérifier que la user story n'est pas déjà dans le sprint
        for us in sprint["user_stories"]:
            if us["id"] == user_story_id:
                print(f"User story {user_story_id} déjà présente dans le sprint {sprint_id}")
                return False
        
        # Ajouter la user story au sprint
        sprint_user_story = {
            "id": user_story_id,
            "title": user_story["title"],
            "priority": priority.value if isinstance(priority, TaskPriority) else priority,
            "status": "planned",
            "added_at": datetime.now().isoformat()
        }
        
        sprint["user_stories"].append(sprint_user_story)
        self._save_plan(self.plan)
        
        log_development_activity(
            dev_logger,
            'planning',
            f'Ajout de la user story {user_story_id} au sprint {sprint_id}',
            {
                'sprint_id': sprint_id,
                'user_story_id': user_story_id,
                'priority': priority.value if isinstance(priority, TaskPriority) else priority
            }
        )
        
        print(f"User story {user_story_id} ajoutée au sprint {sprint_id}")
        return True
    
    def add_task_to_sprint(self, sprint_id, task_id):
        """
        Ajoute une tâche existante à un sprint
        
        Args:
            sprint_id (int): ID du sprint
            task_id (str): ID de la tâche
            
        Returns:
            bool: True si l'ajout a réussi, False sinon
        """
        # Vérifier que la tâche existe
        task = tracker.get_task(task_id)
        if not task:
            print(f"Tâche {task_id} non trouvée")
            return False
        
        # Trouver le sprint
        sprint = None
        for s in self.plan["sprints"]:
            if s["id"] == sprint_id:
                sprint = s
                break
        
        if not sprint:
            print(f"Sprint avec ID {sprint_id} non trouvé")
            return False
        
        # Vérifier que la tâche n'est pas déjà dans le sprint
        for t in sprint["tasks"]:
            if t["id"] == task_id:
                print(f"Tâche {task_id} déjà présente dans le sprint {sprint_id}")
                return False
        
        # Ajouter la tâche au sprint
        sprint_task = {
            "id": task_id,
            "title": task["title"],
            "user_story": task["user_story"],
            "status": task["status"],
            "added_at": datetime.now().isoformat()
        }
        
        sprint["tasks"].append(sprint_task)
        self._save_plan(self.plan)
        
        log_development_activity(
            dev_logger,
            'planning',
            f'Ajout de la tâche {task_id} au sprint {sprint_id}',
            {
                'sprint_id': sprint_id,
                'task_id': task_id,
                'user_story': task["user_story"]
            }
        )
        
        print(f"Tâche {task_id} ajoutée au sprint {sprint_id}")
        return True
    
    def generate_sprint_report(self, sprint_id):
        """
        Génère un rapport sur l'état d'un sprint
        
        Args:
            sprint_id (int): ID du sprint
            
        Returns:
            dict: Rapport du sprint ou None si le sprint n'existe pas
        """
        sprint = None
        for s in self.plan["sprints"]:
            if s["id"] == sprint_id:
                sprint = s
                break
        
        if not sprint:
            print(f"Sprint avec ID {sprint_id} non trouvé")
            return None
        
        # Calculer les statistiques
        user_story_statuses = {}
        task_statuses = {}
        
        for us in sprint["user_stories"]:
            status = us["status"]
            user_story_statuses[status] = user_story_statuses.get(status, 0) + 1
        
        for task in sprint["tasks"]:
            status = task["status"]
            task_statuses[status] = task_statuses.get(status, 0) + 1
        
        # Générer le rapport
        report = {
            "sprint_id": sprint_id,
            "name": sprint["name"],
            "start_date": sprint["start_date"],
            "end_date": sprint["end_date"],
            "status": sprint["status"],
            "user_stories_count": len(sprint["user_stories"]),
            "tasks_count": len(sprint["tasks"]),
            "user_story_statuses": user_story_statuses,
            "task_statuses": task_statuses,
            "generated_at": datetime.now().isoformat()
        }
        
        # Calculer l'avancement
        total_us = len(sprint["user_stories"])
        completed_us = user_story_statuses.get("completed", 0)
        report["user_story_progress"] = (completed_us / total_us) * 100 if total_us > 0 else 0
        
        total_tasks = len(sprint["tasks"])
        completed_tasks = task_statuses.get("completed", 0)
        report["task_progress"] = (completed_tasks / total_tasks) * 100 if total_tasks > 0 else 0
        
        return report
    
    def update_sprint_status(self, sprint_id, new_status):
        """
        Met à jour le statut d'un sprint
        
        Args:
            sprint_id (int): ID du sprint
            new_status (str): Nouveau statut (planned, active, completed, canceled)
            
        Returns:
            bool: True si la mise à jour a réussi, False sinon
        """
        for sprint in self.plan["sprints"]:
            if sprint["id"] == sprint_id:
                sprint["status"] = new_status
                self._save_plan(self.plan)
                
                log_development_activity(
                    dev_logger,
                    'planning',
                    f'Mise à jour du statut du sprint {sprint_id}',
                    {
                        'sprint_id': sprint_id,
                        'new_status': new_status
                    }
                )
                
                print(f"Statut du sprint {sprint_id} mis à jour: {new_status}")
                return True
        
        print(f"Sprint avec ID {sprint_id} non trouvé")
        return False
    
    def add_to_backlog(self, user_story_id, priority=TaskPriority.MEDIUM):
        """
        Ajoute une user story au backlog
        
        Args:
            user_story_id (str): ID de la user story
            priority (TaskPriority): Priorité dans le backlog
            
        Returns:
            bool: True si l'ajout a réussi, False sinon
        """
        # Vérifier que la user story existe
        user_story = analyzer.get_user_story_analysis(user_story_id)
        if not user_story:
            print(f"User story {user_story_id} non trouvée")
            return False
        
        # Vérifier que la user story n'est pas déjà dans le backlog
        for item in self.plan["backlog"]:
            if item["id"] == user_story_id:
                print(f"User story {user_story_id} déjà présente dans le backlog")
                return False
        
        # Ajouter la user story au backlog
        backlog_item = {
            "id": user_story_id,
            "title": user_story["title"],
            "priority": priority.value if isinstance(priority, TaskPriority) else priority,
            "status": "backlog",
            "added_at": datetime.now().isoformat()
        }
        
        self.plan["backlog"].append(backlog_item)
        self._save_plan(self.plan)
        
        log_development_activity(
            dev_logger,
            'planning',
            f'Ajout de la user story {user_story_id} au backlog',
            {
                'user_story_id': user_story_id,
                'priority': priority.value if isinstance(priority, TaskPriority) else priority
            }
        )
        
        print(f"User story {user_story_id} ajoutée au backlog")
        return True
    
    def get_current_sprint(self):
        """
        Récupère le sprint courant
        
        Returns:
            dict: Sprint courant ou None si aucun sprint n'est défini
        """
        if not self.plan["current_sprint"]:
            return None
        
        for sprint in self.plan["sprints"]:
            if sprint["id"] == self.plan["current_sprint"]:
                return sprint
        
        return None
    
    def get_backlog(self):
        """
        Récupère le backlog
        
        Returns:
            list: Backlog
        """
        return self.plan["backlog"]
    
    def get_all_sprints(self):
        """
        Récupère tous les sprints
        
        Returns:
            list: Liste des sprints
        """
        return self.plan["sprints"]

# Fonction pour initialiser le plan de développement initial
def initialize_development_plan():
    planner = DevelopmentPlanner()
    
    # Créer le premier sprint (dates fictives pour la démonstration)
    today = datetime.now()
    sprint_start = today + timedelta(days=1)
    sprint_end = sprint_start + timedelta(days=14)
    
    sprint = planner.create_sprint(
        name="Sprint 1 - Fondations",
        start_date=sprint_start.strftime("%Y-%m-%d"),
        end_date=sprint_end.strftime("%Y-%m-%d"),
        description="Sprint initial pour établir les fondations de la plateforme",
        goals=[
            "Implémenter la création et gestion des profils consultant",
            "Implémenter la création des appels d'offres",
            "Mettre en place l'infrastructure de base pour le matching"
        ]
    )
    
    # Définir ce sprint comme le sprint courant
    planner.set_current_sprint(sprint["id"])
    
    # Ajouter les user stories prioritaires au sprint
    planner.add_user_story_to_sprint(sprint["id"], "US1.1", TaskPriority.HIGH)  # Création de profil consultant
    planner.add_user_story_to_sprint(sprint["id"], "US2.1", TaskPriority.HIGH)  # Création d'appel d'offres
    
    # Ajouter d'autres user stories au backlog
    planner.add_to_backlog("US1.2", TaskPriority.HIGH)  # Téléchargement et analyse de CV
    planner.add_to_backlog("US3.1", TaskPriority.HIGH)  # Matching automatique
    planner.add_to_backlog("US4.1", TaskPriority.MEDIUM)  # Création de partenariats
    
    print("Plan de développement initial créé avec succès.")
    
    # Créer des tâches de développement pour le sprint 1
    tasks = []
    
    # Tâches pour US1.1: Création de profil consultant
    us1_1_task = tracker.add_task(
        title="Implémentation des fonctionnalités de création de profil consultant",
        description="Développement des fonctionnalités back et frontend pour la création de profils consultant",
        component="global",
        user_story="US1.1",
        priority=TaskPriority.HIGH,
        status=TaskStatus.PLANNED
    )
    tasks.append(us1_1_task)
    
    # Sous-tâches pour US1.1
    us1_1_backend_task = tracker.add_task(
        title="API de création de consultant",
        description="Développement de l'endpoint d'API pour la création de consultants",
        component="backend",
        user_story="US1.1",
        priority=TaskPriority.HIGH,
        status=TaskStatus.PLANNED,
        dependencies=[us1_1_task]
    )
    tasks.append(us1_1_backend_task)
    
    us1_1_frontend_task = tracker.add_task(
        title="Formulaire de création de consultant",
        description="Développement du formulaire React pour la création de consultants",
        component="frontend",
        user_story="US1.1",
        priority=TaskPriority.HIGH,
        status=TaskStatus.PLANNED,
        dependencies=[us1_1_task]
    )
    tasks.append(us1_1_frontend_task)
    
    us1_1_tests_task = tracker.add_task(
        title="Tests pour la création de consultant",
        description="Développement des tests unitaires et d'intégration pour la création de consultants",
        component="testing",
        user_story="US1.1",
        priority=TaskPriority.MEDIUM,
        status=TaskStatus.PLANNED,
        dependencies=[us1_1_backend_task, us1_1_frontend_task]
    )
    tasks.append(us1_1_tests_task)
    
    # Tâches pour US2.1: Création d'appel d'offres
    us2_1_task = tracker.add_task(
        title="Implémentation des fonctionnalités de création d'appel d'offres",
        description="Développement des fonctionnalités back et frontend pour la création d'appels d'offres",
        component="global",
        user_story="US2.1",
        priority=TaskPriority.HIGH,
        status=TaskStatus.PLANNED
    )
    tasks.append(us2_1_task)
    
    # Sous-tâches pour US2.1
    us2_1_backend_task = tracker.add_task(
        title="API de création d'appel d'offres",
        description="Développement de l'endpoint d'API pour la création d'appels d'offres",
        component="backend",
        user_story="US2.1",
        priority=TaskPriority.HIGH,
        status=TaskStatus.PLANNED,
        dependencies=[us2_1_task]
    )
    tasks.append(us2_1_backend_task)
    
    us2_1_frontend_task = tracker.add_task(
        title="Formulaire de création d'appel d'offres",
        description="Développement du formulaire React pour la création d'appels d'offres",
        component="frontend",
        user_story="US2.1",
        priority=TaskPriority.HIGH,
        status=TaskStatus.PLANNED,
        dependencies=[us2_1_task]
    )
    tasks.append(us2_1_frontend_task)
    
    us2_1_tests_task = tracker.add_task(
        title="Tests pour la création d'appel d'offres",
        description="Développement des tests unitaires et d'intégration pour la création d'appels d'offres",
        component="testing",
        user_story="US2.1",
        priority=TaskPriority.MEDIUM,
        status=TaskStatus.PLANNED,
        dependencies=[us2_1_backend_task, us2_1_frontend_task]
    )
    tasks.append(us2_1_tests_task)
    
    # Ajouter toutes les tâches au sprint
    for task_id in tasks:
        planner.add_task_to_sprint(sprint["id"], task_id)
    
    # Générer un rapport initial du sprint
    report = planner.generate_sprint_report(sprint["id"])
    print("\n=== RAPPORT INITIAL DU SPRINT ===")
    print(f"Sprint: {report['name']}")
    print(f"Période: {report['start_date']} au {report['end_date']}")
    print(f"User stories: {report['user_stories_count']}")
    print(f"Tâches: {report['tasks_count']}")
    print("==================================\n")

if __name__ == "__main__":
    print("Initialisation du plan de développement...")
    initialize_development_plan()
    
    print("Plan de développement initialisé avec succès.")
