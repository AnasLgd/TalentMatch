# Architecture Frontend TalentMatch

## Vue d'ensemble

Le frontend de TalentMatch est développé avec React et TypeScript, suivant une architecture modulaire basée sur les fonctionnalités (feature-based architecture). Cette approche permet une organisation claire du code, une séparation des responsabilités et facilite la maintenance et l'évolution de l'application. L'architecture suit des principes de clean code et adopte une approche "schema-first" garantissant une cohérence avec les modèles backend.

## Structure du projet

```
frontend/
├── public/              # Ressources statiques
│   ├── favicon.ico
│   ├── placeholder.svg
│   └── robots.txt
├── src/
│   ├── components/      # Composants réutilisables
│   │   ├── common/      # Composants génériques
│   │   │   └── LogoSection.tsx
│   │   ├── layout/      # Composants de mise en page
│   │   │   ├── DashboardLayout.tsx
│   │   │   ├── Header.tsx
│   │   │   └── Sidebar.tsx
│   │   ├── ui/          # Composants d'interface utilisateur (shadcn/UI)
│   │   │   ├── accordion.tsx
│   │   │   ├── button.tsx
│   │   │   ├── form.tsx
│   │   │   ├── input.tsx
│   │   │   └── ... (autres composants UI)
│   │   ├── AboutSection.tsx
│   │   ├── HeroSection.tsx
│   │   ├── Navbar.tsx
│   │   └── ... (autres composants spécifiques)
│   ├── features/        # Modules fonctionnels
│   │   ├── consultants/ # Feature des consultants
│   │   │   ├── components/ # Composants spécifiques aux consultants
│   │   │   │   ├── ConsultantForm.tsx
│   │   │   │   └── __tests__/ # Tests des composants
│   │   │   ├── hooks/     # Hooks spécifiques aux consultants
│   │   │   │   └── useConsultants.ts
│   │   │   ├── services/  # Services API pour les consultants
│   │   │   │   ├── consultant-service.ts
│   │   │   │   └── upload-service.ts
│   │   │   └── types/     # Types TypeScript spécifiques
│   │   │       └── index.ts
│   │   ├── tenders/     # Feature des appels d'offres
│   │   │   ├── services/
│   │   │   │   └── tender-service.ts
│   │   │   └── types/
│   │   │       └── index.ts
│   │   ├── matches/     # Feature de mise en correspondance
│   │   │   ├── services/
│   │   │   │   └── match-service.ts
│   │   │   └── types/
│   │   │       └── index.ts
│   │   └── cv-processing/# Feature de traitement des CV
│   │       ├── services/
│   │       │   └── cv-processing-service.ts
│   │       └── types/
│   │           └── index.ts
│   ├── hooks/           # Hooks généraux réutilisables
│   │   ├── use-mobile.tsx
│   │   ├── use-toast.ts
│   │   └── useInView.tsx
│   ├── lib/             # Bibliothèques et utilitaires
│   │   ├── api/         # Configuration de l'API client
│   │   │   └── api-client.ts
│   │   ├── utils.ts
│   │   └── themes.ts    # Configuration des thèmes
│   ├── pages/           # Pages/routes de l'application
│   │   ├── Consultants.tsx
│   │   ├── CvAnalysis.tsx
│   │   ├── Dashboard.tsx
│   │   ├── Index.tsx
│   │   ├── Login.tsx
│   │   ├── Matches.tsx
│   │   ├── NotFound.tsx
│   │   ├── Partners.tsx
│   │   ├── Register.tsx
│   │   ├── StyleGuide.tsx
│   │   └── Tenders.tsx
│   ├── providers/       # Fournisseurs de contexte React
│   │   └── AuthProvider.tsx
│   ├── styles/          # Styles globaux
│   ├── App.tsx          # Composant racine de l'application
│   ├── App.css          # Styles pour le composant App
│   ├── index.css        # Styles globaux
│   └── main.tsx         # Point d'entrée de l'application
├── Dockerfile           # Configuration Docker pour le frontend
├── components.json      # Configuration shadcn/ui
├── eslint.config.js     # Configuration ESLint
├── jest.config.js       # Configuration Jest
├── package.json         # Dépendances et scripts
├── postcss.config.js    # Configuration PostCSS
├── tailwind.config.ts   # Configuration Tailwind CSS
├── tsconfig.json        # Configuration TypeScript
└── vite.config.ts       # Configuration Vite
```

