import React, { useState, useMemo } from "react";
import { useNavigate } from "react-router-dom";
import { ChevronLeft, Loader2 } from "lucide-react";

import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";
import { Separator } from "@/components/ui/separator";

import { TalentMultiStepForm, TalentFormActions } from "@/features/consultants/components/talent-creation/form/TalentMultiStepForm";
import { useTheme } from "@/providers/ThemeProvider";

/**
 * CreateTalentPage - A page for creating new talent profiles
 * 
 * This page provides a full-page experience for creating new talent profiles, with
 * a multi-step form and navigation controls.
 */
const CreateTalentPage: React.FC = () => {
  const navigate = useNavigate();
  const { theme } = useTheme();
  
  // State for managing form progress
  const [formActions, setFormActions] = useState<TalentFormActions | null>(null);
  const [currentStep, setCurrentStep] = useState<number>(0);
  const [totalSteps, setTotalSteps] = useState<number>(5);
  
  // Mock company ID for demo purposes
  const companyId = 1;
  
  // Calculate progress percentage
  const progressPercentage = useMemo(() => {
    return Math.round((currentStep / (totalSteps - 1)) * 100);
  }, [currentStep, totalSteps]);
  
  // Handle step change
  const handleStepChange = (current: number, total: number) => {
    setCurrentStep(current);
    setTotalSteps(total);
  };
  
  // Handle form actions ready callback
  const handleFormActionsReady = (actions: TalentFormActions) => {
    setFormActions(actions);
  };
  
  // Handle cancel action
  const handleCancel = () => {
    navigate("/consultants");
  };
  
  return (
    <div className="relative bg-gray-50 min-h-screen">
      {/* Main content area with adjusted padding to account for fixed elements */}
      <div className="space-y-4 px-4 pt-2 pb-32 md:pt-4 max-w-[1600px] mx-auto">
        {/* Header with back button */}
        <div className="flex items-center gap-2 mb-4">
          <Button
            variant="ghost"
            size="icon"
            onClick={() => navigate("/consultants")}
            className="rounded-full hover:bg-gray-100"
          >
            <ChevronLeft className="h-4 w-4" />
          </Button>
          <h1 className="text-sm font-medium text-muted-foreground">Retour à la liste des talents</h1>
        </div>
        
        {/* Main content card */}
        <Card className="p-4 md:p-6 bg-white rounded-xl shadow-md">
          <CardHeader className="px-0 pt-0">
            <CardTitle className="text-2xl font-bold mb-1">Création d'un nouveau talent</CardTitle>
            <CardDescription>
              Créez un nouveau profil de talent en suivant les étapes ci-dessous
            </CardDescription>
          </CardHeader>
          
          {/* Content area */}
          <CardContent className="px-0 pb-4">
            {/* Full width form */}
            <TalentMultiStepForm
              companyId={companyId}
              onCancel={handleCancel}
              onStepChange={handleStepChange}
              onFormActionsReady={handleFormActionsReady}
            />
          </CardContent>
        </Card>
      </div>
      
      {/* Fixed footer with steps - soft UI style */}
      <div className="fixed bottom-0 left-0 right-0 z-10 px-4 pb-4">
        <div className="max-w-[1600px] mx-auto">
          <div className="ml-[220px] bg-white rounded-xl border border-gray-100 shadow-lg p-4">
            <div className="flex flex-col md:flex-row md:items-center md:justify-between space-y-3 md:space-y-0 w-full">
              {/* Left side: Progress information and steps */}
              <div className="flex-1 mr-6 space-y-2 flex flex-col justify-center">
                {/* Progress percentage and bar */}
                <div className="flex justify-between items-center">
                  <span className="text-sm font-medium text-gray-700">Étape {currentStep + 1} sur {totalSteps}</span>
                  <span className="text-sm font-medium text-emerald-600">{progressPercentage}%</span>
                </div>
                <Progress value={progressPercentage} className="h-3 bg-gray-100 rounded-full shadow-inner" />
                
                {/* Step markers */}
                <div className="flex justify-between mt-3">
                  <div 
                    className={`flex flex-col items-center ${currentStep === 0 ? 'text-emerald-600' : 'text-gray-400'}`}
                  >
                    <div className={`w-4 h-4 rounded-full mb-1.5 transition-all duration-300 shadow-sm ${currentStep === 0 ? 'bg-emerald-600 ring-2 ring-emerald-100' : 'bg-gray-200'}`}></div>
                    <span className="text-xs font-medium">Identité</span>
                  </div>
                  <div 
                    className={`flex flex-col items-center ${currentStep === 1 ? 'text-emerald-600' : 'text-gray-400'}`}
                  >
                    <div className={`w-4 h-4 rounded-full mb-1.5 transition-all duration-300 shadow-sm ${currentStep === 1 ? 'bg-emerald-600 ring-2 ring-emerald-100' : 'bg-gray-200'}`}></div>
                    <span className="text-xs font-medium">Compétences</span>
                  </div>
                  <div 
                    className={`flex flex-col items-center ${currentStep === 2 ? 'text-emerald-600' : 'text-gray-400'}`}
                  >
                    <div className={`w-4 h-4 rounded-full mb-1.5 transition-all duration-300 shadow-sm ${currentStep === 2 ? 'bg-emerald-600 ring-2 ring-emerald-100' : 'bg-gray-200'}`}></div>
                    <span className="text-xs font-medium">Projets</span>
                  </div>
                  <div 
                    className={`flex flex-col items-center ${currentStep === 3 ? 'text-emerald-600' : 'text-gray-400'}`}
                  >
                    <div className={`w-4 h-4 rounded-full mb-1.5 transition-all duration-300 shadow-sm ${currentStep === 3 ? 'bg-emerald-600 ring-2 ring-emerald-100' : 'bg-gray-200'}`}></div>
                    <span className="text-xs font-medium">Soft Skills</span>
                  </div>
                  <div 
                    className={`flex flex-col items-center ${currentStep === 4 ? 'text-emerald-600' : 'text-gray-400'}`}
                  >
                    <div className={`w-4 h-4 rounded-full mb-1.5 transition-all duration-300 shadow-sm ${currentStep === 4 ? 'bg-emerald-600 ring-2 ring-emerald-100' : 'bg-gray-200'}`}></div>
                    <span className="text-xs font-medium">Validation</span>
                  </div>
                </div>
              </div>
              
              {/* Right side: Action buttons with soft UI style */}
              <div className="flex gap-4 justify-end items-center">
                {/* Cancel button */}
                <Button
                  type="button"
                  variant="outline"
                  onClick={handleCancel}
                  className="rounded-xl bg-white border-gray-200 shadow-sm hover:shadow-md hover:bg-gray-50 transition-all duration-300"
                >
                  Annuler
                </Button>
                
                {/* Save and exit button */}
                <Button
                  type="button"
                  variant="secondary"
                  onClick={() => formActions?.handleSaveAndExit()}
                  disabled={!formActions || formActions.isSubmitting || formActions.isSaving}
                  className="rounded-xl bg-gray-50 border border-gray-200 shadow-sm hover:shadow-md hover:bg-gray-100 transition-all duration-300"
                >
                  {formActions?.isSaving && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
                  Sauvegarder et quitter
                </Button>
                
                {/* Next/Submit button */}
                <Button
                  type="button"
                  onClick={() => formActions?.handleNext()}
                  disabled={!formActions || formActions.isSubmitting || formActions.isSaving}
                  className="rounded-xl shadow-sm hover:shadow-md transition-all duration-300 bg-emerald-600 hover:bg-emerald-500 text-white min-w-[120px] border border-emerald-500"
                >
                  {(formActions?.isSubmitting || formActions?.isSaving) && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
                  {currentStep < totalSteps - 1 ? "Suivant" : "Finaliser"}
                </Button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CreateTalentPage;