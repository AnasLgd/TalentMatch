# Spécification Technique du Frontend TalentMatch

## 1. Vue d'ensemble

### 1.1 Introduction
TalentMatch est une plateforme SaaS destinée aux ESN (Entreprises de Services du Numérique) pour faciliter la gestion des talents, des appels d'offres et la collaboration inter-ESN. Le frontend constitue l'interface utilisateur de cette plateforme et doit offrir une expérience intuitive, performante et responsive.

### 1.2 Objectifs
- Fournir une interface utilisateur moderne et intuitive pour toutes les fonctionnalités de TalentMatch
- Assurer une expérience utilisateur fluide et responsive sur tous les appareils
- Faciliter la gestion des consultants, des appels d'offres et des correspondances (matching)
- Permettre la collaboration entre différentes ESN

### 1.3 Technologies
- **Framework** : Next.js 14+ avec App Router
- **Langage** : TypeScript 5+
- **Styling** : TailwindCSS avec shadcn/ui comme bibliothèque de composants
- **Gestion d'état** : React Context pour l'état global, React Query pour les données serveur
- **Authentification** : NextAuth.js intégré avec le backend FastAPI
- **Tests** : Jest pour les tests unitaires, Cypress pour les tests E2E

## 2. Architecture Frontend

### 2.1 Structure des répertoires
```
frontend/
├── public/                  # Ressources statiques
│   ├── assets/              # Images, logos, etc.
│   └── icons/               # Icônes SVG
├── src/
│   ├── app/                 # Structure App Router de Next.js
│   │   ├── (auth)/          # Routes protégées par authentification
│   │   │   ├── dashboard/   # Tableau de bord principal
│   │   │   ├── consultants/ # Gestion des consultants
│   │   │   ├── tenders/     # Gestion des appels d'offres
│   │   │   ├── matches/     # Visualisation et gestion des correspondances
│   │   │   └── settings/    # Paramètres utilisateur et entreprise
│   │   ├── api/             # Routes API côté serveur Next.js
│   │   ├── login/           # Page de connexion
│   │   └── register/        # Page d'inscription
│   ├── components/          # Composants partagés
│   │   ├── ui/              # Composants UI de base (shadcn/ui)
│   │   ├── layout/          # Composants de mise en page
│   │   ├── forms/           # Composants de formulaires
│   │   └── data-display/    # Tableaux, graphiques, etc.
│   ├── features/            # Composants spécifiques aux fonctionnalités
│   │   ├── availability/    # Gestion des disponibilités
│   │   ├── collaboration/   # Collaboration inter-ESN
│   │   ├── consultants/     # Gestion des consultants
│   │   ├── cv-processing/   # Traitement et analyse des CV
│   │   ├── dashboard/       # Tableaux de bord et widgets
│   │   ├── matching/        # Algorithmes et visualisation de matching
│   │   └── qualification/   # Évaluation et qualification des consultants
│   ├── hooks/               # Hooks React personnalisés
│   ├── lib/                 # Utilitaires et fonctions d'aide
│   │   ├── api/             # Client API pour communiquer avec le backend
│   │   ├── auth/            # Logique d'authentification
│   │   └── utils/           # Fonctions utilitaires
│   ├── providers/           # Providers React Context
│   │   ├── auth-provider.tsx
│   │   └── theme-provider.tsx
│   ├── styles/              # Styles globaux et variables TailwindCSS
│   └── types/               # Définitions de types TypeScript
└── next.config.js           # Configuration Next.js
```

### 2.2 Organisation par fonctionnalités
Le frontend est organisé selon une architecture orientée fonctionnalités (Feature-Driven Architecture), où chaque domaine fonctionnel est encapsulé dans son propre module avec ses composants, hooks et services spécifiques.

Chaque module fonctionnel suit cette structure :
```
features/[feature-name]/
├── components/       # Composants spécifiques à la fonctionnalité
├── hooks/            # Hooks spécifiques à la fonctionnalité
├── services/         # Services et logique métier
└── types/            # Types spécifiques à la fonctionnalité
```

### 2.3 Gestion d'état
- **État local** : Hooks useState et useReducer de React
- **État global** : React Context pour les données partagées (thème, préférences utilisateur)
- **État serveur** : React Query pour la gestion des requêtes API, mise en cache et synchronisation

### 2.4 Routage
Utilisation du système App Router de Next.js avec :
- Routes groupées par domaine fonctionnel
- Layouts partagés pour maintenir la cohérence de l'interface
- Middleware pour la protection des routes authentifiées
- Chargement progressif et streaming pour améliorer les performances

## 3. Composants et Interfaces Utilisateur

### 3.1 Système de design
- Utilisation de TailwindCSS pour le styling
- Intégration de shadcn/ui pour les composants de base
- Système de thèmes avec mode clair/sombre
- Variables CSS pour les couleurs, espacements et typographie

### 3.2 Pages principales

#### 3.2.1 Tableau de bord
- Vue d'ensemble des KPIs (consultants disponibles, appels d'offres actifs, taux de matching)
- Widgets personnalisables
- Graphiques et visualisations des données
- Notifications et alertes

#### 3.2.2 Gestion des consultants
- Liste des consultants avec filtres et recherche
- Fiche détaillée du consultant
- Formulaire d'ajout/édition de consultant
- Gestion des compétences et expériences
- Visualisation des disponibilités
- Upload et analyse de CV

#### 3.2.3 Gestion des appels d'offres
- Liste des appels d'offres avec filtres et recherche
- Fiche détaillée de l'appel d'offres
- Formulaire d'ajout/édition d'appel d'offres
- Gestion des compétences requises
- Suivi du statut et des échéances

