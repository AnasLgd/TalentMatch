# Guide d'utilisation de l'infrastructure de développement TalentMatch

Ce document explique comment utiliser l'infrastructure de développement mise en place pour le projet TalentMatch. Cette infrastructure comprend des outils de journalisation, de suivi des tâches, d'analyse des user stories, et de planification du développement.

## 1. Vue d'ensemble

L'infrastructure de développement de TalentMatch est organisée autour des composants suivants :

- **Système de journalisation** : Capture et enregistre les activités de développement, erreurs et événements d'audit.
- **Tracker de développement** : Suit les tâches de développement, leur statut et leur progression.
- **Analyseur de user stories** : Décompose les user stories en exigences techniques et identifie les risques.
- **Planificateur de développement** : Organise les sprints et la répartition des tâches.

Ces composants fonctionnent ensemble pour fournir une traçabilité complète du processus de développement et faciliter la collaboration.

## 2. Installation et configuration

### 2.1. Prérequis

- Python 3.10+
- Accès au répertoire `/projects/TalentMatch`

### 2.2. Initialisation

Pour initialiser l'infrastructure complète, exécutez le script d'onboarding :

```bash
cd /projects/TalentMatch
python logs/onboarding.py
```

Ce script vérifie l'environnement, initialise tous les composants et génère un résumé du processus d'onboarding.

Pour vérifier uniquement l'environnement sans exécuter l'initialisation complète :

```bash
python logs/onboarding.py --check-only
```

## 3. Utilisation des composants

### 3.1. Système de journalisation

Le système de journalisation est configuré pour capturer trois types de logs :

- **Logs de développement** : Activités normales de développement (`/projects/TalentMatch/logs/development.log`)
- **Logs d'erreurs** : Erreurs et exceptions (`/projects/TalentMatch/logs/error.log`)
- **Logs d'audit** : Événements de sécurité et d'accès (`/projects/TalentMatch/logs/audit.log`)

Pour utiliser le système de journalisation dans votre code :

```python
from logs.init_logging import setup_logging, log_development_activity, log_error, log_audit

# Configuration du système de journalisation
loggers = setup_logging()
dev_logger = loggers['dev']
error_logger = loggers['error']
audit_logger = loggers['audit']

# Exemple d'utilisation
log_development_activity(
    dev_logger,
    'frontend',
    'Implémentation du formulaire de création de consultant',
    {
        'component': 'ConsultantForm',
        'user_story': 'US1.1'
    }
)

log_error(
    error_logger,
    'api',
    'Erreur lors de la création du consultant',
    exception,
    {
        'user_id': 123,
        'request_data': request_data
    }
)

log_audit(
    audit_logger,
    'admin',
    'modification',
    'user_permissions',
    True,
    {
        'user_id': 123,
        'previous_role': 'user',
        'new_role': 'admin'
    }
)
```

### 3.2. Tracker de développement

Le tracker de développement permet de suivre les tâches de développement, leur statut et leur progression.

```python
from logs.development_tracker import DevelopmentTracker, TaskStatus, TaskPriority

# Initialisation du tracker
tracker = DevelopmentTracker()

# Ajouter une tâche
task_id = tracker.add_task(
    title="Implémentation de l'API de création de consultant",
    description="Développement de l'endpoint d'API pour la création de consultants",
    component="backend",
    user_story="US1.1",
    priority=TaskPriority.HIGH,
    status=TaskStatus.PLANNED
)

# Mettre à jour le statut d'une tâche
tracker.update_task_status(
    task_id,
    TaskStatus.IN_PROGRESS,
    "Démarrage de l'implémentation"
)

# Ajouter une note à une tâche
tracker.add_task_note(
    task_id,
    "Implémentation des validations de données terminée"
)

# Générer un rapport
report = tracker.generate_report()
print(report)
```

### 3.3. Analyseur de user stories

L'analyseur de user stories permet de décomposer les user stories en exigences techniques et d'identifier les risques.

