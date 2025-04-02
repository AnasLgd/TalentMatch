# Documentation de la Base de Données TalentMatch

## 1. Vue d'ensemble

### 1.1 Introduction
La base de données de TalentMatch est conçue pour stocker et gérer efficacement toutes les données nécessaires à la plateforme, notamment les informations sur les consultants, les entreprises, les appels d'offres, les compétences, les correspondances (matches) et les collaborations inter-ESN. Elle utilise PostgreSQL comme système de gestion de base de données relationnelle.

### 1.2 Objectifs
- Assurer l'intégrité et la cohérence des données
- Permettre des requêtes performantes pour les fonctionnalités de matching
- Faciliter la gestion des relations complexes entre les entités
- Supporter l'évolution du schéma via des migrations contrôlées

### 1.3 Technologies
- **SGBD** : PostgreSQL 14+
- **ORM** : SQLAlchemy 2.0+
- **Migrations** : Alembic
- **Types spéciaux** : JSONB pour les données semi-structurées

## 2. Schéma de la Base de Données

### 2.1 Diagramme Entité-Relation
Le schéma suivant représente les principales entités et leurs relations :

```
+-------------+       +---------------+       +------------+
|   Users     |------>|  Consultants  |<----->|   Skills   |
+-------------+       +---------------+       +------------+
      |                     |   |                   |
      |                     |   |                   |
      v                     v   v                   v
+-------------+       +--------+       +------------------+
|  Companies  |<----->| Matches|<----->| Consultant_Skills|
+-------------+       +--------+       +------------------+
      |                  |
      |                  |
      v                  v
+----------------+    +--------+
| Collaborations |    | Tenders|
+----------------+    +--------+
                         |
                         |
                         v
                  +-------------+
                  |Tender_Skills|
                  +-------------+
```

### 2.2 Description des Tables

#### 2.2.1 Users
Stocke les informations des utilisateurs de la plateforme.

| Colonne         | Type           | Contraintes       | Description                           |
|-----------------|----------------|-------------------|---------------------------------------|
| id              | INTEGER        | PK                | Identifiant unique                    |
| email           | VARCHAR(255)   | UNIQUE, NOT NULL  | Adresse email (identifiant de connexion) |
| hashed_password | VARCHAR(255)   | NOT NULL          | Mot de passe hashé                    |
| first_name      | VARCHAR(100)   | NOT NULL          | Prénom                                |
| last_name       | VARCHAR(100)   | NOT NULL          | Nom                                   |
| role            | ENUM           | NOT NULL          | Rôle (admin, manager, recruiter, sales, consultant) |
| company_id      | INTEGER        | FK                | Référence à l'entreprise              |
| is_active       | BOOLEAN        | DEFAULT TRUE      | Statut d'activation du compte         |
| created_at      | TIMESTAMP      | NOT NULL          | Date de création                      |
| updated_at      | TIMESTAMP      |                   | Date de dernière modification         |

#### 2.2.2 Companies
Stocke les informations sur les entreprises (ESN).

| Colonne         | Type           | Contraintes       | Description                           |
|-----------------|----------------|-------------------|---------------------------------------|
| id              | INTEGER        | PK                | Identifiant unique                    |
| name            | VARCHAR(255)   | NOT NULL          | Nom de l'entreprise                   |
| description     | TEXT           |                   | Description de l'entreprise           |
| website         | VARCHAR(255)   |                   | Site web                              |
| address         | VARCHAR(255)   |                   | Adresse                               |
| city            | VARCHAR(100)   |                   | Ville                                 |
| postal_code     | VARCHAR(20)    |                   | Code postal                           |
| country         | VARCHAR(100)   |                   | Pays                                  |
| is_active       | BOOLEAN        | DEFAULT TRUE      | Statut d'activation                   |
| created_at      | TIMESTAMP      | NOT NULL          | Date de création                      |
| updated_at      | TIMESTAMP      |                   | Date de dernière modification         |

