
import React from 'react';

interface SectionConnectorProps {
  color: string;
  start: 'top-left' | 'top-right' | 'bottom-left' | 'bottom-right';
  end: 'top-left' | 'top-right' | 'bottom-left' | 'bottom-right';
  section: string;
  thickness?: number;
}

const SectionConnector: React.FC<SectionConnectorProps> = ({ 
  color, 
  start, 
  end, 
  section,
  thickness = 3.2 // Épaisseur augmentée selon le guide
}) => {
  // Déterminer la position de départ
  const startPosition = (): string => {
    switch (start) {
      case 'top-left': return 'top-0 left-0';
      case 'top-right': return 'top-0 right-0';
      case 'bottom-left': return 'bottom-0 left-0';
      case 'bottom-right': return 'bottom-0 right-0';
      default: return 'top-0 left-0';
    }
  };

  // Créer un chemin SVG qui traverse complètement
  const pathStyle = (): string => {
    if (start === 'top-left' && end === 'bottom-right') {
      return 'M0 0 C20 30, 50 50, 70 70 S90 90, 100 100';
    } else if (start === 'top-right' && end === 'bottom-left') {
      return 'M100 0 C80 30, 60 50, 40 70 S10 90, 0 100';
    } else if (start === 'bottom-left' && end === 'top-right') {
      return 'M0 100 C20 70, 40 50, 60 30 S80 10, 100 0';
    } else if (start === 'bottom-right' && end === 'top-left') {
      return 'M100 100 C80 70, 60 50, 40 30 S20 10, 0 0';
    } else {
      return 'M0 0 C25 25, 75 25, 50 50 S25 75, 100 100';
    }
  };

  // ID unique pour le gradient
  const gradientId = `connector-gradient-${section}`;

  return (
    <div 
      className={`absolute ${startPosition()} w-24 h-64 md:w-48 md:h-96 pointer-events-none z-[-5]`}
      data-section={section}
    >
      <svg width="100%" height="100%" viewBox="0 0 100 100" preserveAspectRatio="none">
        <defs>
          <linearGradient id={gradientId} x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor={color} stopOpacity="0.5" />
            <stop offset="50%" stopColor={color} stopOpacity="0.55" />
            <stop offset="100%" stopColor={color} stopOpacity="0.5" />
          </linearGradient>
        </defs>
        <path
          d={pathStyle()}
          stroke={`url(#${gradientId})`}
          strokeWidth={thickness}
          strokeLinecap="round"
          fill="none"
        />
      </svg>
    </div>
  );
};

// Composant qui regroupe plusieurs connecteurs pour différentes sections
const SectionConnectors: React.FC = () => {
  return (
    <>
      {/* Connecteur entre Hero et About */}
      <div className="absolute w-full h-24 bottom-0 left-0 overflow-hidden z-[-5]" style={{ bottom: '-12px' }} id="hero-to-about">
        <SectionConnector 
          color="#a5e9b3" // Vert principal du guide
          start="bottom-right" 
          end="top-left" 
          section="hero-about" 
          thickness={3.3}
        />
      </div>
      
      {/* Connecteur entre About et Projects */}
      <div className="absolute w-full h-24 bottom-0 left-0 overflow-hidden z-[-5]" style={{ bottom: '-12px' }} id="about-to-projects">
        <SectionConnector 
          color="#93e9be" // Vert secondaire du guide
          start="bottom-left" 
          end="top-right" 
          section="about-projects" 
          thickness={3.2}
        />
      </div>
      
      {/* Connecteur entre Projects et CTA */}
      <div className="absolute w-full h-24 bottom-0 left-0 overflow-hidden z-[-5]" style={{ bottom: '-12px' }} id="projects-to-cta">
        <SectionConnector 
          color="#a5e9b3" // Vert principal du guide
          start="bottom-right" 
          end="top-left" 
          section="projects-cta" 
          thickness={3.3}
        />
      </div>
      
      {/* Connecteur entre CTA et Contact */}
      <div className="absolute w-full h-24 bottom-0 left-0 overflow-hidden z-[-5]" style={{ bottom: '-12px' }} id="cta-to-contact">
        <SectionConnector 
          color="#93e9be" // Vert secondaire du guide
          start="bottom-left" 
          end="top-right" 
          section="cta-contact" 
          thickness={3.2}
        />
      </div>
      
      {/* Connecteur entre Contact et Footer */}
      <div className="absolute w-full h-24 bottom-0 left-0 overflow-hidden z-[-5]" style={{ bottom: '-12px' }} id="contact-to-footer">
        <SectionConnector 
          color="#a5e9b3" // Vert principal du guide
          start="bottom-right" 
          end="top-left" 
          section="contact-footer" 
          thickness={3.0}
        />
      </div>
    </>
  );
};

export default SectionConnectors;
