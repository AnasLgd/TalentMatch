// Définition simplifiée du thème basée sur la capture d'écran
// Version simplifiée qui reproduit fidèlement l'image de référence

// Couleurs principales du thème sombre - conforme à l'image fournie
const themeColors = {
  // Couleurs de fond - fonds très sombres presque noirs avec nuance bleue
  background: "222 33% 11%", // Fond principal très sombre
  foreground: "210 40% 98%", // Texte clair sur fond sombre
  
  // Éléments de carte
  card: "223 35% 13%", // Fond de carte légèrement plus clair que le fond principal
  cardForeground: "210 40% 98%", // Texte des cartes
  
  // Popover et menus déroulants
  popover: "223 35% 13%", 
  popoverForeground: "210 40% 98%",
  
  // Couleur accent principale - émeraude profond comme demandé
  primary: "160 84% 39%", // Émeraude pour les accents
  primaryForeground: "222 33% 11%", // Texte sombre sur fond accent
  
  // Couleur secondaire - utilisée pour les bordures, séparateurs
  secondary: "215 25% 24%", // Gris bleuté pour les éléments secondaires
  secondaryForeground: "210 40% 98%",
  
  // Éléments atténués et textes secondaires
  muted: "215 28% 17%",
  mutedForeground: "218 12% 75%",
  
  // Accent - même que primary pour cohérence
  accent: "160 84% 39%",
  accentForeground: "222 33% 11%",
  
  // Couleur destructive pour les actions d'alerte
  destructive: "0 63% 31%", 
  destructiveForeground: "210 40% 98%",
  
  // Bordures, inputs et éléments d'interface
  border: "215 25% 24%",
  input: "215 25% 24%",
  ring: "160 84% 39%",
  
  // Valeur de l'arrondi des coins
  radius: "0.75rem",
};

// Fonction pour appliquer le thème au document
export function applyTheme() {
  const root = document.documentElement;
  
  // Appliquer les variables CSS du thème
  Object.entries(themeColors).forEach(([key, value]) => {
    root.style.setProperty(`--${key}`, value as string);
  });
}

// Fonction d'initialisation appelée au chargement de l'application
export function initializeTheme() {
  applyTheme();
}

export default themeColors;