#### 2.2.3 Consultants
Stocke les informations sur les consultants.

| Colonne              | Type           | Contraintes       | Description                           |
|----------------------|----------------|-------------------|---------------------------------------|
| id                   | INTEGER        | PK                | Identifiant unique                    |
| user_id              | INTEGER        | FK, UNIQUE        | Référence à l'utilisateur             |
| company_id           | INTEGER        | FK, NOT NULL      | Référence à l'entreprise              |
| title                | VARCHAR(255)   | NOT NULL          | Titre/Poste                           |
| experience_years     | INTEGER        |                   | Années d'expérience                   |
| availability_status  | ENUM           | NOT NULL          | Statut de disponibilité (available, partially_available, unavailable, on_mission) |
| availability_date    | DATE           |                   | Date de disponibilité                 |
| hourly_rate          | FLOAT          |                   | Taux horaire                          |
| daily_rate           | FLOAT          |                   | Taux journalier                       |
| bio                  | TEXT           |                   | Biographie/Présentation               |
| location             | VARCHAR(255)   |                   | Localisation                          |
| remote_work          | BOOLEAN        | DEFAULT FALSE     | Disponibilité pour le travail à distance |
| max_travel_distance  | INTEGER        |                   | Distance maximale de déplacement (km) |
| created_at           | TIMESTAMP      | NOT NULL          | Date de création                      |
| updated_at           | TIMESTAMP      |                   | Date de dernière modification         |

#### 2.2.4 Skills
Stocke les compétences disponibles dans le système.

| Colonne         | Type           | Contraintes       | Description                           |
|-----------------|----------------|-------------------|---------------------------------------|
| id              | INTEGER        | PK                | Identifiant unique                    |
| name            | VARCHAR(255)   | UNIQUE, NOT NULL  | Nom de la compétence                  |
| category        | ENUM           | NOT NULL          | Catégorie (programming_language, framework, database, cloud, devops, methodology, soft_skill, other) |
| description     | TEXT           |                   | Description de la compétence          |
| created_at      | TIMESTAMP      | NOT NULL          | Date de création                      |
| updated_at      | TIMESTAMP      |                   | Date de dernière modification         |

#### 2.2.5 ConsultantSkill
Table d'association entre consultants et compétences.

| Colonne           | Type           | Contraintes       | Description                           |
|-------------------|----------------|-------------------|---------------------------------------|
| id                | INTEGER        | PK                | Identifiant unique                    |
| consultant_id     | INTEGER        | FK, NOT NULL      | Référence au consultant               |
| skill_id          | INTEGER        | FK, NOT NULL      | Référence à la compétence             |
| proficiency_level | ENUM           | NOT NULL          | Niveau de maîtrise (beginner, intermediate, advanced, expert) |
| years_experience  | INTEGER        |                   | Années d'expérience avec cette compétence |
| details           | TEXT           |                   | Détails supplémentaires               |
| created_at        | TIMESTAMP      | NOT NULL          | Date de création                      |
| updated_at        | TIMESTAMP      |                   | Date de dernière modification         |

#### 2.2.6 Resume
Stocke les CV des consultants.

| Colonne         | Type           | Contraintes       | Description                           |
|-----------------|----------------|-------------------|---------------------------------------|
| id              | INTEGER        | PK                | Identifiant unique                    |
| consultant_id   | INTEGER        | FK, NOT NULL      | Référence au consultant               |
| file_path       | VARCHAR(255)   | NOT NULL          | Chemin du fichier                     |
| file_type       | VARCHAR(50)    | NOT NULL          | Type de fichier (pdf, docx, etc.)     |
| version         | INTEGER        | DEFAULT 1         | Version du CV                         |
| extracted_data  | TEXT           |                   | Données extraites du CV               |
| created_at      | TIMESTAMP      | NOT NULL          | Date de création                      |
| updated_at      | TIMESTAMP      |                   | Date de dernière modification         |

