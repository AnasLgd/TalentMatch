# Architecture Globale TalentMatch

## Vue d'ensemble

TalentMatch est une plateforme SaaS destinée aux ESN (Entreprises de Services du Numérique) pour faciliter la gestion des talents, des appels d'offres et la collaboration inter-ESN. L'architecture globale de TalentMatch est conçue selon les principes modernes de développement d'applications web, avec une séparation claire entre le frontend et le backend, tout en garantissant une intégration cohérente.

## Architecture système

```
┌─────────────────┐         ┌──────────────────┐         ┌──────────────────┐
│                 │         │                  │         │                  │
│    Frontend     │ ◄─────► │     Backend      │ ◄─────► │   Base de        │
│    (React)      │   API   │    (FastAPI)     │   ORM   │   données        │
│                 │   REST  │                  │         │  (PostgreSQL)    │
└─────────────────┘         └──────────────────┘         └──────────────────┘
                                     │
                          ┌──────────┴───────────┐
                          │                      │
                 ┌────────▼─────────┐   ┌────────▼─────────┐
                 │                  │   │                  │
                 │    Stockage      │   │  Automatisation  │
                 │    (MinIO)       │   │     (n8n)        │
                 │                  │   │                  │
                 └──────────────────┘   └──────────────────┘
```

## Composants principaux

### Frontend

- Application React avec TypeScript
- Interface utilisateur basée sur shadcn/UI et Tailwind CSS
- Gestion d'état avec TanStack Query et React Context
- Routage avec React Router

### Backend

- API REST développée avec FastAPI
- Architecture hexagonale (ports et adaptateurs)
- Logique métier centralisée dans les cas d'utilisation
- Accès aux données via SQLAlchemy

### Base de données

- PostgreSQL comme système de gestion de base de données relationnelle
- Schéma optimisé pour les requêtes fréquentes
- Migrations gérées avec Alembic

### Services auxiliaires

- MinIO pour le stockage d'objets (CV, portfolios)
- Redis pour le cache
- n8n pour l'automatisation des workflows
- JWT pour l'authentification

## Flux de données

### Authentification

1. L'utilisateur saisit ses identifiants sur le frontend
2. Le frontend envoie une requête à `/api/v1/auth/login`
3. Le backend vérifie les identifiants et génère un JWT
4. Le token JWT est stocké dans le localStorage du navigateur
5. Toutes les requêtes ultérieures incluent le token dans l'en-tête Authorization

### Gestion des consultants

1. Le frontend récupère la liste des consultants via `/api/v1/consultants`
2. Les données sont mises en cache côté client avec TanStack Query
3. Les modifications sont envoyées au backend qui les persiste en base de données
4. Les événements importants déclenchent des workflows n8n pour des traitements supplémentaires

### Traitement des CV

1. L'utilisateur télécharge un CV depuis l'interface
2. Le fichier est envoyé au backend qui le stocke dans MinIO
3. Un workflow n8n est déclenché pour analyser le CV
4. Les données extraites sont enregistrées en base de données
5. Le frontend est notifié de la fin du traitement et affiche les résultats

### Matching

1. Le frontend demande des suggestions de matching pour un appel d'offres
2. Le backend exécute l'algorithme de matching
3. Les résultats sont retournés au frontend, triés par score de matching
4. L'utilisateur peut valider ou modifier les suggestions

## Principes d'intégration

### API REST

L'intégration entre frontend et backend se fait via une API REST avec les caractéristiques suivantes :

- Endpoints organisés par domaine fonctionnel
- Format JSON pour les requêtes et réponses
- Statuts HTTP standards pour indiquer le résultat des opérations
- Authentification JWT pour sécuriser les communications

### Validation des données

- Côté frontend : Validation avec Zod avant envoi au backend
- Côté backend : Validation avec Pydantic à la réception des requêtes

### Gestion des erreurs

- Erreurs structurées retournées par le backend
- Intercepteurs côté frontend pour traiter les erreurs de manière cohérente
- Journalisation centralisée des erreurs

## Déploiement

L'application est conteneurisée avec Docker et orchestrée avec Docker Compose :

- Container frontend : Nginx + build React
- Container backend : FastAPI + Uvicorn
- Container base de données : PostgreSQL
- Container MinIO : Stockage d'objets
- Container Redis : Cache
- Container n8n : Automatisation des workflows

## Environnements

Trois environnements sont configurés :

- **Développement** : Pour le développement local
- **Staging** : Pour les tests avant mise en production
- **Production** : Environnement de production

## Sécurité

- Authentification JWT
- HTTPS pour toutes les communications
- Validation des entrées côté client et serveur
- Protection contre les attaques XSS et CSRF
- Contrôle d'accès basé sur les rôles
