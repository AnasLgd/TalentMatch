# Architecture Backend TalentMatch

## Vue d'ensemble

Le backend de TalentMatch est développé avec FastAPI et Python, suivant une architecture hexagonale (ou architecture en ports et adaptateurs). Cette approche permet de séparer clairement le domaine métier de l'infrastructure technique, facilitant les tests et l'évolution du système.

Le backend suit des principes de clean code, avec une séparation du code par domaines fonctionnels et une forte séparation des préoccupations. Il implémente une approche "schema-first" où la validation des données est prioritaire, en utilisant des modèles Pydantic qui définissent à la fois les contrats d'API et les entités du domaine.

## Structure du projet

```
backend/
├── app/
│   ├── adapters/              # Implémentations des interfaces
│   │   ├── n8n/               # Intégration avec n8n
│   │   │   └── workflow_service.py # Service d'exécution des workflows
│   │   ├── repositories/      # Implémentations des repositories avec SQLAlchemy
│   │   │   ├── collaboration_repository.py
│   │   │   ├── company_repository.py
│   │   │   ├── consultant_repository.py
│   │   │   ├── match_repository.py
│   │   │   ├── skill_repository.py
│   │   │   ├── tender_repository.py
│   │   │   └── user_repository.py
│   │   └── services/          # Implémentations des services externes
│   │       ├── agent_ia_maison_service.py
│   │       ├── cv_analysis_service.py
│   │       ├── enhanced_cv_analysis_service.py
│   │       ├── matchmaking_service.py
│   │       ├── n8n_cv_analysis_service.py
│   │       └── rag_service.py
│   ├── api/                   # Endpoints API
│   │   └── v1/                # API version 1
│   │       ├── collaborations.py
│   │       ├── companies.py
│   │       ├── consultants.py
│   │       ├── cv_analysis.py
│   │       ├── matches.py
│   │       ├── n8n.py
│   │       ├── rag.py
│   │       └── tenders.py
│   ├── core/                  # Cœur du domaine métier
│   │   ├── config.py          # Configuration de l'application
│   │   ├── entities/          # Entités du domaine
│   │   │   ├── collaboration.py
│   │   │   ├── company.py
│   │   │   ├── consultant.py
│   │   │   ├── match.py
│   │   │   ├── portfolio.py
│   │   │   ├── skill.py
│   │   │   ├── tender.py
│   │   │   └── user.py
│   │   ├── interfaces/        # Interfaces (ports)
│   │   │   ├── collaboration_repository.py
│   │   │   ├── collaboration_service.py
│   │   │   ├── company_repository.py
│   │   │   ├── consultant_repository.py
│   │   │   ├── cv_analysis_service.py
│   │   │   ├── cv_extraction_service.py
│   │   │   ├── match_repository.py
│   │   │   ├── matchmaking_service.py
│   │   │   ├── n8n_integration_service.py
│   │   │   ├── portfolio_repository.py
│   │   │   ├── rag_service.py
│   │   │   ├── skill_repository.py
│   │   │   ├── tender_repository.py
│   │   │   └── user_repository.py
│   │   └── use_cases/         # Cas d'utilisation
│   │       ├── collaboration_use_case.py
│   │       ├── consultant_use_case.py
│   │       ├── cv_analysis_use_case.py
│   │       ├── match_use_case.py
│   │       ├── portfolio_use_case.py
│   │       ├── tender_use_case.py
│   │       └── user_use_case.py
│   ├── cv_extraction/         # Module d'extraction de données des CV
│   ├── infrastructure/        # Configuration technique
│   │   ├── cache/             # Configuration du cache Redis
│   │   ├── database/          # Configuration de la base de données
│   │   │   ├── models.py      # Modèles SQLAlchemy
│   │   │   ├── seed.sql       # Données initiales
│   │   │   └── session.py     # Gestion des sessions de base de données
│   │   ├── security/          # Sécurité et authentification
│   │   │   └── password.py    # Gestion des mots de passe
│   │   └── storage/           # Stockage de fichiers (MinIO/S3)
│   └── main.py                # Point d'entrée de l'application
├── migrations/                # Scripts de migration Alembic
│   ├── env.py
│   ├── script.py.mako
│   └── versions/              # Versions des migrations
│       ├── 001_initial.py
│       ├── 002_n8n_ia_maison.py
│       ├── 003_convert_tender_skills_to_model.py
│       ├── 004_add_workflow_status_enum.py
│       ├── 005_add_photo_url_to_consultant.py
│       ├── 006_make_consultant_user_id_nullable.py
│       └── 007_add_first_last_name_to_consultants.py
└── tests/                     # Tests unitaires et d'intégration
    ├── conftest.py
    ├── e2e/                   # Tests end-to-end
    ├── integration/           # Tests d'intégration
    ├── test_api.py
    ├── test_workflows.py
    └── unit/                  # Tests unitaires
```