#### 2.2.7 Tenders
Stocke les appels d'offres.

| Colonne              | Type           | Contraintes       | Description                           |
|----------------------|----------------|-------------------|---------------------------------------|
| id                   | INTEGER        | PK                | Identifiant unique                    |
| company_id           | INTEGER        | FK, NOT NULL      | Référence à l'entreprise              |
| title                | VARCHAR(255)   | NOT NULL          | Titre de l'appel d'offres             |
| client_name          | VARCHAR(255)   | NOT NULL          | Nom du client                         |
| description          | TEXT           | NOT NULL          | Description détaillée                 |
| start_date           | DATE           |                   | Date de début                         |
| end_date             | DATE           |                   | Date de fin                           |
| status               | ENUM           | NOT NULL          | Statut (open, in_progress, closed, cancelled) |
| location             | VARCHAR(255)   |                   | Localisation                          |
| remote_work          | BOOLEAN        | DEFAULT FALSE     | Possibilité de travail à distance     |
| budget               | FLOAT          |                   | Budget                                |
| required_consultants | INTEGER        | DEFAULT 1         | Nombre de consultants requis          |
| created_at           | TIMESTAMP      | NOT NULL          | Date de création                      |
| updated_at           | TIMESTAMP      |                   | Date de dernière modification         |

#### 2.2.8 TenderSkill
Table d'association entre appels d'offres et compétences requises.

| Colonne         | Type           | Contraintes       | Description                           |
|-----------------|----------------|-------------------|---------------------------------------|
| id              | INTEGER        | PK                | Identifiant unique                    |
| tender_id       | INTEGER        | FK, NOT NULL      | Référence à l'appel d'offres          |
| skill_id        | INTEGER        | FK, NOT NULL      | Référence à la compétence             |
| importance      | VARCHAR(50)    | NOT NULL          | Importance (required, preferred, nice_to_have) |
| details         | TEXT           |                   | Détails supplémentaires               |
| created_at      | TIMESTAMP      | NOT NULL          | Date de création                      |
| updated_at      | TIMESTAMP      |                   | Date de dernière modification         |

#### 2.2.9 Match
Stocke les correspondances entre consultants et appels d'offres.

| Colonne         | Type           | Contraintes       | Description                           |
|-----------------|----------------|-------------------|---------------------------------------|
| id              | INTEGER        | PK                | Identifiant unique                    |
| consultant_id   | INTEGER        | FK, NOT NULL      | Référence au consultant               |
| tender_id       | INTEGER        | FK, NOT NULL      | Référence à l'appel d'offres          |
| match_score     | FLOAT          | NOT NULL          | Score de correspondance (0-1)         |
| status          | ENUM           | NOT NULL          | Statut (suggested, submitted, accepted, rejected) |
| notes           | TEXT           |                   | Notes                                 |
| created_at      | TIMESTAMP      | NOT NULL          | Date de création                      |
| updated_at      | TIMESTAMP      |                   | Date de dernière modification         |

#### 2.2.10 Portfolio
Stocke les portfolios générés pour les consultants.

| Colonne         | Type           | Contraintes       | Description                           |
|-----------------|----------------|-------------------|---------------------------------------|
| id              | INTEGER        | PK                | Identifiant unique                    |
| consultant_id   | INTEGER        | FK, NOT NULL      | Référence au consultant               |
| tender_id       | INTEGER        | FK, NOT NULL      | Référence à l'appel d'offres          |
| file_path       | VARCHAR(255)   |                   | Chemin du fichier                     |
| version         | INTEGER        | DEFAULT 1         | Version du portfolio                  |
| status          | ENUM           | NOT NULL          | Statut (draft, final)                 |
| content         | TEXT           |                   | Contenu du portfolio                  |
| generated_date  | TIMESTAMP      | NOT NULL          | Date de génération                    |
| created_at      | TIMESTAMP      | NOT NULL          | Date de création                      |
| updated_at      | TIMESTAMP      |                   | Date de dernière modification         |

