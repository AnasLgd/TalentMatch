import React, { useState, useEffect, useCallback } from "react";
import { useForm, FormProvider } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Loader2 } from "lucide-react";
import { IdentityStep } from "./steps/IdentityStep";
import { SkillsStep } from "./steps/SkillsStep";
import { ProjectsStep } from "./steps/ProjectsStep";
import { SoftSkillsStep } from "./steps/SoftSkillsStep";
import { SummaryStep } from "./steps/SummaryStep";
import { QualificationSidebar } from "../common/QualificationSidebar";
import { CvAnalysisResult } from "@/features/cv-processing/types";
import { toast } from "@/hooks/use-toast";
import { AvailabilityStatus, ConsultantCreate } from "../../../types";
import { consultantService } from "../../../services/consultant-service";

// Define the form schema 
export type TalentFormActions = {
  handleNext: () => Promise<void>;
  handlePrevious: () => Promise<void>;
  handleSaveAndExit: () => Promise<void>;
  isSubmitting: boolean;
  isSaving: boolean;
  currentStep: number;
  totalSteps: number;
};

interface TalentMultiStepFormProps {
  cvAnalysisResult?: CvAnalysisResult;
  companyId: number;
  onSuccess?: (consultantId: number) => void;
  onCancel?: () => void;
  onStepChange?: (currentStep: number, totalSteps: number) => void;
  renderButtons?: boolean;
  onFormActionsReady?: (actions: TalentFormActions) => void;
}