## Technologies principales

- **FastAPI 0.100+** : Framework web rapide pour la création d'API
- **Python 3.10+** : Langage de programmation
- **SQLAlchemy 2.0+** : ORM pour l'accès à la base de données
- **Pydantic 2.0+** : Validation des données et sérialisation
- **Alembic** : Outil de migration de base de données
- **PostgreSQL** : Système de gestion de base de données
- **Redis** : Cache pour les données fréquemment utilisées
- **MinIO** : Stockage d'objets compatible S3
- **n8n** : Outil d'automatisation des workflows
- **JWT** : Authentification via tokens
- **Vector Embeddings** : Pour la recherche sémantique via RAG
- **Langchain** : Intégration avec des LLMs pour l'analyse documentaire

## Principes architecturaux

### Architecture hexagonale

Le backend suit une architecture hexagonale (ou architecture en ports et adaptateurs) qui :

- Isole le domaine métier des détails d'implémentation
- Facilite les tests unitaires et d'intégration
- Permet de remplacer facilement les composants techniques
- Centralise la logique métier indépendamment des technologies utilisées

Cette architecture se compose de trois couches principales :

1. **Core (Domaine)** : 
   - **Entités** : Modèles de données du domaine métier définis avec Pydantic
   - **Interfaces (Ports)** : Contrats définis via des Protocol Python que les adaptateurs doivent implémenter
   - **Cas d'utilisation** : Orchestration de la logique métier utilisant les interfaces

2. **Adaptateurs** : 
   - **Repositories** : Implémentations des interfaces repository pour l'accès aux données via SQLAlchemy
   - **Services** : Implémentations des interfaces de service pour l'interaction avec des systèmes externes
   - **API** : Endpoints FastAPI qui exposent les fonctionnalités aux utilisateurs

3. **Infrastructure** : 
   - **Database** : Configuration de la base de données et définition des modèles SQLAlchemy
   - **Security** : Mécanismes d'authentification et d'autorisation
   - **Cache** : Configuration et utilisation du cache Redis
   - **Storage** : Gestion du stockage des fichiers avec MinIO

### Approche Schema-First

L'application adopte une approche "schema-first" où :

- Les modèles Pydantic définissent à la fois les contrats d'API et les entités du domaine
- La validation des données est effectuée à chaque niveau (entrée API, logique métier, persistance)
- Les schémas garantissent la cohérence des données à travers toute l'application

### Entités du domaine

Le modèle de données du système est composé des entités suivantes, définies dans les modèles SQLAlchemy et les schémas Pydantic correspondants :

#### User
Représente un utilisateur du système avec différents rôles.
```python
class User:
    id: int
    email: str
    full_name: str
    role: UserRole  # ADMIN, MANAGER, CONSULTANT, CLIENT
    company_id: Optional[int]
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime]
```