#### 2.2.11 Collaboration
Stocke les collaborations entre ESN.

| Colonne               | Type           | Contraintes       | Description                           |
|-----------------------|----------------|-------------------|---------------------------------------|
| id                    | INTEGER        | PK                | Identifiant unique                    |
| initiator_company_id  | INTEGER        | FK, NOT NULL      | Référence à l'entreprise initiatrice  |
| partner_company_id    | INTEGER        | FK, NOT NULL      | Référence à l'entreprise partenaire   |
| status                | ENUM           | NOT NULL          | Statut (pending, active, inactive)    |
| start_date            | DATE           |                   | Date de début                         |
| end_date              | DATE           |                   | Date de fin                           |
| terms                 | TEXT           |                   | Termes de la collaboration            |
| created_at            | TIMESTAMP      | NOT NULL          | Date de création                      |
| updated_at            | TIMESTAMP      |                   | Date de dernière modification         |

### 2.3 Énumérations (ENUM)

#### 2.3.1 UserRole
```sql
CREATE TYPE UserRole AS ENUM (
    'admin',
    'manager',
    'recruiter',
    'sales',
    'consultant'
);
```

#### 2.3.2 AvailabilityStatus
```sql
CREATE TYPE AvailabilityStatus AS ENUM (
    'available',
    'partially_available',
    'unavailable',
    'on_mission'
);
```

#### 2.3.3 TenderStatus
```sql
CREATE TYPE TenderStatus AS ENUM (
    'open',
    'in_progress',
    'closed',
    'cancelled'
);
```

#### 2.3.4 MatchStatus
```sql
CREATE TYPE MatchStatus AS ENUM (
    'suggested',
    'submitted',
    'accepted',
    'rejected'
);
```

#### 2.3.5 PortfolioStatus
```sql
CREATE TYPE PortfolioStatus AS ENUM (
    'draft',
    'final'
);
```

#### 2.3.6 CollaborationStatus
```sql
CREATE TYPE CollaborationStatus AS ENUM (
    'pending',
    'active',
    'inactive'
);
```

#### 2.3.7 ProficiencyLevel
```sql
CREATE TYPE ProficiencyLevel AS ENUM (
    'beginner',
    'intermediate',
    'advanced',
    'expert'
);
```

#### 2.3.8 SkillCategory
```sql
CREATE TYPE SkillCategory AS ENUM (
    'programming_language',
    'framework',
    'database',
    'cloud',
    'devops',
    'methodology',
    'soft_skill',
    'other'
);
```

## 3. Migrations

### 3.1 Gestion des migrations avec Alembic
Les migrations de la base de données sont gérées avec Alembic, qui permet :
- De versionner le schéma de la base de données
- D'appliquer des modifications de schéma de manière contrôlée
- De revenir à une version antérieure si nécessaire

### 3.2 Structure des migrations
```
migrations/
├── env.py                # Configuration de l'environnement Alembic
├── README               # Documentation sur les migrations
├── script.py.mako       # Template pour les scripts de migration
└── versions/            # Scripts de migration versionnés
    └── 001_initial.py   # Migration initiale
```

### 3.3 Migration initiale
La migration initiale crée toutes les tables de base nécessaires au fonctionnement de l'application :

```python
"""
Script de migration initial pour créer les tables de base de données TalentMatch
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB

# revision identifiers, used by Alembic
revision = '001_initial'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Création des tables (users, companies, consultants, skills, etc.)
    # ...

def downgrade():
    # Suppression des tables dans l'ordre inverse
    op.drop_table('collaborations')
    op.drop_table('skill_portfolios')
    op.drop_table('matches')
    op.drop_table('tender_skills')
    op.drop_table('tenders')
    op.drop_table('resumes')
    op.drop_table('consultant_skills')
    op.drop_table('skills')
    op.drop_table('consultants')
    op.drop_table('companies')
    op.drop_table('users')
```