## Technologies principales

- **React 18+** : Bibliothèque UI pour la construction des interfaces
- **TypeScript 5+** : Typage statique pour améliorer la robustesse et la maintenabilité
- **Vite** : Outil de build moderne pour un développement rapide
- **React Router 6+** : Gestion du routage
- **TanStack Query (React Query)** : Gestion des données et du cache côté client
- **Axios** : Client HTTP pour les requêtes API
- **Tailwind CSS** : Framework CSS utilitaire pour le styling
- **shadcn/UI** : Composants UI basés sur Radix UI et Tailwind
- **Jest + React Testing Library** : Tests unitaires et d'intégration
- **ESLint** : Linting et vérification de la qualité du code
- **Zod** : Validation des schémas côté client

## Principes architecturaux

### Architecture modulaire par fonctionnalités

L'application est organisée autour des fonctionnalités métier principales, suivant une approche "feature-based":

- Gestion des consultants (`features/consultants`)
- Gestion des appels d'offres (`features/tenders`)
- Matching entre consultants et appels d'offres (`features/matches`)
- Traitement et analyse des CV (`features/cv-processing`)

Chaque module fonctionnel (feature) contient tous les éléments nécessaires à son fonctionnement :

- **Types et interfaces TypeScript** : Définition des modèles de données et des DTOs
- **Services d'accès à l'API** : Encapsulation des appels HTTP et mappage des réponses
- **Hooks personnalisés** : Gestion de l'état et de la logique métier
- **Composants spécifiques** : Éléments d'interface dédiés à la fonctionnalité

Cette organisation facilite :
- La compréhension du code et de ses responsabilités
- Le développement parallèle par plusieurs équipes
- L'extension ou la refactorisation d'une fonctionnalité sans affecter le reste de l'application

### Approche Schema-First

Le frontend suit une approche "schema-first" où :

1. Les interfaces TypeScript sont définies pour correspondre exactement aux modèles Pydantic du backend
2. Les types sont organisés par domaine fonctionnel dans chaque feature
3. Des types distincts sont utilisés pour différents cas d'utilisation :
   - Types de base (ex: `Consultant`) reflétant le modèle backend
   - Types d'affichage (ex: `ConsultantDisplay`) pour les besoins spécifiques de l'UI
   - Types de création (ex: `ConsultantCreate`) pour les données à envoyer lors de la création
   - Types de mise à jour (ex: `ConsultantUpdate`) pour les données modifiables

Exemple d'interfaces pour les consultants :

```typescript
// Type de base reflétant le modèle backend
export interface Consultant {
  id: number;
  user_id: number;
  company_id: number;
  title: string;
  experience_years?: number;
  availability_status: AvailabilityStatus;
  availability_date?: string;
  hourly_rate?: number;
  daily_rate?: number;
  bio?: string;
  location?: string;
  user: User;
  skills: Skill[];
  created_at: string;
  updated_at?: string;
  first_name?: string;
  last_name?: string;
}

// Type spécifique pour l'affichage dans l'UI
export interface ConsultantDisplay {
  id: number;
  name: string;
  role: string;
  experience: string;
  skills: Skill[];
  status: string;
  email?: string;
  availabilityDate?: string;
}

// Type pour la création d'un nouveau consultant
export interface ConsultantCreate {
  user_id?: number;
  company_id: number;
  title: string;
  experience_years?: number;
  availability_status?: AvailabilityStatus;
  availability_date?: string;
  skills?: Skill[];
  first_name?: string;
  last_name?: string;
}
```

### Gestion de l'état

La gestion de l'état est répartie en plusieurs niveaux, suivant le principe de "responsabilité appropriée" :

#### 1. État global distant (Server State)

Géré par TanStack Query, qui offre :
- Mise en cache automatique des données
- Invalidation intelligente du cache
- Gestion des états de chargement et d'erreur
- Revalidation automatique des données
- Pagination et gestion de l'infinité
- Déduplications des requêtes