#### Company
Représente une entreprise cliente ou une ESN (Entreprise de Services du Numérique).
```python
class Company:
    id: int
    name: str
    description: Optional[str]
    website: Optional[str]
    address: Optional[str]
    logo_url: Optional[str]
    is_esn: bool  # True si ESN, False si client
    created_at: datetime
    updated_at: Optional[datetime]
```

#### Consultant
Représente un consultant disponible pour des missions.
```python
class Consultant:
    id: int
    user_id: Optional[int]  # Peut être null pour les consultants sans compte utilisateur
    company_id: int
    first_name: Optional[str]
    last_name: Optional[str]
    title: str
    bio: Optional[str]
    years_experience: Optional[int]
    hourly_rate: Optional[float]
    daily_rate: Optional[float]
    availability_date: Optional[date]
    status: ConsultantStatus  # AVAILABLE, ON_MISSION, UNAVAILABLE, LEAVING
    cv_url: Optional[str]
    linkedin_url: Optional[str]
    github_url: Optional[str]
    photo_url: Optional[str]
    skills: List[Dict[str, Any]]  # Liste de compétences avec niveau et années d'expérience
    created_at: datetime
    updated_at: Optional[datetime]
```

#### Skill
Représente une compétence technique ou non-technique.
```python
class Skill:
    id: int
    name: str
    category: str  # ex: "programming", "language", "soft skill"
    description: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]
```

#### ConsultantSkill
Représente l'association entre un consultant et une compétence, avec des détails sur le niveau.
```python
class ConsultantSkill:
    consultant_id: int
    skill_id: int
    proficiency_level: ProficiencyLevel  # BEGINNER, INTERMEDIATE, ADVANCED, EXPERT
    years_experience: int
    details: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]
```

#### Tender
Représente un appel d'offres ou une mission proposée par une entreprise.
```python
class Tender:
    id: int
    title: str
    description: Optional[str]
    company_id: int
    start_date: Optional[date]
    end_date: Optional[date]
    location: Optional[str]
    remote_allowed: bool
    status: TenderStatus  # DRAFT, OPEN, IN_PROGRESS, CLOSED, CANCELLED
    budget_min: Optional[float]
    budget_max: Optional[float]
    skills: List[Dict[str, Any]]  # Liste de compétences requises avec niveau d'importance
    created_at: datetime
    updated_at: Optional[datetime]
```

#### TenderSkill
Représente l'association entre un appel d'offres et une compétence, avec des détails sur l'importance.
```python
class TenderSkill:
    id: int
    tender_id: int
    skill_id: int
    importance: str  # "required", "preferred", "nice_to_have"
    details: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]
```

#### Match
Représente une correspondance entre un consultant et un appel d'offres.
```python
class Match:
    id: int
    consultant_id: int
    tender_id: int
    score: float  # Score de correspondance (0-1)
    status: MatchStatus  # PENDING, PROPOSED, ACCEPTED, REJECTED, CANCELLED
    notes: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]
```

#### Collaboration
Représente une collaboration établie entre un consultant et un client.
```python
class Collaboration:
    id: int
    match_id: int
    consultant_id: int
    tender_id: int
    start_date: Optional[date]
    end_date: Optional[date]
    hourly_rate: Optional[float]
    daily_rate: Optional[float]
    status: CollaborationStatus  # DRAFT, ACTIVE, COMPLETED, CANCELLED
    contract_url: Optional[str]
    notes: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]
```

#### Portfolio
Représente un projet ou une réalisation d'un consultant.
```python
class Portfolio:
    id: int
    title: str
    description: Optional[str]
    company_id: int
    image_url: Optional[str]
    project_url: Optional[str]
    start_date: Optional[date]
    end_date: Optional[date]
    created_at: datetime
    updated_at: Optional[datetime]
```

#### Resume
Représente un CV téléchargé dans le système.
```python
class Resume:
    id: int
    consultant_id: int
    file_name: str
    file_path: str
    file_type: str  # ex: "pdf", "docx"
    file_size: int
    parsed_data: Dict[str, Any]  # Données extraites du CV
    created_at: datetime
    updated_at: Optional[datetime]
```

