# Refonte de la charte graphique TalentMatch

Cette documentation présente la nouvelle charte graphique implémentée pour TalentMatch, reproduisant fidèlement l'esthétique de la capture d'écran de référence et offrant un système de thèmes cohérent.

## Caractéristiques principales

- **Système de thèmes bicolore** : Un thème sombre reproduisant l'interface de la capture d'écran et un thème clair complémentaire.
- **Palette de couleurs harmonieuse** : Couleurs soigneusement sélectionnées pour assurer accessibilité et cohérence visuelle.
- **Composants réutilisables** : Bibliothèque de composants améliorés et styles prédéfinis.
- **Espacements et typographie standardisés** : Système cohérent d'espacement et hiérarchie typographique.

## Structure des fichiers

- `/src/lib/themes.ts` - Définition des thèmes (couleurs, espacements, etc.)
- `/src/components/ui/theme-switcher.tsx` - Composant de bascule entre thèmes
- `/src/index.css` - Styles globaux et variables CSS
- `/src/pages/StyleGuide.tsx` - Page de démonstration des composants et styles

## Palette de couleurs

### Thème sombre (valeurs HSL)
- **Background**: 222 33% 11%
- **Card**: 223 35% 13%
- **Primary** (accent émeraude): 160 84% 39%
- **Secondary**: 215 25% 24%
- **Muted**: 215 28% 17%

### Thème clair (valeurs HSL)
- **Background**: 210 40% 98%
- **Card**: 0 0% 100%
- **Primary** (accent émeraude foncé): 160 84% 30%
- **Secondary**: 215 25% 85%
- **Muted**: 210 25% 90%
- **Foreground/Texte** (assombri pour meilleur contraste): 222 47% 11%

## Classes utilitaires

### Cartes et conteneurs
- `.dashboard-card` - Style standard pour les cartes du dashboard
- `.stats-card` - Style pour les cartes de statistiques
- `.card-hover-effect` - Effet au survol sur les cartes
- `.glass-effect` - Effet verre dépoli pour les overlays

### Statuts et badges
- `.status-badge` - Badge standard pour les statuts
- `.status-badge-new` - Badge "Nouveau" (bleu)
- `.status-badge-active` - Badge "Actif" (vert)
- `.status-badge-pending` - Badge "En attente" (orange)
- `.status-badge-closed` - Badge "Fermé" (rouge)

### Éléments graphiques
- `.progress-bar` et `.progress-bar-fill` - Barres de progression améliorées
- `.icon-container` - Conteneur pour icônes avec fond
- `.accent-glow` - Effet de lueur pour mettre en évidence des éléments

## Utilisation des thèmes

Le système de thèmes s'initialise automatiquement au chargement de l'application, en détectant la préférence système de l'utilisateur ou en utilisant une préférence sauvegardée.

```typescript
// Pour appliquer manuellement un thème
import { applyTheme } from "@/lib/themes";

// Appliquer le thème sombre
applyTheme("dark");

// Appliquer le thème clair
applyTheme("light");
```

## Démonstration

Visitez la page `/style-guide` pour voir tous les éléments de la charte graphique et tester les deux thèmes. Cette page sert également de référence pour l'implémentation des composants conformes à la charte.

## Recommandations d'utilisation

1. Utilisez systématiquement les classes utilitaires définies plutôt que des styles personnalisés.
2. Respectez la hiérarchie typographique pour maintenir la cohérence visuelle.
3. Limitez l'usage des couleurs d'accent à des éléments importants pour préserver leur impact.
4. Veillez à maintenir un contraste suffisant pour l'accessibilité, particulièrement dans le thème clair.