Exemple d'implémentation dans `useConsultants.ts` :

```typescript
const {
  data: consultants,
  isLoading,
  isError,
  error,
  refetch,
} = useQuery({
  queryKey: ["consultants"],
  queryFn: () => consultantService.getConsultants(),
  staleTime: 5 * 60 * 1000, // 5 minutes
});
```

#### 2. État global partagé (Client State)

Géré par React Context pour les états partagés entre composants non liés hiérarchiquement :
- État d'authentification (`AuthProvider.tsx`)
- Thème et préférences utilisateur
- Paramètres globaux de l'application

#### 3. État local des composants

Géré par les hooks React au niveau des composants :
- `useState` pour les états simples
- `useReducer` pour les états complexes
- `useMemo` et `useCallback` pour l'optimisation

### Communication avec le backend

La communication avec le backend est centralisée et organisée en plusieurs couches :

#### 1. Client API central (apiClient)

Le client API (`lib/api/api-client.ts`) fournit une abstraction sur Axios avec :
- Configuration de base (URL, headers, timeout)
- Intercepteurs pour l'authentification
- Gestion centralisée des erreurs
- Transformation des réponses
- Typage générique des méthodes

```typescript
const apiClient = {
  get: <T>(url: string, config?: AxiosRequestConfig): Promise<T> => {
    return axiosInstance.get(url, config);
  },
  post: <T>(url: string, data?: unknown, config?: AxiosRequestConfig): Promise<T> => {
    return axiosInstance.post(url, data, config);
  },
  // ...autres méthodes HTTP
};
```

#### 2. Services spécifiques par domaine

Chaque domaine fonctionnel possède son propre service qui :
- Utilise le client API pour les requêtes HTTP
- Encapsule les endpoints spécifiques
- Mappe les données entre formats backend et frontend
- Gère les erreurs spécifiques au domaine

Exemple avec `consultant-service.ts` :

```typescript
export const consultantService = {
  async getConsultants(filters?: ConsultantFilters): Promise<ConsultantDisplay[]> {
    const queryParams = buildQueryParams(filters);
    const endpoint = `/consultants?${queryParams.toString()}`;
    
    const response = await apiClient.get<Consultant[]>(endpoint);
    return response.map(mapToConsultantDisplay);
  },
  
  async createConsultant(consultantData: ConsultantCreate): Promise<ConsultantDisplay> {
    const newConsultant = await apiClient.post<Consultant>("/consultants", consultantData);
    return mapToConsultantDisplay(newConsultant);
  },
  
  // ...autres méthodes
};
```

#### 3. Hooks personnalisés

Les hooks encapsulent l'utilisation des services et exposent des méthodes et états réactifs :
- Utilisation de TanStack Query pour le cache et les requêtes
- Gestion des états de chargement et d'erreur
- Méthodes CRUD et opérations spécifiques

Exemple avec `useConsultants.ts` :

```typescript
export const useConsultants = () => {
  const queryClient = useQueryClient();
  
  const { data: consultants, isLoading, isError } = useQuery({
    queryKey: ["consultants"],
    queryFn: () => consultantService.getConsultants(),
  });
  
  const { mutate: createConsultant } = useMutation({
    mutationFn: (newConsultant: ConsultantCreate) => 
      consultantService.createConsultant(newConsultant),
    onSuccess: (newConsultant) => {
      queryClient.invalidateQueries({ queryKey: ["consultants"] });
    },
  });
  
  // ...autres mutations et fonctionnalités
  
  return {
    consultants,
    isLoading,
    isError,
    createConsultant,
    // ...autres propriétés
  };
};
```

### Composants UI

L'application utilise une approche de composition pour les composants UI, suivant une hiérarchie claire :

#### 1. Composants de base (UI)

Basés sur shadcn/UI, ces composants sont :
- Hautement réutilisables
- Accessibles (conformes WCAG)
- Stylisés avec Tailwind CSS
- Fortement typés avec TypeScript

Exemples : Button, Input, Form, Select, Modal, etc.

#### 2. Composants de mise en page (Layout)

Définissent la structure générale des pages :
- Header
- Sidebar
- DashboardLayout
- Containers

