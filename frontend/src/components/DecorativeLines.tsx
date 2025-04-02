
import React from 'react';

interface DecoLineProps {
  color: string;
  width: string;
  height: string;
  position: string;
  path: string;
  thickness?: number;
  opacity?: number;
  rotate?: string;
}

const DecoLine: React.FC<DecoLineProps> = ({ 
  color, 
  width, 
  height, 
  position, 
  path,
  thickness = 3.0, // Épaisseur augmentée selon le guide
  opacity = 0.5, // Opacité ajustée
  rotate = '0deg'
}) => {
  // Identifiant unique pour le gradient
  const gradientId = `deco-gradient-${color.replace(/[^a-zA-Z0-9]/g, '')}-${position}`;

  return (
    <div 
      className="absolute pointer-events-none z-[-5]" 
      style={{ 
        ...parsePosition(position),
        width, 
        height,
        transform: `rotate(${rotate})`,
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
          strokeLinecap="round"
          fill="none"
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

const DecorativeLines: React.FC = () => {
  return (
    <>
      {/* Ligne décorative qui traverse complètement la page horizontalement */}
      <DecoLine 
        color="#a5e9b3" // Vert principal du guide
        width="150vw" 
        height="300px" 
        position="top-24 left-0" 
        path="M0 50 C20 20, 50 80, 150 30"
        thickness={3.4}
        opacity={0.5}
      />
      
      {/* Ligne sinueuse complète qui traverse en diagonale */}
      <DecoLine 
        color="#93e9be" // Vert secondaire du guide
        width="120vw" 
        height="120vh" 
        position="top-[20%] right-0" 
        path="M120 0 C70 30, 30 70, 0 120"
        thickness={3.3}
        opacity={0.45}
      />
      
      {/* Ligne centrale qui traverse totalement */}
      <DecoLine 
        color="#1a1a1a" // Noir du guide (très subtil)
        width="150vw" 
        height="40vh" 
        position="top-[50%] left-0" 
        path="M0 20 C30 30, 70 10, 150 40"
        thickness={2.8}
        opacity={0.2}
      />
      
      {/* Ligne courbe complète en bas de page */}
      <DecoLine 
        color="#777777" // Gris moyen du guide
        width="130vw" 
        height="300px" 
        position="bottom-[20%] left-0" 
        path="M0 70 C30 30, 70 80, 130 20"
        thickness={3.0}
        opacity={0.25}
      />
      
      {/* Ligne qui forme une vague traversant complètement */}
      <DecoLine 
        color="#333333" // Gris foncé du guide
        width="150vw" 
        height="300px" 
        position="bottom-40 left-0" 
        path="M0 50 C25 20, 50 80, 75 20 S125 50, 150 30"
        thickness={3.2}
        opacity={0.3}
      />
      
      {/* Ligne verticale complète */}
      <DecoLine 
        color="#a5e9b3" // Vert principal du guide
        width="300px" 
        height="150vh" 
        position="top-[10%] right-[20%]" 
        path="M50 0 C30 50, 70 100, 50 150"
        thickness={3.1}
        opacity={0.35}
      />
      
      {/* Grande ligne traversant diagonalement */}
      <DecoLine 
        color="#93e9be" // Vert secondaire du guide
        width="120vw" 
        height="120vh" 
        position="top-[35%] left-[10%]" 
        path="M0 0 C40 40, 60 80, 120 120"
        thickness={3.0}
        opacity={0.3}
      />
    </>
  );
};

export default DecorativeLines;
