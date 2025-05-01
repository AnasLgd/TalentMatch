import json
import os
from datetime import datetime
import uuid
from enum import Enum

class TaskStatus(str, Enum):
    PLANNED = "planned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    BLOCKED = "blocked"

class TaskPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class DevelopmentTracker:
    def __init__(self, tracker_file='/projects/TalentMatch/logs/development_tasks.json'):
        self.tracker_file = tracker_file
        self.tasks = self._load_tasks()

    def _load_tasks(self):
        if os.path.exists(self.tracker_file):
            with open(self.tracker_file, 'r') as f:
                return json.load(f)
        else:
            # Initialiser avec une structure vide
            initial_data = {
                "tasks": [],
                "last_updated": datetime.now().isoformat()
            }
            self._save_tasks(initial_data)
            return initial_data

    def _save_tasks(self, data):
        data["last_updated"] = datetime.now().isoformat()
        with open(self.tracker_file, 'w') as f:
            json.dump(data, f, indent=2)

    def add_task(self, title, description, component, user_story=None, 
                 priority=TaskPriority.MEDIUM, status=TaskStatus.PLANNED, 
                 assignee="Claude", dependencies=None, notes=None):
        """
        Ajoute une nouvelle tâche de développement
        
        Args:
            title (str): Titre de la tâche
            description (str): Description détaillée
            component (str): Composant concerné (frontend, backend, etc.)
            user_story (str, optional): Référence à une user story (ex: US1.2)
            priority (TaskPriority): Priorité de la tâche
            status (TaskStatus): Statut initial de la tâche
            assignee (str): Personne assignée à la tâche
            dependencies (list, optional): Liste des IDs de tâches dont celle-ci dépend
            notes (str, optional): Notes additionnelles
            
        Returns:
            str: ID de la tâche créée
        """
        task_id = str(uuid.uuid4())
        new_task = {
            "id": task_id,
            "title": title,
            "description": description,
            "component": component,
            "user_story": user_story,
            "priority": priority.value if isinstance(priority, TaskPriority) else priority,
            "status": status.value if isinstance(status, TaskStatus) else status,
            "assignee": assignee,
            "dependencies": dependencies or [],
            "notes": notes,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "completed_at": None,
            "history": [
                {
                    "timestamp": datetime.now().isoformat(),
                    "status": status.value if isinstance(status, TaskStatus) else status,
                    "comment": "Tâche créée"
                }
            ]
        }
        
        self.tasks["tasks"].append(new_task)
        self._save_tasks(self.tasks)
        print(f"Tâche créée avec l'ID: {task_id}")
        return task_id

    def update_task_status(self, task_id, new_status, comment=None):
        """
        Met à jour le statut d'une tâche
        
        Args:
            task_id (str): ID de la tâche
            new_status (TaskStatus): Nouveau statut
            comment (str, optional): Commentaire expliquant la mise à jour
            
        Returns:
            bool: True si la mise à jour a réussi, False sinon
        """
        for task in self.tasks["tasks"]:
            if task["id"] == task_id:
                old_status = task["status"]
                task["status"] = new_status.value if isinstance(new_status, TaskStatus) else new_status
                task["updated_at"] = datetime.now().isoformat()
                
                if new_status == TaskStatus.COMPLETED:
                    task["completed_at"] = datetime.now().isoformat()
                
                # Ajouter un élément d'historique
                task["history"].append({
                    "timestamp": datetime.now().isoformat(),
                    "status": new_status.value if isinstance(new_status, TaskStatus) else new_status,
                    "comment": comment or f"Statut changé de {old_status} à {new_status}"
                })
                
                self._save_tasks(self.tasks)
                print(f"Statut de la tâche {task_id} mis à jour: {new_status}")
                return True
                
        print(f"Tâche avec ID {task_id} non trouvée")
        return False

    def add_task_note(self, task_id, note):
        """
        Ajoute une note à une tâche existante
        
        Args:
            task_id (str): ID de la tâche
            note (str): Note à ajouter
            
        Returns:
            bool: True si l'ajout a réussi, False sinon
        """
        for task in self.tasks["tasks"]:
            if task["id"] == task_id:
                if task["notes"]:
                    task["notes"] += f"\n\n{datetime.now().isoformat()}: {note}"
                else:
                    task["notes"] = f"{datetime.now().isoformat()}: {note}"
                
                task["updated_at"] = datetime.now().isoformat()
                
                self._save_tasks(self.tasks)
                print(f"Note ajoutée à la tâche {task_id}")
                return True
                
        print(f"Tâche avec ID {task_id} non trouvée")
        return False

    def get_task(self, task_id):
        """
        Récupère une tâche par son ID
        
        Args:
            task_id (str): ID de la tâche
            
        Returns:
            dict: Tâche trouvée ou None
        """
        for task in self.tasks["tasks"]:
            if task["id"] == task_id:
                return task
        return None

    def get_tasks_by_status(self, status):
        """
        Récupère toutes les tâches avec un statut donné
        
        Args:
            status (TaskStatus): Statut à filtrer
            
        Returns:
            list: Liste des tâches correspondantes
        """
        status_value = status.value if isinstance(status, TaskStatus) else status
        return [task for task in self.tasks["tasks"] if task["status"] == status_value]

    def get_tasks_by_user_story(self, user_story):
        """
        Récupère toutes les tâches liées à une user story
        
        Args:
            user_story (str): Référence de la user story (ex: US1.2)
            
        Returns:
            list: Liste des tâches correspondantes
        """
        return [task for task in self.tasks["tasks"] if task["user_story"] == user_story]

    def generate_report(self):
        """
        Génère un rapport sur l'état actuel des tâches
        
        Returns:
            dict: Rapport avec statistiques
        """
        total_tasks = len(self.tasks["tasks"])
        statuses = {}
        priorities = {}
        components = {}
        user_stories = {}
        
        for status in TaskStatus:
            statuses[status.value] = 0
            
        for priority in TaskPriority:
            priorities[priority.value] = 0
            
        for task in self.tasks["tasks"]:
            statuses[task["status"]] = statuses.get(task["status"], 0) + 1
            priorities[task["priority"]] = priorities.get(task["priority"], 0) + 1
            
            if task["component"] not in components:
                components[task["component"]] = 0
            components[task["component"]] += 1
            
            if task["user_story"] and task["user_story"] not in user_stories:
                user_stories[task["user_story"]] = 0
            if task["user_story"]:
                user_stories[task["user_story"]] += 1
        
        return {
            "total_tasks": total_tasks,
            "by_status": statuses,
            "by_priority": priorities,
            "by_component": components,
            "by_user_story": user_stories,
            "generated_at": datetime.now().isoformat()
        }

# Initialisation du tracker si le script est exécuté directement
if __name__ == "__main__":
    tracker = DevelopmentTracker()
    
    # Création de quelques tâches initiales pour l'onboarding
    tracker.add_task(
        title="Configuration de l'environnement de développement",
        description="Mise en place des outils de développement et de suivi",
        component="infrastructure",
        user_story=None,
        priority=TaskPriority.HIGH,
        status=TaskStatus.COMPLETED,
        notes="Environnement configuré avec succès"
    )
    
    tracker.add_task(
        title="Analyse du code existant",
        description="Revue du code et identification des patterns utilisés",
        component="global",
        user_story=None,
        priority=TaskPriority.HIGH,
        status=TaskStatus.IN_PROGRESS,
        notes="En cours d'analyse"
    )
    
    tracker.add_task(
        title="Planification du développement",
        description="Identification des prochaines user stories à implémenter",
        component="global",
        user_story=None,
        priority=TaskPriority.HIGH,
        status=TaskStatus.PLANNED
    )
    
    print("Tracker de développement initialisé avec succès.")
    print(json.dumps(tracker.generate_report(), indent=2))
