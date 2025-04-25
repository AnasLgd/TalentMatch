import React from "react";
import { Moon, Sun } from "lucide-react";
import { Button } from "./button";
import { useTheme } from "@/providers/ThemeProvider";
import { applyTheme } from "@/lib/themes";

const ThemeSwitcher = () => {
  const { theme, setTheme } = useTheme();

  const toggleTheme = () => {
    const newTheme = theme === 'dark' ? 'light' : 'dark';
    setTheme(newTheme);
    applyTheme(newTheme);
  };

  return (
    <Button 
      variant="ghost" 
      size="icon" 
      title={theme === 'dark' ? "Passer au thème clair" : "Passer au thème sombre"}
      className="relative hover:bg-accent hover:text-accent-foreground transition-colors duration-200"
      onClick={toggleTheme}
    >
      {theme === 'dark' ? (
        <Sun className="h-5 w-5 transition-transform duration-200" />
      ) : (
        <Moon className="h-5 w-5 transition-transform duration-200" />
      )}
    </Button>
  );
};

export default ThemeSwitcher;