### 3.4 Création d'une nouvelle migration
Pour créer une nouvelle migration :

```bash
alembic revision -m "description_de_la_migration"
```

### 3.5 Application des migrations
Pour appliquer les migrations :

```bash
# Appliquer toutes les migrations
alembic upgrade head

# Appliquer jusqu'à une révision spécifique
alembic upgrade <revision_id>

# Revenir à une révision antérieure
alembic downgrade <revision_id>
```

## 4. Modèles SQLAlchemy

### 4.1 Définition des modèles
Les modèles SQLAlchemy sont définis dans le fichier `app/infrastructure/database/models.py` et correspondent aux tables de la base de données.

```python
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, ForeignKey, Float, Text, Date, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.sql import func
import enum

Base = declarative_base()

# Définition des énumérations
class UserRole(enum.Enum):
    ADMIN = "admin"
    MANAGER = "manager"
    RECRUITER = "recruiter"
    SALES = "sales"
    CONSULTANT = "consultant"

# ... autres énumérations ...

# Définition des modèles SQLAlchemy
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    role = Column(Enum(UserRole), nullable=False)
    company_id = Column(Integer, ForeignKey("companies.id"))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    company = relationship("Company", back_populates="users")
    consultant = relationship("Consultant", back_populates="user", uselist=False)

# ... autres modèles ...
```

### 4.2 Relations entre modèles
Les relations entre les modèles sont définies à l'aide de `relationship` de SQLAlchemy :

```python
class Consultant(Base):
    __tablename__ = "consultants"
    
    # ... colonnes ...
    
    user = relationship("User", back_populates="consultant")
    company = relationship("Company", back_populates="consultants")
    skills = relationship("ConsultantSkill", back_populates="consultant")
    matches = relationship("Match", back_populates="consultant")
    portfolios = relationship("Portfolio", back_populates="consultant")
    resumes = relationship("Resume", back_populates="consultant")
```

### 4.3 Création des tables
Les tables sont créées à partir des modèles SQLAlchemy :

```python
def create_tables(engine):
    Base.metadata.create_all(bind=engine)
```

## 5. Configuration de la Base de Données

### 5.1 Connexion à la base de données
La connexion à la base de données est configurée dans `app/infrastructure/database/session.py` :

```python
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
```

### 5.2 Configuration via variables d'environnement
Les paramètres de connexion à la base de données sont configurés via des variables d'environnement dans `app/core/config.py` :

```python
class Settings(BaseSettings):
    # ...
    
    # Configuration de la base de données PostgreSQL
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "localhost")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", "5432")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "postgres")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "talentmatch")
    
    # ...
```

## 6. Requêtes et Opérations Courantes

### 6.1 Requêtes de base
Exemples de requêtes de base avec SQLAlchemy :

```python
# Récupérer tous les consultants
consultants = db.query(ConsultantModel).all()

# Récupérer un consultant par ID
consultant = db.query(ConsultantModel).filter(ConsultantModel.id == consultant_id).first()

# Récupérer les consultants d'une entreprise
consultants = db.query(ConsultantModel).filter(ConsultantModel.company_id == company_id).all()

# Récupérer les consultants disponibles
consultants = db.query(ConsultantModel).filter(
    ConsultantModel.availability_status == "available"
).all()
```

### 6.2 Requêtes avec jointures
Exemples de requêtes avec jointures :

```python
# Récupérer les compétences d'un consultant
skills = db.query(
    ConsultantSkillModel, SkillModel
).join(
    SkillModel, ConsultantSkillModel.skill_id == SkillModel.id
).filter(
    ConsultantSkillModel.consultant_id == consultant_id
).all()

# Recherche de consultants par critères
consultants_query = db.query(ConsultantModel).join(
    UserModel, ConsultantModel.user_id == UserModel.id
).filter(
    (UserModel.first_name.ilike(f"%{query}%")) |
    (UserModel.last_name.ilike(f"%{query}%")) |
    (ConsultantModel.title.ilike(f"%{query}%")) |
    (ConsultantModel.bio.ilike(f"%{query}%"))
)
```

