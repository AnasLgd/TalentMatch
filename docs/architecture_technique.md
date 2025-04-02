# Architecture Technique de TalentMatch

## Vue d'ensemble

TalentMatch est une plateforme SaaS pour ESN (Entreprises de Services du Numérique) qui facilite la gestion des talents et des appels d'offres. L'architecture suit un modèle hexagonal (ou architecture en ports et adaptateurs) qui sépare clairement le domaine métier de l'infrastructure technique.

## Composants principaux

### Backend (FastAPI)

Le backend est développé avec FastAPI et suit une architecture hexagonale avec les couches suivantes :

1. **Core (Cœur du domaine)**
   - **Entités** : Définissent les objets métier (Consultant, Tender, Match, etc.)
   - **Interfaces** : Définissent les contrats pour les repositories et services
   - **Use Cases** : Implémentent la logique métier

2. **Adaptateurs**
   - **Repositories** : Implémentent les interfaces de persistance avec SQLAlchemy
   - **Services** : Implémentent les interfaces pour les services externes (n8n, analyse de CV)

3. **API**
   - **Endpoints** : Exposent les fonctionnalités via des routes REST

4. **Infrastructure**
   - **Database** : Configuration et modèles SQLAlchemy pour PostgreSQL

### Frontend (Next.js)

Le frontend est prévu pour être développé avec Next.js, mais le code est actuellement absent. La structure de base existe avec :
- Un Dockerfile configuré pour Node.js
- Des dossiers vides pour le code source (src) et les ressources statiques (public)

### Base de données

PostgreSQL est utilisé comme système de gestion de base de données avec :
- Une configuration via SQLAlchemy
- Des migrations gérées par Alembic
- Un schéma complet incluant les tables pour :
  - Utilisateurs et entreprises
  - Consultants et leurs compétences
  - Appels d'offres
  - Correspondances (matches)
  - Collaborations inter-ESN

### Services complémentaires

L'architecture prévoit l'intégration de plusieurs services :

1. **MinIO** : Stockage d'objets compatible S3 pour les fichiers (CV, portfolios)
2. **Redis** : Cache pour améliorer les performances
3. **n8n** : Automatisation des workflows (notamment pour le matching)

## Configuration

La configuration est gérée via des variables d'environnement avec des valeurs par défaut, permettant une personnalisation facile selon l'environnement (développement, test, production).

## Déploiement

L'architecture est conçue pour être déployée via Docker, avec :
- Des conteneurs séparés pour chaque service
- Une orchestration via Docker Compose
- Un déploiement prévu sur VPS Hostinger KVM2

## Points forts de l'architecture

1. **Séparation des préoccupations** : L'architecture hexagonale permet une séparation claire entre la logique métier et l'infrastructure technique.
2. **Testabilité** : Les interfaces et l'inversion de dépendance facilitent les tests unitaires et d'intégration.
3. **Évolutivité** : La structure modulaire permet d'ajouter facilement de nouvelles fonctionnalités.
4. **Maintenabilité** : L'organisation du code en couches distinctes facilite la maintenance.

## Lacunes actuelles

1. **Frontend manquant** : Le code frontend est entièrement absent et doit être développé.
2. **Documentation limitée** : Peu de documentation sur l'utilisation des API et l'intégration des services.
3. **Tests incomplets** : Les tests unitaires et d'intégration sont limités.