export const TalentMultiStepForm: React.FC<TalentMultiStepFormProps> = ({
  cvAnalysisResult,
  companyId,
  onSuccess,
  onCancel,
  onStepChange,
  renderButtons = false,
  onFormActionsReady,
}) => {
  const navigate = useNavigate();
  
  // Step tracking
  const [currentStep, setCurrentStep] = useState(0);
  const totalSteps = 5;
  
  // Form status tracking
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isSaving, setIsSaving] = useState(false);
  const [lastSaved, setLastSaved] = useState<Date | null>(null);
  
  // Tracking prefilled fields
  const [autoFilledFields] = useState<string[]>([]);
  
  // Save consultant ID for updates
  const [savedConsultantId, setSavedConsultantId] = useState<number | null>(null);

  // Form setup
  const methods = useForm({
    defaultValues: {
      first_name: "",
      last_name: "",
      title: "",
      experience_years: undefined,
      skills: [],
      projects: [],
      soft_skills: [],
      remote_work: false,
      company_id: companyId,
      user_id: null,
      hr_status: "SOURCED",
    },
  });

  // Notify parent component about step changes
  useEffect(() => {
    if (onStepChange) {
      onStepChange(currentStep, totalSteps);
    }
  }, [currentStep, totalSteps, onStepChange]);

  // Handle next step
  const handleNext = useCallback(async () => {
    if (currentStep < totalSteps - 1) {
      setCurrentStep(prev => prev + 1);
    }
  }, [currentStep, totalSteps]);
  
  // Handle previous step
  const handlePrevious = useCallback(async () => {
    if (currentStep > 0) {
      setCurrentStep(prev => prev - 1);
    }
  }, [currentStep]);

  // Handle save and exit
  const handleSaveAndExit = useCallback(async () => {
    if (onCancel) {
      onCancel();
    } else {
      navigate("/consultants");
    }
  }, [navigate, onCancel]);

  // Expose form actions to parent component
  useEffect(() => {
    if (onFormActionsReady) {
      const actions: TalentFormActions = {
        handleNext,
        handlePrevious,
        handleSaveAndExit,
        isSubmitting,
        isSaving,
        currentStep,
        totalSteps
      };
      onFormActionsReady(actions);
    }
  }, [
    currentStep, 
    handleNext, 
    handlePrevious, 
    handleSaveAndExit, 
    isSubmitting, 
    isSaving, 
    onFormActionsReady, 
    totalSteps
  ]);
  
  // Render step content
  const renderStepContent = () => {
    switch (currentStep) {
      case 0:
        return <IdentityStep autoFilledFields={autoFilledFields} />;
      case 1:
        return <SkillsStep autoFilledFields={autoFilledFields} />;
      case 2:
        return <ProjectsStep autoFilledFields={autoFilledFields} />;
      case 3:
        return <SoftSkillsStep autoFilledFields={autoFilledFields} />;
      case 4:
        return <SummaryStep />;
      default:
        return null;
    }
  };
  
  // Step definitions
  const steps = [
    { title: "Identité & Disponibilité", description: "Informations de base et disponibilité" },
    { title: "Compétences", description: "Compétences techniques et fonctionnelles" },
    { title: "Projets", description: "Références de projets et réalisations" },
    { title: "Soft Skills & Préférences", description: "Compétences comportementales et mobilité" },
    { title: "Synthèse & Validation", description: "Récapitulatif et validation finale" },
  ];
  
  return (
    <FormProvider {...methods}>
      <div className="w-full mb-20">
        {/* Title of current step */}
        <div className="mb-4 md:mb-6">
          <h2 className="text-xl md:text-2xl font-semibold mb-1">{steps[currentStep].title}</h2>
          <p className="text-sm text-muted-foreground">{steps[currentStep].description}</p>
        </div>
        
        {/* Main content area with two columns */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Left column - Main form - 2/3 de l'espace sur desktop */}
          <div className="lg:col-span-2 space-y-6">
            <form className="space-y-6 rounded-2xl p-6 shadow-inner bg-white/95 border border-gray-200">
              {renderStepContent()}
            </form>
            
            {/* Indicateur de sauvegarde automatique */}
            {lastSaved && (
              <div className="text-xs md:text-sm text-muted-foreground mt-4 flex items-center gap-2">
                <div
                  className={isSaving ? "animate-pulse bg-blue-500" : "bg-emerald-500"}
                  style={{ width: "8px", height: "8px", borderRadius: "50%" }}
                />
                {isSaving
                  ? "Sauvegarde en cours..."
                  : `Progression sauvegardée automatiquement (${lastSaved.toLocaleTimeString()})`}
              </div>
            )}
          </div>
          
          {/* Right column - HR Qualification Block - 1/3 de l'espace sur desktop */}
          <div className="lg:col-span-1">
            {/* Ne pas afficher dans l'étape de résumé où nous avons déjà la section HR */}
            {currentStep !== 4 && <QualificationSidebar currentStep={currentStep} />}
          </div>
        </div>
        
        {/* Form buttons */}
        {renderButtons && (
          <div className="flex flex-col sm:flex-row sm:justify-between pt-6 md:pt-8 mt-6 md:mt-8 border-t border-gray-200 gap-4 sm:gap-0">
            <div className="flex flex-wrap gap-3 w-full sm:w-auto justify-center sm:justify-start">
              <Button
                type="button"
                variant="outline"
                size="default"
                onClick={currentStep === 0 ? onCancel : handlePrevious}
                className="rounded-xl shadow-sm hover:shadow-md transition-all bg-white border border-gray-200 text-sm"
              >
                {currentStep === 0 ? "Annuler" : "Précédent"}
              </Button>
              
              <Button
                type="button"
                variant="secondary"
                size="default"
                onClick={handleSaveAndExit}
                disabled={isSubmitting || isSaving}
                className="rounded-xl shadow-sm hover:shadow-md transition-all bg-white border border-gray-200 text-sm"
              >
                Sauvegarder et quitter
              </Button>
            </div>
            
            <Button
              type="button"
              size="default"
              onClick={handleNext}
              disabled={isSubmitting || isSaving}
              className="w-full sm:w-auto min-w-[120px] rounded-xl shadow-sm hover:shadow-md transition-all bg-emerald-600 hover:bg-emerald-500 text-white text-sm"
            >
              {(isSubmitting || isSaving) && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
              {currentStep < totalSteps - 1 ? "Suivant" : "Finaliser"}
            </Button>
          </div>
        )}
      </div>
    </FormProvider>
  );
};