### 6.3 Opérations CRUD
Exemples d'opérations CRUD (Create, Read, Update, Delete) :

```python
# Création d'un consultant
db_consultant = ConsultantModel(
    user_id=consultant.user_id,
    company_id=consultant.company_id,
    title=consultant.title,
    # ... autres champs ...
)
db.add(db_consultant)
db.commit()
db.refresh(db_consultant)

# Mise à jour d'un consultant
db_consultant = db.query(ConsultantModel).filter(ConsultantModel.id == consultant_id).first()
for key, value in update_data.items():
    setattr(db_consultant, key, value)
db.commit()
db.refresh(db_consultant)

# Suppression d'un consultant
db_consultant = db.query(ConsultantModel).filter(ConsultantModel.id == consultant_id).first()
db.delete(db_consultant)
db.commit()
```

## 7. Optimisation et Performance

### 7.1 Indexation
Les index sont définis pour optimiser les requêtes fréquentes :

```python
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    # ...
```

### 7.2 Requêtes optimisées
Techniques pour optimiser les requêtes :

- Utilisation de `select_from` pour des jointures complexes
- Utilisation de `options(joinedload())` pour le chargement eager des relations
- Filtrage côté base de données plutôt que côté application
- Pagination pour limiter le nombre de résultats

```python
# Exemple de requête optimisée avec pagination
def get_consultants_paginated(db, skip=0, limit=100):
    return db.query(ConsultantModel).options(
        joinedload(ConsultantModel.user),
        joinedload(ConsultantModel.company)
    ).offset(skip).limit(limit).all()
```

### 7.3 Cache avec Redis
Utilisation de Redis pour mettre en cache les résultats de requêtes fréquentes :

```python
async def get_consultant_by_id(consultant_id: int, db: Session, redis_client):
    # Vérifier si les données sont en cache
    cache_key = f"consultant:{consultant_id}"
    cached_data = await redis_client.get(cache_key)
    
    if cached_data:
        return json.loads(cached_data)
    
    # Si non, récupérer depuis la base de données
    consultant = db.query(ConsultantModel).filter(ConsultantModel.id == consultant_id).first()
    if not consultant:
        return None
    
    # Convertir en entité et mettre en cache
    consultant_entity = await _map_to_entity(consultant, db)
    await redis_client.set(cache_key, json.dumps(consultant_entity.dict()), ex=3600)  # Expire après 1h
    
    return consultant_entity
```

## 8. Sécurité des Données

### 8.1 Gestion des mots de passe
Les mots de passe sont hashés avant stockage :

```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
```

### 8.2 Protection contre les injections SQL
SQLAlchemy protège automatiquement contre les injections SQL en utilisant des requêtes paramétrées.

### 8.3 Contrôle d'accès aux données
Mise en place de contrôles d'accès basés sur les rôles :

```python
def check_company_access(user: User, company_id: int) -> bool:
    # Les administrateurs ont accès à toutes les entreprises
    if user.role == UserRole.ADMIN:
        return True
    
    # Les utilisateurs ont accès uniquement à leur propre entreprise
    return user.company_id == company_id
```

## 9. Sauvegarde et Restauration

### 9.1 Stratégie de sauvegarde
- Sauvegardes complètes quotidiennes
- Sauvegardes incrémentielles toutes les 6 heures
- Conservation des sauvegardes pendant 30 jours

### 9.2 Commandes de sauvegarde
```bash
# Sauvegarde complète
pg_dump -U postgres -d talentmatch -F c -f /backups/talentmatch_full_$(date +%Y%m%d).dump

# Sauvegarde des données uniquement
pg_dump -U postgres -d talentmatch --data-only -F c -f /backups/talentmatch_data_$(date +%Y%m%d).dump
```

