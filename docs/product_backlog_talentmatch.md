# Product Backlog TalentMatch

## Introduction

Ce product backlog définit l'ensemble des fonctionnalités et exigences pour la plateforme TalentMatch, une solution SaaS destinée aux ESN (Entreprises de Services du Numérique) pour faciliter la gestion des talents, des appels d'offres et la collaboration inter-ESN. Ce document est structuré selon les meilleures pratiques agiles et reflète l'état actuel du projet, intégrant les évolutions récentes notamment l'architecture avec n8n et l'agent IA maison.

## Vision Produit

TalentMatch vise à transformer la façon dont les ESN gèrent leurs talents et répondent aux appels d'offres en :
- Facilitant la collaboration entre ESN pour maximiser les opportunités d'affaires
- Automatisant l'analyse et la qualification des CV grâce à l'IA
- Optimisant le processus de matching entre consultants et appels d'offres
- Fournissant une plateforme intuitive et performante pour la gestion quotidienne

## Structure du Backlog

Le backlog est organisé en :
- **Epics** : Grandes fonctionnalités ou domaines fonctionnels
- **User Stories** : Besoins spécifiques exprimés du point de vue de l'utilisateur
- **Critères d'Acceptation** : Conditions qui doivent être satisfaites pour considérer une story comme terminée
- **Priorité** : Importance relative (Must Have, Should Have, Could Have, Won't Have)
- **Estimation** : Complexité relative en points de story (1, 2, 3, 5, 8, 13, 21)

## Priorités du MVP

Pour le MVP (Minimum Viable Product), les priorités sont :
1. **Plateforme de collaboration inter-ESN** (Priorité maximale)
2. **Analyse et qualification de CV avec agents IA maison** (Priorité haute)
3. **Gestion simplifiée des appels d'offres** (Priorité moyenne)
4. **Interface utilisateur fluide et légère** (Priorité transversale)

## Epics et User Stories

### EPIC 1 : Gestion des Consultants

#### Description
Permettre aux ESN de gérer efficacement leurs consultants, leurs compétences et leur disponibilité.

#### User Stories

##### US1.1 : Création de profil consultant
- **En tant que** Recruteur
- **Je veux** créer un profil pour un nouveau consultant
- **Afin de** l'ajouter à notre base de talents
- **Priorité** : Must Have
- **Estimation** : 5
- **Critères d'acceptation** :
  - Formulaire avec champs obligatoires (nom, prénom, titre, expérience)
  - Possibilité d'ajouter une photo de profil
  - Validation des données saisies
  - Confirmation de création réussie

##### US1.2 : Téléchargement et analyse de CV
- **En tant que** Recruteur
- **Je veux** télécharger le CV d'un consultant et obtenir une analyse automatique
- **Afin de** gagner du temps sur la qualification
- **Priorité** : Must Have
- **Estimation** : 13
- **Critères d'acceptation** :
  - Support des formats PDF, DOCX, DOC
  - Extraction automatique des informations clés (expérience, formation, compétences)
  - Interface de validation/correction des données extraites
  - Intégration des données validées au profil du consultant

##### US1.3 : Gestion des compétences
- **En tant que** Recruteur
- **Je veux** ajouter, modifier ou supprimer des compétences pour un consultant
- **Afin de** maintenir son profil à jour
- **Priorité** : Must Have
- **Estimation** : 5
- **Critères d'acceptation** :
  - Interface intuitive pour la gestion des compétences
  - Possibilité de définir un niveau (débutant à expert)
  - Possibilité d'ajouter des années d'expérience par compétence
  - Suggestions automatiques basées sur le CV

##### US1.4 : Gestion des disponibilités
- **En tant que** Manager
- **Je veux** définir et mettre à jour la disponibilité des consultants
- **Afin de** faciliter leur placement sur des missions
- **Priorité** : Should Have
- **Estimation** : 8
- **Critères d'acceptation** :
  - Statuts de disponibilité (disponible, partiellement disponible, indisponible, en mission)
  - Date de disponibilité prévisionnelle
  - Visualisation calendaire des disponibilités
  - Notifications de changement de statut

##### US1.5 : Recherche avancée de consultants
- **En tant que** Commercial
- **Je veux** rechercher des consultants selon divers critères
- **Afin de** trouver rapidement les profils adaptés aux appels d'offres
- **Priorité** : Should Have
- **Estimation** : 8
- **Critères d'acceptation** :
  - Filtres par compétences, expérience, disponibilité, localisation
  - Recherche textuelle dans les CV et profils
  - Affichage des résultats par pertinence
  - Export des résultats de recherche

##### US1.6 : Génération de portfolios personnalisés
- **En tant que** Commercial
- **Je veux** générer un portfolio personnalisé pour un consultant
- **Afin de** le présenter à un client potentiel
- **Priorité** : Could Have
- **Estimation** : 13
- **Critères d'acceptation** :
  - Sélection des informations à inclure
  - Personnalisation du template et des couleurs
  - Prévisualisation avant génération
  - Export en PDF ou partage de lien

### EPIC 2 : Gestion des Appels d'Offres

#### Description
Permettre aux ESN de gérer efficacement les appels d'offres, depuis leur création jusqu'à leur attribution.

#### User Stories

##### US2.1 : Création d'appel d'offres
- **En tant que** Commercial
- **Je veux** créer un nouvel appel d'offres
- **Afin de** centraliser les informations et faciliter la recherche de consultants
- **Priorité** : Must Have
- **Estimation** : 5
- **Critères d'acceptation** :
  - Formulaire avec champs obligatoires (titre, client, description, compétences requises)
  - Possibilité de définir des dates de début/fin
  - Définition du budget et du nombre de consultants requis
  - Statut initial (ouvert)

##### US2.2 : Analyse automatique des appels d'offres
- **En tant que** Commercial
- **Je veux** que le système analyse automatiquement le contenu d'un appel d'offres
- **Afin d'** identifier les compétences requises et faciliter le matching
- **Priorité** : Should Have
- **Estimation** : 13
- **Critères d'acceptation** :
  - Extraction des compétences clés du texte
  - Suggestion de compétences à ajouter
  - Classification par importance (requise, préférée, bonus)
  - Interface de validation/correction des données extraites

##### US2.3 : Suivi des appels d'offres
- **En tant que** Manager
- **Je veux** suivre l'évolution des appels d'offres
- **Afin de** piloter efficacement l'activité commerciale
- **Priorité** : Should Have
- **Estimation** : 5
- **Critères d'acceptation** :
  - Tableau de bord avec statuts (ouvert, en cours, fermé, annulé)
  - Filtres par client, date, statut
  - Indicateurs de performance (taux de conversion, délai moyen)
  - Notifications de changement de statut

##### US2.4 : Partage d'appels d'offres
- **En tant que** Commercial
- **Je veux** partager un appel d'offres avec des ESN partenaires
- **Afin de** collaborer sur des opportunités trop grandes pour notre seule entreprise
- **Priorité** : Must Have
- **Estimation** : 8
- **Critères d'acceptation** :
  - Sélection des ESN partenaires pour le partage
  - Contrôle des informations partagées (masquage du client si nécessaire)
  - Notifications aux partenaires
  - Suivi des réponses des partenaires

##### US2.5 : Import d'appels d'offres externes
- **En tant que** Commercial
- **Je veux** importer des appels d'offres depuis des sources externes
- **Afin de** centraliser toutes les opportunités
- **Priorité** : Could Have
- **Estimation** : 13
- **Critères d'acceptation** :
  - Support de formats standards (PDF, DOCX, emails)
  - Extraction automatique des informations clés
  - Mapping avec la structure interne
  - Validation avant import définitif

### EPIC 3 : Matching et Recommandations

#### Description
Mettre en relation les consultants et les appels d'offres de manière intelligente et automatisée.

#### User Stories

##### US3.1 : Matching automatique
- **En tant que** Commercial
- **Je veux** que le système me propose automatiquement des consultants pour un appel d'offres
- **Afin de** gagner du temps dans la recherche de profils adaptés
- **Priorité** : Must Have
- **Estimation** : 13
- **Critères d'acceptation** :
  - Algorithme de matching basé sur les compétences, l'expérience et la disponibilité
  - Score de correspondance pour chaque consultant
  - Classement par pertinence
  - Explication du score de matching

##### US3.2 : Matching manuel
- **En tant que** Commercial
- **Je veux** pouvoir associer manuellement un consultant à un appel d'offres
- **Afin de** gérer des cas particuliers ou prioritaires
- **Priorité** : Must Have
- **Estimation** : 5
- **Critères d'acceptation** :
  - Interface de recherche et sélection de consultants
  - Possibilité d'ajouter des notes justificatives
  - Notification au manager du consultant
  - Mise à jour du statut du matching

##### US3.3 : Recommandations intelligentes
- **En tant que** Manager
- **Je veux** recevoir des recommandations intelligentes pour optimiser le placement des consultants
- **Afin d'** améliorer le taux d'occupation et la satisfaction
- **Priorité** : Could Have
- **Estimation** : 21
- **Critères d'acceptation** :
  - Suggestions basées sur l'historique des placements
  - Prise en compte des préférences des consultants
  - Anticipation des fins de mission
  - Alertes sur les consultants bientôt disponibles

##### US3.4 : Matching inter-ESN
- **En tant que** Commercial
- **Je veux** pouvoir rechercher des consultants chez nos ESN partenaires
- **Afin de** répondre à des appels d'offres que nous ne pouvons pas couvrir seuls
- **Priorité** : Must Have
- **Estimation** : 13
- **Critères d'acceptation** :
  - Recherche dans le pool de consultants des ESN partenaires
  - Respect des règles de confidentialité définies
  - Processus de demande et validation
  - Suivi des collaborations inter-ESN

##### US3.5 : Tableau de bord de matching
- **En tant que** Manager
- **Je veux** visualiser l'ensemble des matchings en cours
- **Afin de** piloter efficacement le placement des consultants
- **Priorité** : Should Have
- **Estimation** : 8
- **Critères d'acceptation** :
  - Vue d'ensemble des matchings par statut
  - Filtres par consultant, appel d'offres, client
  - Indicateurs de performance (taux de conversion, délai moyen)
  - Export des données

### EPIC 4 : Collaboration Inter-ESN

#### Description
Faciliter la collaboration entre ESN pour maximiser les opportunités d'affaires et optimiser le placement des consultants.

#### User Stories

##### US4.1 : Création de partenariats
- **En tant que** Directeur
- **Je veux** établir des partenariats avec d'autres ESN
- **Afin de** collaborer sur des opportunités communes
- **Priorité** : Must Have
- **Estimation** : 8
- **Critères d'acceptation** :
  - Invitation et validation des partenariats
  - Définition des règles de collaboration
  - Gestion des accords (dates de début/fin, termes)
  - Tableau de bord des partenariats actifs

##### US4.2 : Partage sécurisé de profils
- **En tant que** Manager
- **Je veux** partager des profils de consultants avec des ESN partenaires
- **Afin de** faciliter leur placement sur des missions externes
- **Priorité** : Must Have
- **Estimation** : 13
- **Critères d'acceptation** :
  - Sélection des informations à partager
  - Anonymisation optionnelle des données
  - Contrôle d'accès granulaire
  - Traçabilité des consultations

##### US4.3 : Gestion des collaborations
- **En tant que** Manager
- **Je veux** suivre les collaborations en cours avec d'autres ESN
- **Afin d'** optimiser nos partenariats
- **Priorité** : Should Have
- **Estimation** : 8
- **Critères d'acceptation** :
  - Suivi des consultants placés chez des partenaires
  - Suivi des consultants externes placés chez nous
  - Gestion des aspects financiers (commissions, facturation)
  - Indicateurs de performance des collaborations

##### US4.4 : Communication inter-ESN
- **En tant que** Commercial
- **Je veux** communiquer facilement avec mes homologues des ESN partenaires
- **Afin de** fluidifier la collaboration
- **Priorité** : Could Have
- **Estimation** : 8
- **Critères d'acceptation** :
  - Messagerie intégrée par appel d'offres/matching
  - Notifications en temps réel
  - Historique des échanges
  - Partage de documents

##### US4.5 : Tableau de bord de collaboration
- **En tant que** Directeur
- **Je veux** visualiser les performances de nos collaborations inter-ESN
- **Afin d'** évaluer et optimiser nos partenariats
- **Priorité** : Should Have
- **Estimation** : 13
- **Critères d'acceptation** :
  - KPIs de collaboration (nombre de placements, CA généré)
  - Analyse par partenaire
  - Évolution dans le temps
  - Recommandations d'optimisation

### EPIC 5 : Analyse et Traitement des CV

#### Description
Automatiser l'analyse et la qualification des CV pour gagner du temps et améliorer la précision.

#### User Stories

##### US5.1 : Extraction de données des CV
- **En tant que** Recruteur
- **Je veux** extraire automatiquement les informations clés des CV
- **Afin de** gagner du temps sur la saisie manuelle
- **Priorité** : Must Have
- **Estimation** : 13
- **Critères d'acceptation** :
  - Support de multiples formats (PDF, DOCX, DOC)
  - Extraction des informations personnelles, expériences, formations, compétences
  - Taux de précision élevé (>90%)
  - Interface de validation/correction

##### US5.2 : Analyse sémantique des CV
- **En tant que** Recruteur
- **Je veux** que le système analyse le contenu sémantique des CV
- **Afin d'** identifier les compétences implicites et l'adéquation aux postes
- **Priorité** : Should Have
- **Estimation** : 21
- **Critères d'acceptation** :
  - Identification des compétences non explicitement mentionnées
  - Analyse du niveau d'expertise basée sur le contexte
  - Détection des technologies et méthodologies utilisées
  - Suggestions d'amélioration du CV

##### US5.3 : Gestion de la base de CV
- **En tant que** Recruteur
- **Je veux** gérer efficacement notre base de CV
- **Afin de** faciliter la recherche et le suivi des candidats
- **Priorité** : Should Have
- **Estimation** : 8
- **Critères d'acceptation** :
  - Organisation par dossiers/tags
  - Versionnement des CV
  - Recherche full-text et par critères
  - Archivage automatique des CV obsolètes

##### US5.4 : Détection de doublons
- **En tant que** Recruteur
- **Je veux** que le système détecte les CV en doublon
- **Afin d'** éviter les candidatures multiples et maintenir une base propre
- **Priorité** : Could Have
- **Estimation** : 8
- **Critères d'acceptation** :
  - Algorithme de détection basé sur plusieurs critères
  - Suggestion de fusion des profils
  - Historique des versions
  - Taux de faux positifs faible

##### US5.5 : Enrichissement automatique des profils
- **En tant que** Recruteur
- **Je veux** que le système enrichisse automatiquement les profils des consultants
- **Afin d'** avoir des informations complètes et à jour
- **Priorité** : Could Have
- **Estimation** : 13
- **Critères d'acceptation** :
  - Suggestions basées sur l'analyse des CV
  - Intégration avec des sources externes (LinkedIn, GitHub)
  - Validation manuelle des enrichissements
  - Traçabilité des modifications

### EPIC 6 : Agent IA et Automatisation

#### Description
Intégrer un agent IA maison et des workflows automatisés pour optimiser les processus.

#### User Stories

##### US6.1 : Intégration de n8n pour les workflows
- **En tant qu'** Administrateur
- **Je veux** configurer des workflows automatisés avec n8n
- **Afin d'** optimiser les processus métier
- **Priorité** : Must Have
- **Estimation** : 13
- **Critères d'acceptation** :
  - Configuration de workflows pour l'extraction de CV
  - Automatisation du matching
  - Intégration avec les autres composants
  - Interface de monitoring des workflows

##### US6.2 : Agent IA maison pour l'analyse de CV
- **En tant que** Recruteur
- **Je veux** utiliser un agent IA maison spécialisé pour analyser les CV
- **Afin d'** obtenir des résultats précis et personnalisés
- **Priorité** : Should Have
- **Estimation** : 21
- **Critères d'acceptation** :
  - Utilisation exclusive d'agents IA maison pour l'analyse
  - Intégration avec n8n pour les workflows d'extraction
  - Amélioration continue basée sur le feedback
  - Confidentialité des données garantie par le traitement local

##### US6.3 : Agent IA pour le matching
- **En tant que** Commercial
- **Je veux** utiliser un agent IA pour optimiser le matching
- **Afin d'** améliorer la pertinence des recommandations
- **Priorité** : Should Have
- **Estimation** : 21
- **Critères d'acceptation** :
  - Algorithme de matching basé sur multiple critères
  - Apprentissage continu basé sur les résultats
  - Explication des recommandations
  - Paramétrage des critères de matching

##### US6.4 : Architecture RAG pour l'agent IA
- **En tant qu'** Administrateur
- **Je veux** implémenter une architecture RAG (Retrieval Augmented Generation)
- **Afin d'** améliorer la précision et la pertinence des réponses de l'agent IA
- **Priorité** : Could Have
- **Estimation** : 21
- **Critères d'acceptation** :
  - Indexation des données pertinentes
  - Mécanisme de récupération efficace
  - Génération de réponses contextuelles
  - Évaluation de la qualité des réponses

##### US6.5 : Tableau de bord IA et automatisation
- **En tant qu'** Administrateur
- **Je veux** un tableau de bord pour suivre les performances de l'IA et des automatisations
- **Afin d'** optimiser continuellement le système
- **Priorité** : Should Have
- **Estimation** : 13
- **Critères d'acceptation** :
  - Métriques de performance des agents IA
  - Suivi des workflows n8n
  - Alertes en cas d'anomalies
  - Suggestions d'optimisation

### EPIC 7 : Interface Utilisateur et Expérience

#### Description
Fournir une interface utilisateur intuitive, performante et adaptée aux différents rôles.

#### User Stories

##### US7.1 : Tableau de bord personnalisé
- **En tant qu'** Utilisateur
- **Je veux** un tableau de bord personnalisé selon mon rôle
- **Afin de** visualiser rapidement les informations pertinentes pour moi
- **Priorité** : Should Have
- **Estimation** : 13
- **Critères d'acceptation** :
  - Widgets configurables
  - Métriques adaptées au rôle
  - Personnalisation de la mise en page
  - Sauvegarde des préférences

##### US7.2 : Interface responsive
- **En tant qu'** Utilisateur
- **Je veux** accéder à l'application sur différents appareils
- **Afin de** travailler en mobilité
- **Priorité** : Should Have
- **Estimation** : 8
- **Critères d'acceptation** :
  - Adaptation à différentes tailles d'écran
  - Expérience optimisée sur mobile et tablette
  - Temps de chargement rapide
  - Fonctionnalités essentielles accessibles sur tous les appareils

##### US7.3 : Notifications et alertes
- **En tant qu'** Utilisateur
- **Je veux** recevoir des notifications pertinentes
- **Afin de** rester informé des événements importants
- **Priorité** : Should Have
- **Estimation** : 8
- **Critères d'acceptation** :
  - Notifications in-app et par email
  - Configuration des préférences de notification
  - Regroupement et priorisation des notifications
  - Marquage comme lu/non lu

##### US7.4 : Mode sombre
- **En tant qu'** Utilisateur
- **Je veux** pouvoir utiliser un mode sombre
- **Afin de** réduire la fatigue visuelle
- **Priorité** : Could Have
- **Estimation** : 5
- **Critères d'acceptation** :
  - Basculement facile entre mode clair et sombre
  - Respect des préférences système
  - Cohérence visuelle dans tous les écrans
  - Sauvegarde de la préférence

##### US7.5 : Aide contextuelle et onboarding
- **En tant que** Nouvel utilisateur
- **Je veux** être guidé dans ma découverte de l'application
- **Afin de** devenir rapidement autonome
- **Priorité** : Could Have
- **Estimation** : 8
- **Critères d'acceptation** :
  - Tutoriel interactif pour les nouveaux utilisateurs
  - Aide contextuelle sur les fonctionnalités complexes
  - Base de connaissances accessible
  - Tooltips et explications intégrées

### EPIC 8 : Administration et Sécurité

#### Description
Assurer la gestion, la sécurité et la conformité de la plateforme.

#### User Stories

##### US8.1 : Gestion des utilisateurs et rôles
- **En tant qu'** Administrateur
- **Je veux** gérer les utilisateurs et leurs droits
- **Afin de** contrôler l'accès aux fonctionnalités
- **Priorité** : Must Have
- **Estimation** : 8
- **Critères d'acceptation** :
  - Création, modification, désactivation d'utilisateurs
  - Attribution de rôles prédéfinis
  - Permissions granulaires
  - Audit des modifications

##### US8.2 : Authentification sécurisée
- **En tant qu'** Utilisateur
- **Je veux** me connecter de manière sécurisée
- **Afin de** protéger mes données et celles de l'entreprise
- **Priorité** : Must Have
- **Estimation** : 8
- **Critères d'acceptation** :
  - Authentification par email/mot de passe
  - Option d'authentification à deux facteurs
  - Gestion des sessions
  - Politique de mots de passe robuste

##### US8.3 : Audit et traçabilité
- **En tant qu'** Administrateur
- **Je veux** suivre les actions des utilisateurs
- **Afin de** garantir la sécurité et la conformité
- **Priorité** : Should Have
- **Estimation** : 13
- **Critères d'acceptation** :
  - Journalisation des actions importantes
  - Filtres et recherche dans les logs
  - Alertes sur actions sensibles
  - Rétention des logs conforme aux réglementations

##### US8.4 : Sauvegarde et restauration
- **En tant qu'** Administrateur
- **Je veux** configurer des sauvegardes automatiques
- **Afin de** prévenir la perte de données
- **Priorité** : Must Have
- **Estimation** : 8
- **Critères d'acceptation** :
  - Sauvegardes programmables
  - Vérification de l'intégrité des sauvegardes
  - Procédure de restauration testée
  - Rétention configurable

##### US8.5 : Conformité RGPD
- **En tant qu'** Administrateur
- **Je veux** assurer la conformité RGPD de la plateforme
- **Afin de** respecter la réglementation sur les données personnelles
- **Priorité** : Must Have
- **Estimation** : 13
- **Critères d'acceptation** :
  - Gestion des consentements
  - Droit à l'oubli et portabilité des données
  - Documentation des traitements
  - Mesures techniques de protection des données

## Roadmap

### Phase 1 : MVP (3-4 mois)
- Plateforme de collaboration inter-ESN
- Analyse et qualification de CV avec agents IA maison
- Gestion simplifiée des appels d'offres
- Interface utilisateur de base

### Phase 2 : Post-MVP (6-12 mois)
- Évolution vers un agent IA maison basé sur un modèle open-source fine-tuné
- Workflows n8n avancés
- Fonctionnalités avancées de matching
- Amélioration de l'expérience utilisateur

### Phase 3 : Expansion (12-18 mois)
- Intégrations externes (LinkedIn, GitHub, etc.)
- Fonctionnalités analytiques avancées
- Application mobile
- Marketplace de services

## Métriques de Succès

- **Adoption** : Nombre d'ESN actives sur la plateforme
- **Engagement** : Fréquence d'utilisation par utilisateur
- **Efficacité** : Temps gagné sur l'analyse de CV et le matching
- **Collaboration** : Nombre de placements réussis via collaborations inter-ESN
- **Satisfaction** : NPS (Net Promoter Score) des utilisateurs

## Dépendances Techniques

- Backend FastAPI
- Frontend Next.js avec TailwindCSS
- Base de données PostgreSQL
- Stockage MinIO
- Cache Redis
- Automatisation n8n
- IA : Agents IA maison et architecture RAG basée sur des modèles open-source

## Risques et Mitigations

| Risque | Impact | Probabilité | Mitigation |
|--------|--------|-------------|------------|
| Précision insuffisante de l'analyse de CV | Élevé | Moyenne | Approche hybride IA/validation humaine |
| Adoption lente par les ESN | Élevé | Moyenne | Programme d'onboarding et démonstration de valeur rapide |
| Complexité de l'agent IA maison | Moyen | Élevée | Approche progressive avec architecture RAG et modèles open-source |
| Problèmes de performance avec la montée en charge | Élevé | Faible | Architecture scalable et tests de charge réguliers |
| Résistance au changement des utilisateurs | Moyen | Moyenne | Formation, aide contextuelle et recueil de feedback |

## Processus de Révision du Backlog

Ce product backlog est un document vivant qui sera régulièrement mis à jour selon :
- Le feedback des utilisateurs
- Les évolutions technologiques
- Les priorités business
- Les apprentissages des phases précédentes

Des sessions de grooming sont prévues toutes les 2 semaines pour maintenir le backlog à jour et pertinent.
