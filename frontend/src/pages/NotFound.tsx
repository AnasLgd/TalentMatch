
import React from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { ArrowLeft } from "lucide-react";

const NotFound = () => {
  const navigate = useNavigate();
  
  return (
    <div className="min-h-screen bg-background flex flex-col items-center justify-center px-6 py-8">
      <div className="flex items-center justify-center w-16 h-16 rounded-full bg-muted/20 mb-8">
        <span className="text-4xl">404</span>
      </div>
      <h1 className="text-3xl font-bold tracking-tight mb-2">Page introuvable</h1>
      <p className="text-muted-foreground text-center max-w-md mb-8">
        La page que vous recherchez n'existe pas ou a été déplacée. Veuillez vérifier l'URL ou revenir à la page d'accueil.
      </p>
      <div className="flex gap-4">
        <Button onClick={() => navigate(-1)}>
          <ArrowLeft className="mr-2 h-4 w-4" />
          Retour
        </Button>
        <Button variant="outline" onClick={() => navigate("/dashboard")}>
          Dashboard
        </Button>
      </div>
    </div>
  );
};

export default NotFound;