#### 3.2.4 Matching
- Interface de matching manuel et automatique
- Visualisation des scores de correspondance
- Filtres et critères de matching personnalisables
- Tableau comparatif des consultants pour un appel d'offres
- Génération de portfolios personnalisés

#### 3.2.5 Collaboration inter-ESN
- Interface de recherche de partenaires
- Gestion des demandes de collaboration
- Suivi des collaborations en cours
- Partage sécurisé des profils de consultants

### 3.3 Composants réutilisables
- Tableaux de données avec tri, filtrage et pagination
- Formulaires avec validation et gestion d'erreurs
- Sélecteurs de compétences avec niveaux d'expertise
- Visualisations de données (graphiques, jauges, etc.)
- Système de notifications
- Modales et popovers
- Menus de navigation et breadcrumbs

## 4. Intégration avec le Backend

### 4.1 Communication API
- Client API centralisé basé sur Axios ou fetch
- Endpoints organisés par domaine fonctionnel
- Gestion des tokens JWT pour l'authentification
- Intercepteurs pour la gestion des erreurs et des tokens expirés

### 4.2 Structure des requêtes
- Utilisation de React Query pour la gestion des requêtes
- Hooks personnalisés pour chaque type de requête
- Mise en cache et invalidation intelligente
- Gestion des états de chargement et d'erreur

### 4.3 Authentification
- Intégration avec NextAuth.js
- Flux d'authentification complet (login, register, reset password)
- Gestion des rôles et permissions
- Protection des routes authentifiées via middleware

## 5. Fonctionnalités Spécifiques

### 5.1 Analyse et traitement des CV
- Interface de téléchargement de CV (drag & drop)
- Prévisualisation des CV
- Affichage des données extraites
- Édition et validation des informations extraites
- Suggestion automatique de compétences

### 5.2 Système de matching
- Interface de définition des critères de matching
- Visualisation des scores de correspondance
- Filtres avancés pour affiner les résultats
- Comparaison côte à côte des candidats
- Génération de rapports de matching

### 5.3 Gestion des disponibilités
- Calendrier des disponibilités des consultants
- Vue par consultant, équipe ou projet
- Filtres par période, statut, compétences
- Alertes pour les conflits de planning

### 5.4 Génération de portfolios
- Interface de sélection des informations à inclure
- Prévisualisation du portfolio
- Options de personnalisation (template, couleurs, logo)
- Export en PDF ou partage de lien

## 6. Performance et Optimisation

### 6.1 Stratégies de chargement
- Chargement progressif des composants (lazy loading)
- Streaming des données avec Suspense
- Pagination et chargement à la demande pour les listes volumineuses
- Préchargement des données critiques

### 6.2 Optimisation des images
- Utilisation du composant Image de Next.js
- Formats d'image optimisés (WebP, AVIF)
- Chargement adaptatif selon la taille d'écran
- Placeholder et effet de blur pendant le chargement

### 6.3 Mise en cache
- Stratégies de mise en cache côté client
- Utilisation de SWR ou React Query pour la revalidation
- Stockage local pour les données fréquemment utilisées
- Préchargement des données pour les routes probables

## 7. Tests et Qualité

### 7.1 Tests unitaires
- Tests des composants avec Jest et React Testing Library
- Tests des hooks personnalisés
- Tests des utilitaires et fonctions pures

### 7.2 Tests d'intégration
- Tests des flux utilisateur complets
- Mocking des appels API
- Vérification des interactions entre composants

### 7.3 Tests E2E
- Tests Cypress pour les parcours utilisateur critiques
- Vérification des fonctionnalités dans un environnement réel
- Tests de régression visuelle

### 7.4 Accessibilité
- Conformité WCAG 2.1 niveau AA
- Tests automatisés avec axe-core
- Support du clavier et des lecteurs d'écran
- Contraste et taille de texte adaptés

## 8. Déploiement et CI/CD

### 8.1 Environnements
- Développement local
- Staging pour les tests
- Production

### 8.2 Pipeline CI/CD
- Linting et vérification des types
- Exécution des tests automatisés
- Build et optimisation
- Déploiement automatique

### 8.3 Monitoring
- Suivi des performances avec Lighthouse
- Analyse des erreurs côté client
- Tracking des métriques d'utilisation

## 9. Prochaines étapes et évolution

### 9.1 Priorités de développement
1. Mise en place de la structure de base et du système d'authentification
2. Développement des interfaces de gestion des consultants et des appels d'offres
3. Implémentation du système de matching
4. Développement des fonctionnalités de collaboration
5. Optimisation et améliorations UX

### 9.2 Évolutions futures
- Application mobile (PWA ou native)
- Intégration avec des services externes (LinkedIn, GitHub, etc.)
- Fonctionnalités avancées d'IA maison pour l'analyse des CV et le matching
- Tableaux de bord analytiques avancés
- Système de recommandation intelligent

## 10. Ressources et références

### 10.1 Documentation technique
- [Documentation Next.js](https://nextjs.org/docs)
- [Documentation TailwindCSS](https://tailwindcss.com/docs)
- [Documentation shadcn/ui](https://ui.shadcn.com)
- [Documentation React Query](https://tanstack.com/query/latest/docs/react/overview)

### 10.2 Design et maquettes
- Maquettes Figma à développer
- Guide de style et système de design à établir

### 10.3 API Backend
- Documentation Swagger/OpenAPI du backend FastAPI
- Endpoints et modèles de données
