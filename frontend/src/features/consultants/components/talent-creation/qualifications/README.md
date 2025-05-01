# Architecture des Qualifications RH

## Vue d'ensemble

Ce dossier contient les composants de qualification RH pour le formulaire multi-étapes de création de talent. L'architecture est conçue de manière modulaire, avec un composant distinct pour chaque étape du formulaire.

## Structure

- `QualificationIdentity.tsx` - Qualification pour l'étape 1 (Identité & Disponibilité)
- `QualificationSkills.tsx` - Qualification pour l'étape 2 (Compétences techniques)
- `QualificationProjects.tsx` - Qualification pour l'étape 3 (Projets & Références)
- `QualificationSoftSkills.tsx` - Qualification pour l'étape 4 (Soft Skills)
- `QualificationSummary.tsx` - Récapitulatif pour l'étape 5 (Validation)

L'orchestration de ces composants est gérée par le composant parent `QualificationSidebar.tsx` situé dans le dossier parent.

## Principes clés

1. **Séparation des préoccupations** : Chaque composant se concentre uniquement sur la qualification d'un aspect spécifique du talent.
2. **Isolation des données** : Les données sont accessibles via le contexte du formulaire (`useFormContext`) sans duplication.
3. **Cohérence de l'UI** : Tous les composants suivent le même design system.
4. **Réutilisabilité** : Les composants communs (comme `HrRating`) sont réutilisés à travers les différents modules.

## Flux d'affichage

1. Le `QualificationSidebar` reçoit le `currentStep` du formulaire principal.
2. En fonction de cette étape, il affiche le composant de qualification correspondant.
3. Chaque composant de qualification accède aux données du formulaire via `useFormContext`.
4. Les modifications effectuées dans un composant de qualification sont automatiquement reflétées dans l'état global du formulaire.

## Évolution

Pour ajouter une nouvelle fonctionnalité de qualification :

1. Identifiez le composant approprié pour cette fonctionnalité.
2. Ajoutez les champs nécessaires dans `TalentFormSchema.ts`.
3. Implémentez l'UI et la logique correspondante dans le composant de qualification.
4. Mettez à jour le `QualificationSummary.tsx` si nécessaire pour afficher la nouvelle information dans le récapitulatif.

## Précautions

- Ne modifiez pas les propriétés partagées entre les composants sans vérifier l'impact sur les autres composants.
- Maintenez la cohérence des types entre les schémas et les composants.
- Lors de l'ajout de nouveaux champs au schéma, n'oubliez pas de les initialiser dans `defaultValues` du formulaire principal.