#### 3. Composants spécifiques aux features

Encapsulent la logique métier pour une fonctionnalité spécifique :
- ConsultantForm
- TenderList
- MatchingResults
- CVUploader

#### 4. Pages complètes

Assemblent les composants pour former une vue complète :
- Consultants.tsx
- Tenders.tsx
- Matches.tsx
- CvAnalysis.tsx

### Tests

L'application utilise une stratégie de tests complète avec Jest et React Testing Library :

#### 1. Tests unitaires

Testent les fonctions et hooks isolément :
- Validation des fonctions utilitaires
- Comportement des hooks personnalisés

#### 2. Tests de composants

Testent le rendu et le comportement des composants UI :
- Vérification du rendu correct
- Tests d'interaction utilisateur
- Validation des formulaires

Exemple de test de composant (ConsultantForm.test.tsx) :

```typescript
it('crée un consultant avec succès quand le formulaire est valide', async () => {
  render(<ConsultantForm onSuccess={mockOnSuccess} onCancel={mockOnCancel} userId={1} companyId={1} />);
  
  // Remplir le formulaire
  await userEvent.type(screen.getByLabelText(/Prénom\*/i), 'Martin');
  await userEvent.type(screen.getByLabelText(/Nom\*/i), 'Dupont');
  await userEvent.type(screen.getByLabelText(/Titre\*/i), 'Développeur Java');
  
  // Soumettre le formulaire
  const submitButton = screen.getByText(/Créer le consultant/i);
  fireEvent.click(submitButton);
  
  // Vérifier que la création a été appelée avec les bonnes données
  await waitFor(() => {
    expect(mockCreateConsultant).toHaveBeenCalledWith(expect.objectContaining({
      user_id: 1,
      company_id: 1,
      title: 'Développeur Java',
    }));
  });
});
```

#### 3. Tests d'intégration

Testent l'interaction entre plusieurs composants et services :
- Communication entre composants
- Flux complets d'une fonctionnalité

## Flux de données

Le flux de données suit un cycle unidirectionnel :

1. **Interaction utilisateur** : L'utilisateur interagit avec un composant UI
   
2. **Action déclenchée** : Le composant appelle une fonction du hook associé
   ```tsx
   const handleSubmit = (data: FormData) => {
     createConsultant(data);
   };
   ```

3. **Mutation des données** : Le hook utilise une mutation TanStack Query pour modifier les données
   ```tsx
   const { mutate: createConsultant } = useMutation({
     mutationFn: (data) => consultantService.createConsultant(data),
     // ...
   });
   ```

4. **Appel API** : Le service effectue la requête HTTP via le client API
   ```tsx
   async createConsultant(data) {
     return apiClient.post('/consultants', data);
   }
   ```

5. **Mise à jour du cache** : À la réception de la réponse, le cache TanStack Query est mis à jour
   ```tsx
   onSuccess: () => {
     queryClient.invalidateQueries({ queryKey: ['consultants'] });
   }
   ```

6. **Rendu UI** : Les composants se mettent à jour automatiquement avec les nouvelles données

## Intégration avec le backend

L'intégration avec le backend se fait via l'API REST exposée par le backend FastAPI, avec les points d'intégration principaux structurés par domaine fonctionnel :

### API Consultants
- `GET /api/consultants` : Liste des consultants avec filtres optionnels
- `GET /api/consultants/{id}` : Détails d'un consultant
- `POST /api/consultants` : Création d'un consultant
- `PUT /api/consultants/{id}` : Mise à jour d'un consultant
- `DELETE /api/consultants/{id}` : Suppression d'un consultant

### API Appels d'offres
- `GET /api/tenders` : Liste des appels d'offres avec filtres
- `GET /api/tenders/{id}` : Détails d'un appel d'offres
- `POST /api/tenders` : Création d'un appel d'offres
- `PUT /api/tenders/{id}` : Mise à jour d'un appel d'offres
- `DELETE /api/tenders/{id}` : Suppression d'un appel d'offres

### API Matching
- `GET /api/matches` : Liste des matchs
- `GET /api/matches/{id}` : Détails d'un match
- `POST /api/matches` : Création manuelle d'un match
- `PUT /api/matches/{id}` : Mise à jour d'un match
- `POST /api/matches/generate` : Génération automatique de matchs

