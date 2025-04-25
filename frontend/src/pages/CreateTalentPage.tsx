import React from "react";
import { useNavigate } from "react-router-dom";
import { ChevronLeft } from "lucide-react";
import { Button } from "@/components/ui/button";
import { TalentMultiStepForm } from "@/features/consultants/components/talent-creation/TalentMultiStepForm";
import { CvAnalysisResult } from "@/features/cv-processing/types";

interface CreateTalentPageProps {
  cvAnalysisResult?: CvAnalysisResult;
}

const CreateTalentPage: React.FC<CreateTalentPageProps> = ({ cvAnalysisResult }) => {
  const navigate = useNavigate();

  const handleSuccess = (consultantId: number) => {
    navigate("/consultants");
  };

  const handleCancel = () => {
    navigate("/consultants");
  };

  return (
    <div className="space-y-8 p-8 max-w-[1200px] mx-auto">
      {/* Header with back button */}
      <div className="space-y-2">
        <Button
          variant="ghost"
          size="sm"
          className="mb-2 text-muted-foreground hover:text-foreground"
          onClick={handleCancel}
        >
          <ChevronLeft className="mr-1 h-4 w-4" />
          Retour à la liste des talents
        </Button>

        <h1 className="text-3xl font-bold tracking-tight">
          Créer un nouveau Talent
        </h1>
        <p className="text-muted-foreground">
          Complétez les étapes pour enrichir votre vivier.
        </p>
      </div>

      {/* Main content - Using a light background container for better visual separation */}
      <div className="bg-muted/30 p-6 rounded-lg">
        <div className="max-w-[900px] mx-auto">
          <TalentMultiStepForm
            cvAnalysisResult={cvAnalysisResult}
            companyId={1} // In a real app, this would come from an auth context
            onSuccess={handleSuccess}
            onCancel={handleCancel}
          />
        </div>
      </div>

      {/* Future placeholder for preview panel */}
      <div className="hidden lg:block fixed top-1/4 right-8 w-64 h-96 border border-dashed border-muted-foreground/30 rounded-lg">
        {/* This space is reserved for a future preview component */}
      </div>
    </div>
  );
};

export default CreateTalentPage;