# Architecture Frontend TalentMatch

## Vue d'ensemble

Le frontend de TalentMatch est développé avec React et TypeScript, suivant une architecture modulaire basée sur les fonctionnalités (feature-based architecture). Cette approche permet une organisation claire du code, une séparation des responsabilités et facilite la maintenance et l'évolution de l'application.

## Structure du projet

```
frontend/
├── public/              # Ressources statiques
├── src/
│   ├── components/      # Composants réutilisables
│   │   ├── common/      # Composants génériques
│   │   ├── layout/      # Composants de mise en page
│   │   └── ui/          # Composants d'interface utilisateur (shadcn/UI)
│   ├── features/        # Modules fonctionnels
│   │   ├── consultants/ # Feature des consultants
│   │   │   ├── hooks/   # Hooks spécifiques aux consultants
│   │   │   ├── services/# Services API pour les consultants
│   │   │   └── types/   # Types TypeScript spécifiques
│   │   ├── tenders/     # Feature des appels d'offres
│   │   ├── matches/     # Feature de mise en correspondance
│   │   └── cv-processing/# Feature de traitement des CV
│   ├── hooks/           # Hooks généraux réutilisables
│   ├── lib/             # Bibliothèques et utilitaires
│   │   ├── api/         # Configuration de l'API client
│   │   ├── utils/       # Fonctions utilitaires
│   │   └── themes/      # Configuration des thèmes
│   ├── pages/           # Pages/routes de l'application
│   ├── providers/       # Fournisseurs de contexte React
│   ├── styles/          # Styles globaux
│   ├── App.tsx          # Composant racine de l'application
│   └── main.tsx         # Point d'entrée de l'application
```

## Technologies principales

- **React 18+** : Bibliothèque UI pour la construction des interfaces
- **TypeScript 5+** : Typage statique pour améliorer la robustesse et la maintenabilité
- **Vite** : Outil de build moderne pour un développement rapide
- **React Router 6+** : Gestion du routage
- **TanStack Query (React Query)** : Gestion des données et du cache côté client
- **Tailwind CSS** : Framework CSS utilitaire pour le styling
- **shadcn/UI** : Composants UI basés sur Radix UI et Tailwind

## Principes architecturaux

### Architecture modulaire par fonctionnalités

L'application est organisée autour des fonctionnalités métier principales :

- Gestion des consultants
- Gestion des appels d'offres
- Matching entre consultants et appels d'offres
- Traitement et analyse des CV

Chaque module fonctionnel (feature) contient tous les éléments nécessaires à son fonctionnement :

- Types et interfaces TypeScript
- Services d'accès à l'API
- Hooks personnalisés pour la gestion d'état
- Composants spécifiques à la feature

### Gestion de l'état

La gestion de l'état est répartie en plusieurs niveaux :

1. **État global distant** : Géré par TanStack Query pour toutes les données provenant de l'API
2. **État global partagé** : Géré par React Context pour les états partagés entre composants non liés hiérarchiquement
3. **État local** : Géré par les hooks useState et useReducer au niveau des composants

### Communication avec le backend

La communication avec le backend est centralisée dans le client API (basé sur Axios) et encapsulée dans des services spécifiques à chaque domaine fonctionnel.

Exemple de structure pour un service :

```typescript
export const consultantService = {
  async getConsultants(filters?: ConsultantFilters): Promise<ConsultantDisplay[]>,
  async getConsultantById(id: number): Promise<ConsultantDisplay | null>,
  async createConsultant(consultant: ConsultantCreate): Promise<ConsultantDisplay>,
  async updateConsultant(id: number, consultant: ConsultantUpdate): Promise<ConsultantDisplay>,
  async deleteConsultant(id: number): Promise<void>
};
```

### Composants UI

L'application utilise une approche de composition pour les composants UI :

- Composants de base réutilisables (UI)
- Composants de mise en page (Layout)
- Composants spécifiques aux features
- Pages complètes

Les composants UI sont basés sur shadcn/UI, une collection de composants réutilisables construits avec Radix UI et Tailwind CSS.

## Flux de données

1. L'utilisateur interagit avec l'interface
2. Les composants appellent les hooks personnalisés (ex: `useConsultants`)
3. Les hooks utilisent TanStack Query pour gérer les requêtes et le cache
4. Les services API effectuent les requêtes HTTP vers le backend
5. Les données sont retournées, transformées si nécessaire, et rendues dans l'interface

## Intégration avec le backend

L'intégration avec le backend se fait via l'API REST exposée par le backend FastAPI. Les points d'intégration principaux sont :

- `/api/v1/consultants` : Gestion des consultants
- `/api/v1/tenders` : Gestion des appels d'offres
- `/api/v1/matches` : Gestion du matching
- `/api/v1/cv-analysis` : Analyse et traitement des CV

## Sécurité

L'authentification est gérée via JWT (JSON Web Tokens) stockés dans le localStorage. Toutes les requêtes authentifiées incluent le token dans l'en-tête Authorization.

Les routes protégées utilisent un composant `ProtectedRoute` qui vérifie l'authentification avant de permettre l'accès.

## Performance

Plusieurs stratégies sont mises en place pour optimiser les performances :

- Code splitting avec React.lazy et Suspense
- Mémoïsation avec React.memo, useMemo et useCallback
- Virtualisation pour les listes longues
- Optimisation des images avec lazy loading et formats modernes