### API Traitement des CV
- `POST /api/cv-analysis/upload` : Upload d'un CV
- `POST /api/cv-analysis/analyze` : Analyse d'un CV
- `GET /api/cv-analysis/results/{id}` : Résultats d'analyse

## Sécurité

### Authentification

L'authentification est gérée via JWT (JSON Web Tokens) :

1. **Stockage des tokens** :
   - Les tokens sont stockés dans le localStorage
   - Structure de token : `{ access_token, refresh_token, token_type }`

2. **Injection automatique** :
   - L'intercepteur Axios ajoute automatiquement le token aux requêtes
   ```typescript
   axiosInstance.interceptors.request.use((config) => {
     const token = localStorage.getItem('auth_token');
     if (token && config.headers) {
       config.headers.Authorization = `Bearer ${token}`;
     }
     return config;
   });
   ```

3. **Gestion des erreurs d'authentification** :
   - Redirection vers la page de login en cas d'erreur 401
   - Suppression du token expiré
   ```typescript
   if (status === 401) {
     localStorage.removeItem('auth_token');
     if (window.location.pathname !== '/login') {
       window.location.href = '/login';
     }
   }
   ```

### Contrôle d'accès

- **Protection des routes** :
  - Utilisation d'un composant `ProtectedRoute` qui vérifie l'authentification
  - Redirection des utilisateurs non authentifiés

- **Autorisation basée sur les rôles** :
  - Vérification du rôle utilisateur pour l'accès aux fonctionnalités
  - Masquage conditionnel des éléments UI selon les droits

### Validation des données

- **Validation côté client** :
  - Utilisation de Zod pour la validation des formulaires
  - Feedback immédiat à l'utilisateur sur les erreurs de saisie

- **Validation centralisée des réponses API** :
  - Vérification des formats de données reçues
  - Transformation cohérente des données avant utilisation

## Performance

Plusieurs stratégies sont mises en place pour optimiser les performances :

### Optimisations du chargement

- **Code splitting** : 
  - Utilisation de React.lazy et Suspense pour charger les composants à la demande
  - Séparation du bundle par route/feature

- **Lazy loading des images** :
  - Chargement progressif des images avec attributs loading="lazy"
  - Utilisation de placeholders et blur-up pour améliorer l'expérience utilisateur

### Optimisations du rendu

- **Mémoïsation** :
  - Utilisation de React.memo pour éviter les rendus inutiles des composants
  - Usage stratégique de useMemo et useCallback pour les calculs coûteux

- **Virtualisation** :
  - Rendu efficace des listes longues avec des techniques de virtualisation
  - Chargement à la demande des données lors du défilement

### Optimisations des requêtes

- **Stratégies de cache** :
  - Configuration fine du staleTime et cacheTime dans TanStack Query
  - Préchargement des données probables (prefetching)

- **Déduplications des requêtes** :
  - Regroupement automatique des requêtes identiques par TanStack Query
  - Évitement des appels réseau redondants

- **Pagination et chargement incrémental** :
  - Chargement des données par lots avec curseur ou pagination
  - Interfaces infinies pour les grandes listes

## Accessibilité

L'application respecte les directives WCAG (Web Content Accessibility Guidelines) :

- **Composants accessibles** :
  - Utilisation de composants shadcn/UI basés sur Radix UI, conçus pour l'accessibilité
  - Support complet du clavier et des lecteurs d'écran

- **Sémantique HTML appropriée** :
  - Structure de document logique avec éléments landmarks
  - Utilisation correcte des balises sémantiques (h1-h6, nav, main, etc.)

- **Contraste et lisibilité** :
  - Respect des ratios de contraste minimaux
  - Tailles de texte adaptables et lisibles

- **Feedback non-visuel** :
  - Messages d'état pour les lecteurs d'écran
  - Alternatives textuelles pour les éléments visuels

## Internationalisation

Le système est conçu pour supporter la localisation future :

- Textes extraits dans des fichiers de traduction
- Support des formats de date, heure et nombres localisés
- Structure permettant l'ajout de nouvelles langues