```python
from logs.user_story_analysis import UserStoryAnalyzer

# Initialisation de l'analyseur
analyzer = UserStoryAnalyzer()

# Ajouter une analyse de user story
analyzer.add_user_story_analysis(
    user_story_id="US1.1",
    title="Création de profil consultant",
    description="En tant que Recruteur, je veux créer un profil pour un nouveau consultant afin de l'ajouter à notre base de talents",
    acceptance_criteria=[
        "Formulaire avec champs obligatoires (nom, prénom, titre, expérience)",
        "Possibilité d'ajouter une photo de profil",
        "Validation des données saisies",
        "Confirmation de création réussie"
    ],
    technical_requirements=[
        "Endpoint API pour la création de consultant",
        "Validation des données avec Pydantic et Zod",
        "Intégration avec le service de stockage pour les photos",
        "Formulaire React avec gestion d'erreurs",
        "Tests unitaires et d'intégration"
    ],
    dependencies=[],
    risks=[
        "Gestion des permissions et droits d'accès",
        "Performance lors du téléchargement de photos volumineuses"
    ]
)

# Récupérer l'analyse d'une user story
analysis = analyzer.get_user_story_analysis("US1.1")
print(analysis)
```

### 3.4. Planificateur de développement

Le planificateur de développement permet d'organiser les sprints et la répartition des tâches.

```python
from logs.development_plan import DevelopmentPlanner
from logs.development_tracker import TaskPriority

# Initialisation du planificateur
planner = DevelopmentPlanner()

# Créer un sprint
sprint = planner.create_sprint(
    name="Sprint 2 - Analyse de CV",
    start_date="2025-05-10",
    end_date="2025-05-24",
    description="Sprint focalisé sur l'analyse de CV",
    goals=[
        "Implémenter le téléchargement et l'analyse de CV",
        "Améliorer l'interface utilisateur du profil consultant"
    ]
)

# Ajouter une user story au sprint
planner.add_user_story_to_sprint(sprint["id"], "US1.2", TaskPriority.HIGH)

# Ajouter une tâche au sprint
planner.add_task_to_sprint(sprint["id"], task_id)

# Générer un rapport de sprint
report = planner.generate_sprint_report(sprint["id"])
print(report)
```

## 4. Flux de travail recommandé

### 4.1. Au début d'un sprint

1. Créez un nouveau sprint avec le planificateur de développement.
2. Ajoutez les user stories à implémenter dans ce sprint.
3. Décomposez chaque user story en tâches techniques avec le tracker de développement.
4. Ajoutez ces tâches au sprint.

### 4.2. Pendant le développement

1. Mettez à jour le statut des tâches au fur et à mesure de l'avancement.
2. Utilisez le système de journalisation pour tracer les activités importantes.
3. Ajoutez des notes aux tâches pour documenter les décisions et les problèmes rencontrés.

### 4.3. À la fin d'un sprint

1. Générez un rapport de sprint pour évaluer la progression.
2. Mettez à jour le statut du sprint (completed).
3. Préparez le prochain sprint en fonction des résultats obtenus.

## 5. Fichiers et emplacements

- **Logs de développement** : `/projects/TalentMatch/logs/development.log`
- **Logs d'erreurs** : `/projects/TalentMatch/logs/error.log`
- **Logs d'audit** : `/projects/TalentMatch/logs/audit.log`
- **Tâches de développement** : `/projects/TalentMatch/logs/development_tasks.json`
- **Analyses de user stories** : `/projects/TalentMatch/logs/user_story_analysis.json`
- **Plan de développement** : `/projects/TalentMatch/logs/development_plan.json`
- **Résumé d'onboarding** : `/projects/TalentMatch/logs/onboarding_summary.md`

## 6. Dépannage

### 6.1. Problèmes courants

- **Les logs ne sont pas générés** : Vérifiez que le répertoire `/projects/TalentMatch/logs` existe et a les bonnes permissions.
- **Erreurs d'importation de modules** : Assurez-vous que le répertoire parent est dans le `sys.path`.
- **Fichiers JSON corrompus** : Faites une copie de sauvegarde avant de les modifier manuellement.

### 6.2. Réinitialisation

Si nécessaire, vous pouvez réinitialiser l'infrastructure en supprimant les fichiers JSON et en relançant le script d'onboarding :

```bash
cd /projects/TalentMatch
rm logs/*.json
python logs/onboarding.py
```

## 7. Extension et personnalisation

Cette infrastructure est conçue pour être extensible. Vous pouvez ajouter de nouveaux composants ou personnaliser les existants selon vos besoins.

Pour ajouter un nouveau composant :

1. Créez un nouveau module dans le répertoire `/projects/TalentMatch/logs/`.
2. Intégrez-le avec les composants existants en suivant les patterns établis.
3. Mettez à jour le script d'onboarding pour initialiser votre nouveau composant.

## 8. Contribution

Lorsque vous contribuez au projet, assurez-vous de :

1. Suivre les conventions de codage établies.
2. Documenter vos modifications dans les logs et les tâches.
3. Mettre à jour ce guide si vous apportez des modifications à l'infrastructure.