#### WorkflowExecution
Représente l'exécution d'un workflow n8n.
```python
class WorkflowExecution:
    id: int
    workflow_id: str
    execution_id: str
    status: WorkflowStatus  # RUNNING, SUCCESS, ERROR, CANCELLED
    data: Dict[str, Any]
    resume_id: Optional[int]
    match_id: Optional[int]
    portfolio_id: Optional[int]
    error_message: Optional[str]
    started_at: datetime
    finished_at: Optional[datetime]
    created_at: datetime
    updated_at: Optional[datetime]
```

#### RAGDocument
Représente un document indexé pour la recherche sémantique.
```python
class RAGDocument:
    id: int
    document_id: str
    document_type: DocumentType  # CV, TENDER, SKILL, PORTFOLIO
    title: str
    content: str
    document_metadata: Dict[str, Any]
    file_path: Optional[str]
    chunk_count: int
    indexed_at: datetime
    created_at: datetime
    updated_at: Optional[datetime]
```

#### RAGChunk
Représente un fragment de document indexé avec son embedding.
```python
class RAGChunk:
    id: int
    chunk_id: str
    document_id: int
    content: str
    embedding: str  # Représentation vectorielle sous forme de texte
    chunk_index: Optional[int]
    token_count: Optional[int]
    created_at: datetime
```

#### RAGQuery
Représente une requête de recherche sémantique.
```python
class RAGQuery:
    id: int
    query_text: str
    embedding: Optional[str]
    user_id: Optional[int]
    generated_response: Optional[str]
    created_at: datetime
```

### Interfaces (Ports)

Les interfaces définissent les contrats que les adaptateurs doivent implémenter :

#### Interfaces de Repository

Ces interfaces définissent les opérations de persistance pour chaque entité :

- **ConsultantRepository** : Gestion des consultants
- **TenderRepository** : Gestion des appels d'offres
- **MatchRepository** : Gestion des matchings
- **CollaborationRepository** : Gestion des collaborations
- **CompanyRepository** : Gestion des entreprises
- **UserRepository** : Gestion des utilisateurs
- **SkillRepository** : Gestion des compétences
- **PortfolioRepository** : Gestion des portfolios

Exemple d'une interface repository :

```python
class ConsultantRepository(Protocol):
    async def get_all(self) -> List[Consultant]: ...
    async def get_by_id(self, consultant_id: int) -> Optional[Consultant]: ...
    async def create(self, consultant: ConsultantCreate) -> Consultant: ...
    async def update(self, consultant_id: int, consultant: ConsultantUpdate) -> Optional[Consultant]: ...
    async def delete(self, consultant_id: int) -> bool: ...
    async def get_by_user_id(self, user_id: int) -> Optional[Consultant]: ...
    async def get_by_company_id(self, company_id: int) -> List[Consultant]: ...
    async def add_skill(self, consultant_id: int, skill_id: int, proficiency: ProficiencyLevel, years: int) -> bool: ...
    async def remove_skill(self, consultant_id: int, skill_id: int) -> bool: ...
    async def search(self, filters: Dict[str, Any]) -> List[Consultant]: ...
```

#### Interfaces de Service

Ces interfaces définissent les opérations pour les services externes :

- **CVAnalysisService** : Analyse et extraction de données de CV
- **MatchmakingService** : Algorithmes de matching entre consultants et appels d'offres
- **N8nIntegrationService** : Intégration avec l'outil d'automatisation n8n
- **RAGService** : Service de Retrieval Augmented Generation pour la recherche sémantique

Exemple d'une interface service :

