import React from "react";
import { Moon } from "lucide-react";
import { Button } from "./button";

// Version simplifiée du ThemeSwitcher qui ne fait rien
// Gardé uniquement pour éviter les erreurs d'importation
const ThemeSwitcher = () => {
  return (
    <Button 
      variant="ghost" 
      size="icon" 
      title="Thème sombre"
      className="relative hover:bg-accent hover:text-accent-foreground"
    >
      <Moon className="h-5 w-5" />
    </Button>
  );
};

export default ThemeSwitcher;