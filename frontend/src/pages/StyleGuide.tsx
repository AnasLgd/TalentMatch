import React from "react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";

// Version simplifiée du StyleGuide (placeholder uniquement)
const StyleGuide = () => {
  return (
    <div className="container mx-auto py-12 space-y-8">
      <div className="text-center">
        <h1 className="text-3xl font-bold">Guide de style TalentMatch</h1>
        <p className="text-muted-foreground mt-2">
          Visualisation des composants et styles du thème
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <CardTitle>Interface en thème sombre</CardTitle>
            <CardDescription>
              Reproduction fidèle de l'image de référence
            </CardDescription>
          </CardHeader>
          <CardContent>
            <p>
              L'interface utilise un thème sombre avec des accents émeraude
              pour reproduire exactement l'interface montrée dans l'image.
            </p>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default StyleGuide;