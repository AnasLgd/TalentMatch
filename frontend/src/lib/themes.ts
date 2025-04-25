// Définition des thèmes clair et sombre pour l'application

// Types pour les thèmes
export type ThemeMode = 'dark' | 'light';

// Couleurs du thème sombre - conforme aux valeurs actuelles de l'application
const darkThemeColors = {
  background: "222 33% 11%", // Fond principal très sombre
  foreground: "210 40% 98%", // Texte clair sur fond sombre
  
  card: "223 35% 13%", // Fond de carte légèrement plus clair que le fond principal
  cardForeground: "210 40% 98%", // Texte des cartes
  
  popover: "223 35% 13%", 
  popoverForeground: "210 40% 98%",
  
  primary: "152 69% 65%", // Émeraude pour les accents
  primaryForeground: "222 33% 11%", // Texte sombre sur fond accent
  
  secondary: "215 25% 24%", // Gris bleuté pour les éléments secondaires
  secondaryForeground: "210 40% 98%",
  
  muted: "215 28% 17%",
  mutedForeground: "218 12% 65%",
  
  accent: "152 69% 65%",
  accentForeground: "222 33% 11%",
  
  destructive: "0 63% 31%", 
  destructiveForeground: "210 40% 98%",
  
  border: "215 25% 24%",
  input: "215 25% 24%",
  ring: "152 69% 65%",
  
  radius: "0.75rem",
};

// Couleurs du thème clair - basé sur les valeurs définies dans index.css
const lightThemeColors = {
  background: "210 40% 98%", 
  foreground: "222 33% 11%",
  
  card: "0 0% 100%",
  cardForeground: "222 33% 11%",
  
  popover: "0 0% 100%",
  popoverForeground: "222 33% 11%",
  
  primary: "152 75% 40%",
  primaryForeground: "0 0% 100%",
  
  secondary: "210 20% 93%",
  secondaryForeground: "222 33% 20%",
  
  muted: "210 20% 93%",
  mutedForeground: "215 25% 40%",
  
  accent: "152 75% 40%",
  accentForeground: "0 0% 100%",
  
  destructive: "0 85% 60%",
  destructiveForeground: "0 0% 100%",
  
  border: "215 20% 85%",
  input: "215 20% 85%",
  ring: "152 75% 40%",
  
  radius: "0.75rem",
};

// Mapper toutes les clés pour les noms de variables CSS corrects
const cssVarMap: Record<string, string> = {
  cardForeground: "card-foreground",
  popoverForeground: "popover-foreground",
  primaryForeground: "primary-foreground",
  secondaryForeground: "secondary-foreground",
  mutedForeground: "muted-foreground",
  accentForeground: "accent-foreground",
  destructiveForeground: "destructive-foreground",
  // Les autres clés restent identiques
};

// Fonction pour appliquer un thème spécifique
export function applyTheme(mode: ThemeMode = 'dark') {
  const root = document.documentElement;
  const colors = mode === 'dark' ? darkThemeColors : lightThemeColors;
  
  // Appliquer les variables CSS du thème
  Object.entries(colors).forEach(([key, value]) => {
    const cssVar = cssVarMap[key] || key;
    root.style.setProperty(`--${cssVar}`, value as string);
  });
}

// Fonction pour détecter les préférences du système
export function getSystemThemePreference(): ThemeMode {
  return window.matchMedia('(prefers-color-scheme: light)').matches ? 'light' : 'dark';
}

// Fonction d'initialisation appelée au chargement de l'application
export function initializeTheme() {
  // Récupérer le thème sauvegardé ou utiliser la préférence système
  const savedTheme = localStorage.getItem('theme') as ThemeMode | null;
  const preferredTheme = savedTheme || getSystemThemePreference();
  
  // Appliquer le thème
  applyTheme(preferredTheme);
  
  // Appliquer également la classe CSS pour Tailwind
  document.documentElement.classList.toggle('light', preferredTheme === 'light');
}

// Exporter les thèmes pour utilisation ailleurs dans l'application
export const themes = {
  dark: darkThemeColors,
  light: lightThemeColors,
};