```python
class N8nIntegrationService(Protocol):
    async def execute_workflow(self, workflow_id: str, data: Dict[str, Any]) -> Dict[str, Any]: ...
    async def trigger_webhook(self, webhook_url: str, data: Dict[str, Any]) -> Dict[str, Any]: ...
    async def get_workflows(self) -> List[Dict[str, Any]]: ...
    async def get_workflow(self, workflow_id: str) -> Dict[str, Any]: ...
    async def process_cv(self, cv_data: Dict[str, Any]) -> Dict[str, Any]: ...
    async def match_consultant_with_tenders(self, consultant_id: int) -> List[Dict[str, Any]]: ...
    async def find_consultants_for_tender(self, tender_id: int) -> List[Dict[str, Any]]: ...
```

### Cas d'utilisation

Les cas d'utilisation orchestrent la logique métier en utilisant les interfaces :

- **ConsultantUseCase** : Gestion des consultants
- **TenderUseCase** : Gestion des appels d'offres
- **MatchUseCase** : Gestion du matching
- **CollaborationUseCase** : Gestion des collaborations
- **UserUseCase** : Gestion des utilisateurs
- **PortfolioUseCase** : Gestion des portfolios
- **CVAnalysisUseCase** : Analyse des CV

Exemple d'un cas d'utilisation :

```python
class ConsultantUseCase:
    def __init__(self, consultant_repository: ConsultantRepository,
                 skill_repository: SkillRepository,
                 cv_analysis_service: CVAnalysisService,
                 rag_service: RAGService):
        self.consultant_repository = consultant_repository
        self.skill_repository = skill_repository
        self.cv_analysis_service = cv_analysis_service
        self.rag_service = rag_service

    async def get_all_consultants(self) -> List[Consultant]: ...
    async def get_consultant_by_id(self, consultant_id: int) -> Optional[Consultant]: ...
    async def create_consultant(self, consultant_data: ConsultantCreate) -> Consultant: ...
    async def update_consultant(self, consultant_id: int, consultant_data: ConsultantUpdate) -> Optional[Consultant]: ...
    async def delete_consultant(self, consultant_id: int) -> bool: ...
    async def upload_cv(self, consultant_id: int, file: bytes, filename: str) -> Dict[str, Any]: ...
    async def analyze_cv(self, consultant_id: int, cv_id: int) -> Dict[str, Any]: ...
    async def search_consultants(self, filters: Dict[str, Any]) -> List[Consultant]: ...
    async def add_skill_to_consultant(self, consultant_id: int, skill_data: SkillAssignment) -> bool: ...
```

### API Endpoints

Les endpoints API sont organisés par domaine fonctionnel :

```
/api/v1/consultants
  GET /                  - Liste des consultants
  POST /                 - Créer un consultant
  GET /{id}              - Détails d'un consultant
  PUT /{id}              - Mettre à jour un consultant
  DELETE /{id}           - Supprimer un consultant
  POST /{id}/skills      - Ajouter une compétence à un consultant
  DELETE /{id}/skills/{skill_id} - Supprimer une compétence d'un consultant
  POST /{id}/cv          - Télécharger un CV pour un consultant
  GET /{id}/matches      - Obtenir les matchs d'un consultant

/api/v1/tenders
  GET /                  - Liste des appels d'offres
  POST /                 - Créer un appel d'offres
  GET /{id}              - Détails d'un appel d'offres
  PUT /{id}              - Mettre à jour un appel d'offres
  DELETE /{id}           - Supprimer un appel d'offres
  POST /{id}/skills      - Ajouter une compétence à un appel d'offres
  GET /{id}/matches      - Obtenir les matchs pour un appel d'offres

/api/v1/matches
  GET /                  - Liste des matchs
  POST /                 - Créer un match manuellement
  GET /{id}              - Détails d'un match
  PUT /{id}              - Mettre à jour un match
  POST /{id}/accept      - Accepter un match
  POST /{id}/reject      - Rejeter un match
  POST /generate         - Générer des matchs automatiquement

/api/v1/collaborations
  GET /                  - Liste des collaborations
  POST /                 - Créer une collaboration
  GET /{id}              - Détails d'une collaboration
  PUT /{id}              - Mettre à jour une collaboration
  DELETE /{id}           - Supprimer une collaboration

/api/v1/companies
  GET /                  - Liste des entreprises
  POST /                 - Créer une entreprise
  GET /{id}              - Détails d'une entreprise
  PUT /{id}              - Mettre à jour une entreprise
  DELETE /{id}           - Supprimer une entreprise

/api/v1/cv_analysis
  POST /upload           - Télécharger un CV pour analyse
  POST /analyze          - Analyser un CV téléchargé
  GET /results/{id}      - Obtenir les résultats d'analyse d'un CV

/api/v1/n8n
  GET /workflows         - Liste des workflows disponibles
  POST /execute/{id}     - Exécuter un workflow
  GET /executions        - Liste des exécutions de workflow
  GET /executions/{id}   - Détails d'une exécution de workflow

/api/v1/rag
  POST /query            - Effectuer une requête de recherche
  POST /generate         - Générer une réponse basée sur la recherche
  POST /index            - Indexer un document
  GET /documents         - Liste des documents indexés
  GET /documents/{id}    - Détails d'un document indexé
  DELETE /documents/{id} - Supprimer un document indexé
```

