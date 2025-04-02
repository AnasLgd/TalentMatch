
import React from 'react';

interface LineProps {
  color: string;
  path: string;
  width: string;
  height: string;
  position: string;
  zIndex?: number;
  thickness?: number;
  opacity?: number;
}

const ColorLine: React.FC<LineProps> = ({ 
  color, 
  path,
  width,
  height,
  position,
  zIndex = -10,
  thickness = 3.2, // Épaisseur augmentée selon le guide
  opacity = 0.6 // Opacité ajustée
}) => {
  // Créer un gradient unique pour chaque ligne
  const gradientId = `line-gradient-${color.replace(/[^a-zA-Z0-9]/g, '')}`;
  
  return (
    <div 
      className="absolute pointer-events-none" 
      style={{ 
        width,
        height,
        ...parsePosition(position),
        zIndex
      }}
    >
      <svg width="100%" height="100%" viewBox="0 0 100 100" preserveAspectRatio="none">
        <defs>
          <linearGradient id={gradientId} x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor={color} stopOpacity={opacity} />
            <stop offset="50%" stopColor={color} stopOpacity={opacity} />
            <stop offset="100%" stopColor={color} stopOpacity={opacity} />
          </linearGradient>
        </defs>
        
        <path
          d={path}
          stroke={`url(#${gradientId})`}
          strokeWidth={thickness}
          fill="none"
          strokeLinecap="round"
        />
      </svg>
    </div>
  );
};

// Fonction pour parser la position (ex: "top-10 left-0")
function parsePosition(position: string): React.CSSProperties {
  const styles: React.CSSProperties = {};
  const parts = position.split(' ');
  
  parts.forEach(part => {
    if (part.startsWith('top-')) {
      styles.top = part.replace('top-', '');
    } else if (part.startsWith('bottom-')) {
      styles.bottom = part.replace('bottom-', '');
    } else if (part.startsWith('left-')) {
      styles.left = part.replace('left-', '');
    } else if (part.startsWith('right-')) {
      styles.right = part.replace('right-', '');
    }
  });
  
  return styles;
}

const ColoredLines: React.FC = () => {
  return (
    <>
      {/* Ligne complète traversant toute la page en diagonale */}
      <ColorLine 
        color="#a5e9b3" // Vert principal du guide de style
        path="M0 0 C20 30, 50 60, 100 100" 
        width="100vw" 
        height="200vh" 
        position="top-0 left-0" 
        thickness={3.2}
        opacity={0.5}
      />
      
      {/* Grande ligne sinueuse traversant la page d'un bout à l'autre */}
      <ColorLine 
        color="#93e9be" // Vert secondaire du guide
        path="M0 30 Q25 10, 50 50 T100 30" 
        width="120vw" 
        height="180vh" 
        position="top-[10%] left-0"
        thickness={3.5}
        opacity={0.45}
      />
      
      {/* Ligne qui traverse verticalement toute la page */}
      <ColorLine 
        color="#1a1a1a" // Noir du guide de style (très subtil)
        path="M70 0 Q60 50, 80 200" 
        width="100vw" 
        height="200vh" 
        position="top-0 left-0" 
        thickness={2.8}
        opacity={0.2}
      />
      
      {/* Ligne qui traverse dans la partie inférieure */}
      <ColorLine 
        color="#777777" // Gris moyen du guide
        path="M0 140 Q50 160, 100 120" 
        width="100vw" 
        height="200vh" 
        position="top-0 left-0" 
        thickness={3.0}
        opacity={0.25}
      />
      
      {/* Ligne qui croise les autres de manière structurée */}
      <ColorLine 
        color="#333333" // Gris foncé du guide
        path="M20 10 Q50 100, 80 190" 
        width="100vw" 
        height="200vh" 
        position="top-0 left-0" 
        thickness={3.3}
        opacity={0.2}
      />
    </>
  );
};

export default ColoredLines;
