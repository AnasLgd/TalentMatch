import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { FileText } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Container } from "@/components/ui/container";
import CVUploadPage from "../features/cv-processing/components/CVUploadPage";

// Define the tabs for the CV Analysis page
type AnalysisTab = "upload" | "history" | "templates";

const CvAnalysis = () => {
  const [activeTab, setActiveTab] = useState<AnalysisTab>("upload");
  const navigate = useNavigate();

  return (
    <Container className="py-4">
      <div className="mb-6">
        <h1 className="text-3xl font-bold tracking-tight">Analyse et parsing de CV</h1>
        <p className="text-muted-foreground mt-1">
          Uploadez des CV pour extraire automatiquement les informations et créer des profils consultants
        </p>
      </div>

      <Tabs
        defaultValue="upload"
        value={activeTab}
        onValueChange={(value) => setActiveTab(value as AnalysisTab)}
        className="w-full"
      >
        <TabsList className="grid grid-cols-3 w-full max-w-md mb-8">
          <TabsTrigger value="upload">Upload CV</TabsTrigger>
          <TabsTrigger value="history">Historique</TabsTrigger>
          <TabsTrigger value="templates">Modèles</TabsTrigger>
        </TabsList>

        <TabsContent value="upload" className="mt-0">
          <CVUploadPage />
        </TabsContent>

        <TabsContent value="history" className="mt-0">
          <div className="flex flex-col items-center justify-center py-12 text-center">
            <FileText className="h-16 w-16 text-muted-foreground mb-4" />
            <h3 className="text-xl font-semibold mb-2">Historique des CV analysés</h3>
            <p className="text-muted-foreground mb-6 max-w-md">
              Consultez l'historique des CV précédemment analysés et leur statut de traitement.
              Cette fonctionnalité sera disponible prochainement.
            </p>
            <Button 
              variant="outline" 
              onClick={() => setActiveTab("upload")}
            >
              Revenir à l'upload
            </Button>
          </div>
        </TabsContent>

        <TabsContent value="templates" className="mt-0">
          <div className="flex flex-col items-center justify-center py-12 text-center">
            <FileText className="h-16 w-16 text-muted-foreground mb-4" />
            <h3 className="text-xl font-semibold mb-2">Modèles de CV</h3>
            <p className="text-muted-foreground mb-6 max-w-md">
              Créez et gérez des modèles de CV pour une extraction de données optimisée.
              Cette fonctionnalité sera disponible prochainement.
            </p>
            <Button 
              variant="outline" 
              onClick={() => setActiveTab("upload")}
            >
              Revenir à l'upload
            </Button>
          </div>
        </TabsContent>
      </Tabs>
    </Container>
  );
};

export default CvAnalysis;