## Fonctionnalités spécifiques

### Intégration avec n8n

Le backend intègre n8n pour l'automatisation des workflows complexes, notamment pour :

- **Analyse de CV** : Extraction automatique de compétences et d'informations pertinentes des CV
- **Matchmaking** : Association automatique entre consultants et appels d'offres
- **Notifications** : Envoi automatique d'alertes et de notifications
- **Intégration tierce** : Connexion avec des services externes

L'intégration est réalisée via un service dédié (`N8nWorkflowService`) qui :

- Communique avec l'API REST de n8n
- Exécute des workflows prédéfinis
- Récupère et surveille l'état des exécutions
- Fournit un mécanisme d'événements pour des workflows asynchrones

Exemple d'implémentation pour le traitement des CV :

```python
async def process_cv(self, cv_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Traite un CV via un workflow n8n
    
    Args:
        cv_data: Données du CV à traiter
        
    Returns:
        Résultat du traitement du CV
    """
    workflow_id = os.getenv("N8N_CV_ANALYSIS_WORKFLOW_ID", "1")
    return await self.execute_workflow(workflow_id, cv_data)
```

### Analyse des CV

Le module `cv_extraction` est responsable de l'extraction de données structurées à partir des CV :

- **Extraction d'informations personnelles** : Nom, contact, localisation
- **Identification des compétences** : Détection automatique des compétences techniques
- **Extraction d'expériences** : Postes occupés, durées, responsabilités
- **Extraction de formations** : Diplômes, établissements, années
- **Suggestion de profil** : Proposition automatique de titre et d'années d'expérience
- **Enrichissement sémantique** : Utilisation du RAG pour analyser le contenu du CV

Le système utilise une combinaison d'approches :

1. **Analyse basée sur des règles** : Pattern matching pour l'extraction de base
2. **Traitement du langage naturel** : Pour l'extraction contextuelle d'informations
3. **n8n workflows** : Pour orchestrer le processus d'analyse complet
4. **Recherche sémantique (RAG)** : Pour enrichir l'analyse avec des connaissances contextuelles

### Algorithme de matching

Le système utilise un algorithme sophistiqué pour le matching entre consultants et appels d'offres :

- **Matching basé sur les compétences** :
  - Correspondance entre les compétences du consultant et celles requises par l'appel d'offres
  - Prise en compte des niveaux d'expertise (débutant à expert)
  - Pondération des compétences selon leur importance (requises ou préférées)

- **Facteurs contextuels** :
  - Disponibilité temporelle du consultant
  - Localisation géographique et possibilité de télétravail
  - Tarifs et budget
  - Expérience dans des projets similaires

