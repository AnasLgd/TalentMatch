# Architecture Backend TalentMatch

## Vue d'ensemble

Le backend de TalentMatch est développé avec FastAPI et Python, suivant une architecture hexagonale (ou architecture en ports et adaptateurs). Cette approche permet de séparer clairement le domaine métier de l'infrastructure technique, facilitant les tests et l'évolution du système.

## Structure du projet

```
backend/
├── app/
│   ├── adapters/              # Implémentations des interfaces
│   │   ├── n8n/               # Intégration avec n8n
│   │   ├── repositories/      # Implémentations des repositories avec SQLAlchemy
│   │   └── services/          # Implémentations des services externes
│   ├── api/                   # Endpoints API
│   │   └── v1/                # API version 1
│   │       ├── consultants.py # Endpoints pour les consultants
│   │       ├── tenders.py     # Endpoints pour les appels d'offres
│   │       ├── matches.py     # Endpoints pour le matching
│   │       └── ...            # Autres endpoints
│   ├── core/                  # Cœur du domaine métier
│   │   ├── config.py          # Configuration de l'application
│   │   ├── entities/          # Entités du domaine
│   │   ├── interfaces/        # Interfaces (ports)
│   │   └── use_cases/         # Cas d'utilisation
│   ├── cv_extraction/         # Module d'extraction de données des CV
│   └── infrastructure/        # Configuration technique
│       └── database/          # Configuration de la base de données
├── migrations/                # Scripts de migration Alembic
│   └── versions/              # Versions des migrations
└── tests/                     # Tests unitaires et d'intégration
```

## Technologies principales

- **FastAPI 0.100+** : Framework web rapide pour la création d'API
- **Python 3.10+** : Langage de programmation
- **SQLAlchemy 2.0+** : ORM pour l'accès à la base de données
- **Alembic** : Outil de migration de base de données
- **PostgreSQL** : Système de gestion de base de données
- **Redis** : Cache pour les données fréquemment utilisées
- **MinIO** : Stockage d'objets compatible S3
- **n8n** : Outil d'automatisation des workflows
- **JWT** : Authentification via tokens

## Principes architecturaux

### Architecture hexagonale

Le backend suit une architecture hexagonale (ou architecture en ports et adaptateurs) qui :

- Isole le domaine métier des détails d'implémentation
- Facilite les tests unitaires et d'intégration
- Permet de remplacer facilement les composants techniques

Cette architecture se compose de trois couches principales :

1. **Core (Domaine)** : Entités, interfaces (ports) et cas d'utilisation
2. **Adaptateurs** : Implémentations concrètes des interfaces
3. **Infrastructure** : Configuration technique et dépendances externes

### Entités du domaine

Les entités représentent les objets métier principaux :

- Consultant
- Tender (Appel d'offres)
- Match
- Collaboration
- CV
- Skill

Exemple d'entité :

```python
class Consultant(BaseModel):
    id: int
    user_id: int
    company_id: int
    title: str
    experience_years: Optional[int]
    availability_status: AvailabilityStatus
    availability_date: Optional[date]
    hourly_rate: Optional[float]
    daily_rate: Optional[float]
    bio: Optional[str]
    location: Optional[str]
    remote_work: bool
    max_travel_distance: Optional[int]
    skills: List[Dict[str, Any]]
    created_at: datetime
    updated_at: Optional[datetime]
```

### Interfaces (Ports)

Les interfaces définissent les contrats que les adaptateurs doivent implémenter :

- Repository interfaces : pour l'accès aux données
- Service interfaces : pour les services externes

Exemple d'interface :

```python
class ConsultantRepository(Protocol):
    async def get_all(self) -> List[Consultant]: ...
    async def get_by_id(self, consultant_id: int) -> Optional[Consultant]: ...
    async def create(self, consultant: ConsultantCreate) -> Consultant: ...
    async def update(self, consultant_id: int, consultant: ConsultantUpdate) -> Optional[Consultant]: ...
    async def delete(self, consultant_id: int) -> bool: ...
```

### Cas d'utilisation

Les cas d'utilisation implémentent la logique métier en utilisant les interfaces :

```python
class ConsultantUseCase:
    def __init__(self, consultant_repository: ConsultantRepository,
                 skill_repository: SkillRepository,
                 cv_analysis_service: CVAnalysisService):
        self.consultant_repository = consultant_repository
        self.skill_repository = skill_repository
        self.cv_analysis_service = cv_analysis_service

    async def get_all_consultants(self) -> List[Consultant]: ...
    async def get_consultant_by_id(self, consultant_id: int) -> Optional[Consultant]: ...
    async def create_consultant(self, consultant_data: ConsultantCreate) -> Consultant: ...
```

### API Endpoints

Les endpoints API sont organisés par domaine fonctionnel :

```
/api/v1/consultants
/api/v1/tenders
/api/v1/matches
/api/v1/collaborations
/api/v1/cv-analysis
```

## Fonctionnalités spécifiques

### Intégration avec n8n

Le backend intègre n8n pour l'automatisation des workflows complexes, notamment pour :

- L'extraction et l'analyse des CV
- Le matching automatique entre consultants et appels d'offres
- Les notifications et alertes

### Analyse des CV

Le module `cv_extraction` est responsable de l'extraction de données structurées à partir des CV :

- Extraction des informations personnelles
- Identification des compétences
- Extraction des expériences et formations
- Suggestion de rôle et d'années d'expérience

### Algorithme de matching

Le système utilise un algorithme sophistiqué pour le matching entre consultants et appels d'offres :

- Prise en compte des compétences requises et du niveau d'expertise
- Évaluation de la disponibilité et de la localisation
- Calcul d'un score de matching entre 0 et 1
- Suggestion des meilleurs matchs

## Sécurité

- Authentification JWT pour sécuriser les API
- Hachage des mots de passe avec bcrypt
- Contrôle d'accès basé sur les rôles (RBAC)
- Validation des données d'entrée avec Pydantic
- Protection contre les injections SQL via SQLAlchemy

## Performance et scalabilité

- Cache Redis pour les requêtes fréquentes
- Optimisation des requêtes SQL avec indexation appropriée
- Architecture asynchrone avec FastAPI pour un traitement concurrentiel
- Containeurisation pour un déploiement scalable
