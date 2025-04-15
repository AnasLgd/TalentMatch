
# TalentMatch - Documentation Technique

## Présentation Générale

TalentMatch est une plateforme qui permet aux ESN (Entreprises de Services du Numérique) de gérer efficacement leurs consultants, compétences, appels d'offres et collaborations inter-ESN. La plateforme facilite le matching entre consultants et opportunités d'affaires tout en optimisant la gestion des talents.

### Technologies Principales

- **Frontend** : React, TypeScript, Tailwind CSS, Shadcn UI
- **Backend** : FastAPI (Python)
- **Base de données** : PostgreSQL
- **Stockage** : Supabase Storage
- **Automatisation** : n8n
- **Intelligence Artificielle** : Agents IA maison pour l'analyse des CV et le matching

### Principes Fondamentaux

- Approche "schema-first" pour garantir l'alignement frontend-backend
- Architecture hexagonale pour une séparation claire des préoccupations
- Validation rigoureuse des données à tous les niveaux

## Architecture

### Approche Schema-First

Notre développement suit une approche "schema-first" stricte :
- Les modèles Pydantic du backend définissent le contrat des API
- Les interfaces TypeScript et les schémas Zod du frontend reflètent exactement ces modèles
- Toute modification de schéma doit être synchronisée entre frontend et backend

### Structure du Projet

#### Frontend
```
src/
├── components/        # Composants UI réutilisables
│   ├── consultant/    # Composants spécifiques aux consultants
│   ├── tender/        # Composants spécifiques aux appels d'offres
│   └── ui/            # Composants UI génériques (shadcn)
├── hooks/             # Hooks React personnalisés
├── pages/             # Pages de l'application
├── services/          # Services d'appel API
├── types/             # Définitions TypeScript
├── schema/            # Schémas de validation Zod
└── utils/             # Utilitaires
```

#### Backend
```
app/
├── core/              # Logique métier (domaine)
│   ├── entities/      # Modèles de données
│   ├── interfaces/    # Ports (interfaces)
│   └── use_cases/     # Cas d'utilisation
├── adapters/          # Adaptateurs
│   ├── repositories/  # Implémentations des repositories
│   └── services/      # Services externes
└── api/               # API REST (FastAPI)
    └── v1/            # Points d'entrée API v1
```

### Principes de Design

1. **Clean Architecture**
   - Séparation claire entre domaine, application et infrastructure
   - Dépendances orientées vers le centre (domaine)
   - Inversion de dépendance via des interfaces

2. **Design Patterns**
   - Repository Pattern pour l'accès aux données
   - Factory Pattern pour la création d'objets complexes
   - Adapter Pattern pour l'intégration avec des services externes

3. **Responsabilité Unique**
   - Chaque composant a une responsabilité unique et bien définie
   - Composants petits et focalisés sur une tâche spécifique

## Développement

### Standards de Codage

#### TypeScript/React
- Interfaces explicites pour tous les props et états
- Composants fonctionnels avec hooks
- Utilisation systématique de la déstructuration
- Types stricts (no any sauf exception justifiée)

#### Python/FastAPI
- Type hints pour tous les paramètres et retours
- Docstrings pour toutes les fonctions et classes
- Dependency Injection via FastAPI
- Validation via Pydantic

### Synchronisation Frontend-Backend

1. **Types Partagés**
   - Les interfaces TypeScript reflètent exactement les modèles Pydantic
   - Chaque entité du backend possède son équivalent frontal
   ```typescript
   // frontend: src/types/consultant.ts doit correspondre à
   // backend: app/core/entities/consultant.py
   ```

2. **Validation**
   - Les schémas Zod du frontend correspondent aux validations Pydantic du backend
   ```typescript
   // Le schéma Zod doit valider selon les mêmes règles que Pydantic
   const consultantSchema = z.object({
     title: z.string().min(2),
     // ...doit correspondre aux validateurs Pydantic
   });
   ```

3. **Services API**
   - Un service dédié par ressource
   - Types de retour et paramètres alignés sur les DTOs

### Gestion des États

1. **React Query**
   - Utilisation de React Query pour la gestion des états serveur
   - Cache et invalidation automatique des données
   - Gestion optimiste des mises à jour

2. **État Local**
   - État local via useState pour les composants isolés
   - Contextes React pour l'état partagé limité

### Gestion des Dépendances

- Mise à jour régulière des dépendances (audit mensuel)
- Politique de versions stricte (semver)
- Éviter les dépendances à faible maintenance ou obsolètes

## Qualité et Tests

### Stratégie de Tests

1. **Tests Unitaires**
   - Couverture minimale: 80% du code
   - Focus sur la logique métier complexe
   - Tests isolés avec mocks appropriés

2. **Tests d'Intégration**
   - Vérification des flux complets
   - Tests API de bout en bout
   - Validation des scénarios clés

3. **Tests E2E**
   - Automatisation des parcours utilisateurs critiques
   - Validation des interfaces utilisateur

### Conventions de Nommage

- Variables et fonctions: camelCase
- Types et composants: PascalCase
- Constantes: UPPER_SNAKE_CASE
- Fichiers de composants: PascalCase.tsx
- Autres fichiers: kebab-case.ts

## Performance et Optimisation

### Optimisations Frontend

1. **Rendering**
   - Utilisation de React.memo pour les composants coûteux
   - Hooks personnalisés pour la logique réutilisable
   - Utilisation judicieuse de useMemo et useCallback

2. **Chargement**
   - Lazy loading pour les routes
   - Code splitting par fonctionnalité
   - Optimisation des images et assets

### Optimisations Backend

1. **Base de données**
   - Indexation appropriée des tables
   - Optimisation des requêtes
   - Mise en cache des requêtes fréquentes via Redis

2. **API**
   - Rate limiting
   - Pagination de toutes les listes
   - Compression des réponses

## Sécurité

### Authentification et Autorisation

- JWT pour l'authentification API
- Rôles et permissions granulaires
- Validation côté serveur systématique

### Protection des Données

- Validation stricte des entrées utilisateur
- Protection CSRF/XSS
- Chiffrement des données sensibles

### Conformité RGPD

- Minimisation des données collectées
- Mécanisme de consentement explicite
- Fonctionnalités pour l'exercice des droits

## DevOps et Déploiement

### Environnements

- Développement: local
- Test: environnement de staging
- Production: environnement de production isolé

### CI/CD

- Tests automatisés à chaque PR
- Déploiement automatique vers staging
- Déploiement vers production après validation

### Monitoring

- Logging centralisé
- Alertes sur erreurs
- Métriques de performance

## Fonctionnalités Principales

### Gestion des Consultants
- Création et gestion de profils consultants
- Upload et analyse automatique des CV
- Gestion des compétences et disponibilités

### Gestion des Appels d'Offres
- Création et suivi des appels d'offres
- Matching automatique avec les consultants
- Génération de portfolios personnalisés

### Collaboration Inter-ESN
- Création et gestion de partenariats
- Partage sécurisé de profils
- Communication et suivi des collaborations

### Intelligence Artificielle
- Agents IA maison pour l'analyse des CV
- Architecture RAG pour l'amélioration des réponses
- Matching intelligent basé sur multiple critères

## Épics et User Stories

Le projet est organisé en épics qui regroupent des user stories fonctionnelles.
Voir la documentation détaillée pour la liste complète des épics et user stories.

## Ressources et Documentation

- API Documentation: `/api/docs`
- Architecture Diagrams: `/docs/architecture`
- User Guides: `/docs/guides`

---

© 2025 TalentMatch - Tous droits réservés