### 9.3 Commandes de restauration
```bash
# Restauration complète
pg_restore -U postgres -d talentmatch -c /backups/talentmatch_full_20250401.dump

# Restauration des données uniquement
pg_restore -U postgres -d talentmatch --data-only /backups/talentmatch_data_20250401.dump
```

## 10. Monitoring et Maintenance

### 10.1 Surveillance des performances
- Utilisation de pg_stat_statements pour surveiller les requêtes lentes
- Mise en place d'alertes sur les temps de réponse élevés
- Surveillance de l'utilisation des ressources (CPU, mémoire, disque)

### 10.2 Maintenance régulière
- VACUUM ANALYZE hebdomadaire pour optimiser les index et les statistiques
- Vérification de l'intégrité des données
- Nettoyage des données temporaires ou obsolètes

### 10.3 Requêtes de diagnostic
```sql
-- Requêtes les plus lentes
SELECT query, calls, total_time, mean_time
FROM pg_stat_statements
ORDER BY mean_time DESC
LIMIT 10;

-- Tables les plus volumineuses
SELECT relname, pg_size_pretty(pg_total_relation_size(relid)) AS size
FROM pg_catalog.pg_statio_user_tables
ORDER BY pg_total_relation_size(relid) DESC;

-- Index inutilisés
SELECT indexrelid::regclass AS index, relid::regclass AS table
FROM pg_stat_user_indexes
JOIN pg_index USING (indexrelid)
WHERE idx_scan = 0 AND indisunique IS FALSE;
```

## 11. Évolution du Schéma

### 11.1 Principes pour les modifications de schéma
- Toujours utiliser Alembic pour les modifications de schéma
- Privilégier les modifications non destructives (ajout de colonnes plutôt que suppression)
- Tester les migrations sur un environnement de staging avant la production

### 11.2 Exemple de migration pour ajouter une colonne
```python
"""Ajouter colonne profile_picture_url à la table consultants"""

from alembic import op
import sqlalchemy as sa

revision = '002_add_profile_picture'
down_revision = '001_initial'

def upgrade():
    op.add_column('consultants', sa.Column('profile_picture_url', sa.String(255), nullable=True))

def downgrade():
    op.drop_column('consultants', 'profile_picture_url')
```

### 11.3 Exemple de migration pour modifier une contrainte
```python
"""Modifier la contrainte d'unicité sur la table skills"""

from alembic import op

revision = '003_modify_skill_constraint'
down_revision = '002_add_profile_picture'

def upgrade():
    # Supprimer l'ancienne contrainte
    op.drop_constraint('skills_name_key', 'skills', type_='unique')
    
    # Ajouter la nouvelle contrainte (nom + catégorie)
    op.create_unique_constraint('skills_name_category_key', 'skills', ['name', 'category'])

def downgrade():
    # Revenir à l'ancienne contrainte
    op.drop_constraint('skills_name_category_key', 'skills', type_='unique')
    op.create_unique_constraint('skills_name_key', 'skills', ['name'])
```

## 12. Ressources et Références

### 12.1 Documentation technique
- [Documentation PostgreSQL](https://www.postgresql.org/docs/)
- [Documentation SQLAlchemy](https://docs.sqlalchemy.org/)
- [Documentation Alembic](https://alembic.sqlalchemy.org/en/latest/)

### 12.2 Outils recommandés
- **pgAdmin** : Interface graphique pour PostgreSQL
- **DBeaver** : Client SQL universel
- **SQLAlchemy Debug Toolbar** : Extension pour déboguer les requêtes SQLAlchemy

### 12.3 Bonnes pratiques
- Utiliser des transactions pour les opérations multiples
- Limiter la taille des résultats avec pagination
- Utiliser des index appropriés pour les colonnes fréquemment utilisées dans les requêtes
- Éviter les requêtes N+1 en utilisant le chargement eager des relations
- Mettre en cache les résultats de requêtes fréquentes et coûteuses