- **Calcul du score** :
  - Score global entre 0 et 1
  - Formule de scoring paramétrable
  - Possibilité de favoriser certains critères selon les préférences

- **Suggestions intelligentes** :
  - Classement des meilleurs matchs
  - Justification du score obtenu
  - Recommandations d'amélioration

### Système RAG (Retrieval Augmented Generation)

Le système implémente une fonctionnalité de RAG pour enrichir l'analyse des CV et le matching avec une recherche sémantique :

- **Indexation de documents** :
  - Stockage vectoriel des CV, appels d'offres, et autres documents
  - Extraction de texte à partir de PDF, DOCX et autres formats
  - Création de chunks pour une meilleure granularité de recherche

- **Recherche vectorielle** :
  - Conversion des requêtes en embeddings vectoriels
  - Recherche par similarité sémantique
  - Filtrage par métadonnées (type de document, date, etc.)

- **Génération augmentée** :
  - Utilisation des résultats de recherche comme contexte pour les LLMs
  - Génération de réponses précises basées sur la base de connaissances
  - Justification des réponses avec les sources utilisées

Le service RAG est implémenté de manière modulaire dans `rag_service.py` et peut être utilisé pour :
- Améliorer l'analyse des CV
- Suggérer des matchs pertinents
- Répondre à des questions sur les consultants ou les appels d'offres
- Générer des descriptions ou des résumés

## Sécurité

- **Authentification JWT** :
  - Tokens signés pour l'authentification des utilisateurs
  - Gestion des refresh tokens
  - Expirations configurables

- **Hachage des mots de passe** :
  - Utilisation de bcrypt pour le hachage sécurisé
  - Salage automatique des mots de passe
  - Configuration paramétrable de la complexité

- **Contrôle d'accès basé sur les rôles (RBAC)** :
  - Définition précise des permissions par rôle (ADMIN, MANAGER, CONSULTANT, CLIENT)
  - Vérification des autorisations à chaque requête API
  - Isolation des données par entreprise

- **Validation des données** :
  - Validation stricte avec Pydantic à chaque niveau
  - Protection contre les injections et les attaques XSS
  - Sanitization des entrées utilisateur

- **Protection contre les attaques courantes** :
  - Protection CSRF
  - Limites de taux (rate limiting)
  - Protection contre les injections SQL via SQLAlchemy

## Performance et scalabilité

- **Cache Redis** :
  - Mise en cache des requêtes fréquentes
  - Stockage des sessions utilisateur
  - Invalidation intelligente du cache

- **Optimisation des requêtes** :
  - Indexation appropriée des tables
  - Requêtes optimisées avec SQLAlchemy
  - Pagination des résultats de recherche

- **Architecture asynchrone** :
  - Traitement concurrentiel avec FastAPI
  - Prise en charge de nombreuses connexions simultanées
  - Traitement parallèle des tâches longues

- **Containeurisation** :
  - Déploiement avec Docker
  - Orchestration possible avec Kubernetes
  - Scaling horizontal des services

## Tests

Le projet implémente une stratégie de tests complète :

- **Tests unitaires** :
  - Tests isolés des composants individuels
  - Mocking des dépendances externes
  - Couverture de la logique métier

- **Tests d'intégration** :
  - Tests des interactions entre composants
  - Vérification du comportement du système dans son ensemble
  - Tests avec la base de données et autres dépendances

- **Tests end-to-end** :
  - Simulation de scénarios utilisateur complets
  - Vérification du comportement de l'API
  - Tests de workflows complets

## Migrations

La gestion des migrations de base de données est réalisée avec Alembic :

- **Versions de migration** :
  - Contrôle précis des modifications de schéma
  - Versionnement des changements de structure
  - Support des migrations réversibles
  - Historique des évolutions du modèle (ajout de champs, conversion de types, etc.)

- **Scripts de migration** :
  - Création automatique des tables
  - Modifications incrémentielles du schéma
  - Données de référence initiales
