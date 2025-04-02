
import React from "react";

interface LogoSectionProps {
  className?: string;
}

const LogoSection: React.FC<LogoSectionProps> = ({ className = "" }) => {
  return (
    <div className={`flex flex-col items-center ${className}`}>
      <div className="flex items-center">
        <span className="bg-primary rounded-lg p-2">
          <svg 
            xmlns="http://www.w3.org/2000/svg" 
            width="24" 
            height="24" 
            viewBox="0 0 24 24" 
            fill="none" 
            stroke="currentColor" 
            strokeWidth="2" 
            strokeLinecap="round" 
            strokeLinejoin="round" 
            className="text-primary-foreground"
          >
            <path d="M17 18a2 2 0 0 1-2 2H9a2 2 0 0 1-2-2V9a2 2 0 0 1 2-2h6a2 2 0 0 1 2 2v9Z"></path>
            <path d="m12 12 4-4"></path>
            <path d="M8 8v4"></path>
            <path d="M8 12h4"></path>
          </svg>
        </span>
        <h1 className="text-2xl font-bold ml-2">TalentMatch</h1>
      </div>
      <p className="text-muted-foreground text-sm mt-2">La plateforme de matching pour les ESN</p>
    </div>
  );
};

export default LogoSection;
