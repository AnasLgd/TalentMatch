import React, { useState, useContext } from "react";
import { useNavigate } from "react-router-dom";
import { ChevronLeft } from "lucide-react";
import { Button } from "@/components/ui/button";
import { TalentMultiStepForm } from "@/features/consultants/components/talent-creation/TalentMultiStepForm";
import { CvAnalysisResult } from "@/features/cv-processing/types";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
  CardDescription
} from "@/components/ui/card";
import { DashboardContext } from "@/components/layout/DashboardLayout";
import { Progress } from "@/components/ui/progress";

interface CreateTalentPageProps {
  cvAnalysisResult?: CvAnalysisResult;
}

const CreateTalentPage: React.FC<CreateTalentPageProps> = ({ cvAnalysisResult }) => {
  const navigate = useNavigate();
  const [currentStep, setCurrentStep] = useState(0);
  const [totalSteps, setTotalSteps] = useState(5);

  // This will be called by the child component to update the step info
  const updateStepInfo = (current: number, total: number) => {
    setCurrentStep(current);
    setTotalSteps(total);
  };

  const handleSuccess = (consultantId: number) => {
    navigate("/consultants");
  };

  const handleCancel = () => {
    navigate("/consultants");
  };

  // Steps data for the breadcrumb footer
  const stepLabels = [
    "Infos Générales",
    "Compétences",
    "Projets",
    "Soft Skills",
    "Validation"
  ];
  // Calculate progress percentage
  const progressPercentage = ((currentStep + 1) / totalSteps) * 100;
  
  // Access sidebar state from context
  const { sidebarExpanded } = useContext(DashboardContext);
  

  return (
    <div className="relative">
      {/* Main content area with adjusted padding to account for fixed elements */}
      <div className="space-y-4 px-4 pt-2 pb-24 md:pt-4 max-w-[1400px] mx-auto">
        {/* Header with back button */}
        <div className="space-y-2 mb-4">
          <Button
            variant="ghost"
            size="sm"
            className="mb-2 text-muted-foreground hover:text-foreground shadow-sm rounded-xl bg-white border border-gray-200 transition-all hover:shadow-md"
            onClick={handleCancel}
          >
            <ChevronLeft className="mr-1 h-4 w-4" />
            Retour à la liste des talents
          </Button>

          <h1 className="text-2xl font-bold tracking-tight">
            Créer un nouveau Talent
          </h1>
          <p className="text-muted-foreground text-sm">
            Complétez les étapes pour enrichir votre vivier.
          </p>
        </div>

        {/* Two-column layout container */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
          {/* Left column (65% on desktop) - Form container */}
          <div className="lg:col-span-8">
            <Card className="rounded-2xl shadow-sm border border-gray-200 bg-white hover:shadow-md transition-all duration-300">
              <CardContent className="p-6 sm:p-8">
                <TalentMultiStepForm
                  cvAnalysisResult={cvAnalysisResult}
                  companyId={1} // In a real app, this would come from an auth context
                  onSuccess={handleSuccess}
                  onCancel={handleCancel}
                  onStepChange={updateStepInfo}
                />
              </CardContent>
            </Card>
          </div>

          {/* Right column (35% on desktop) - Qualification card */}
          <div className="lg:col-span-4">
            <Card className="rounded-2xl shadow-sm border border-gray-200 sticky top-24 bg-white hover:shadow-md transition-all duration-300">
              <CardHeader className="p-6 pb-4">
                <CardTitle className="text-lg">Qualification & Valorisation du Talent</CardTitle>
                <CardDescription>
                  Zone dédiée à l'évaluation et à la valorisation du profil consultant.
                </CardDescription>
              </CardHeader>
              <CardContent className="p-6 pt-2">
                <div className="aspect-square rounded-2xl bg-white flex items-center justify-center shadow-inner border border-gray-200">
                  <p className="text-center text-muted-foreground px-6">
                    Cette section affichera prochainement des informations enrichies sur le profil consultant
                    et les opportunités de valorisation.
                  </p>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>

      {/* Fixed footer that stays in view regardless of scroll position */}
      <div className="fixed bottom-0 left-0 right-0 z-50 pointer-events-none">
        <div className={`mx-auto transition-all duration-300 p-3 pointer-events-auto ${
          sidebarExpanded ? 'lg:ml-[calc(16rem+24px)]' : 'lg:ml-[calc(5rem+24px)]'
        } mr-3 mb-3`}>
          <div className="bg-white shadow-sm rounded-2xl border border-gray-200 py-6 px-8 h-28 flex flex-col justify-center">
          <div className="max-w-[1400px] mx-auto">
            <div className="flex justify-between items-center mb-2">
              <span className="text-sm font-medium">
                Étape {currentStep + 1} sur {totalSteps}
              </span>
              <span className="text-sm font-medium">
                {Math.round(progressPercentage)}%
              </span>
            </div>
            
            {/* Progress bar */}
            <Progress value={progressPercentage} className="h-2.5 shadow-inner bg-gray-100" indicatorClassName="bg-emerald-500" />
            
            {/* Step labels - Hidden on mobile for better spacing */}
            <div className="flex items-center pt-4 overflow-x-auto no-scrollbar">
              <div className="flex space-x-3 items-center text-sm">
                {stepLabels.map((label, index) => (
                  <React.Fragment key={index}>
                    <span className={`whitespace-nowrap px-3 py-1 rounded-lg transition-all ${
                      index === currentStep
                        ? 'font-semibold text-emerald-600 bg-emerald-50 border border-emerald-200 shadow-sm'
                        : index < currentStep
                          ? 'text-emerald-600 bg-emerald-50/50'
                          : 'text-muted-foreground'
                    }`}>
                      {label}
                    </span>
                    {index < stepLabels.length - 1 && (
                      <span className="text-muted-foreground">›</span>
                    )}
                  </React.Fragment>
                ))}
              </div>
            </div>
          </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CreateTalentPage;