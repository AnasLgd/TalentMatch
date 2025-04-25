import React, { useState, useEffect, useCallback } from "react";
import { useForm, FormProvider } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import * as z from "zod";
import { useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Loader2 } from "lucide-react";
import { Steps, Step } from "./Steps";
import { IdentityStep } from "@/features/consultants/components/talent-creation/steps/IdentityStep";
import { SkillsStep } from "@/features/consultants/components/talent-creation/steps/SkillsStep";
import { ProjectsStep } from "@/features/consultants/components/talent-creation/steps/ProjectsStep";
import { SoftSkillsStep } from "@/features/consultants/components/talent-creation/steps/SoftSkillsStep";
import { SummaryStep } from "@/features/consultants/components/talent-creation/steps/SummaryStep";
import { CvAnalysisResult } from "@/features/cv-processing/types";
import { AvailabilityStatus, ConsultantCreate, Skill } from "../../types";
import { consultantService } from "../../services/consultant-service";
import { toast } from "@/hooks/use-toast";

// Define the form schema with Zod
const formSchema = z.object({
  // Identity & Availability
  first_name: z.string().min(1, { message: "Le prénom est requis" }),
  last_name: z.string().min(1, { message: "Le nom est requis" }),
  title: z.string().min(1, { message: "Le rôle est requis" }),
  experience_years: z.preprocess(
    (value) => (value === "" ? undefined : Number(value)),
    z.number().min(0).max(50).optional()
  ),
  availability_date: z.string().optional(),
  
  // HR evaluation for identity step
  potential_evaluation: z.number().min(1).max(5).optional(),
  
  // Skills
  skills: z.array(
    z.object({
      name: z.string(),
      level: z.string().optional(),
      years: z.number().optional(),
      category: z.string().optional(),
      hr_rating: z.number().min(1).max(5).optional(), // HR rating for each skill
    })
  ).optional(),
  
  // Projects
  projects: z.array(
    z.object({
      title: z.string(),
      description: z.string().optional(),
      period: z.string().optional(),
      complexity_rating: z.number().min(1).max(5).optional(), // HR rating for complexity
      impact_rating: z.number().min(1).max(5).optional(),     // HR rating for impact
      autonomy_rating: z.number().min(1).max(5).optional(),   // HR rating for autonomy
    })
  ).optional(),
  
  // Soft Skills & Preferences
  soft_skills: z.array(
    z.object({
      name: z.string(),
      rating: z.number().min(1).max(5).optional(),
    })
  ).optional(),
  location: z.string().optional(),
  remote_work: z.boolean().optional(),
  max_travel_distance: z.number().optional(),
  daily_rate: z.number().optional(),
  
  // Bio/Additional notes
  bio: z.string().optional(),
  
  // Final HR Validation
  hr_status: z.enum(["SOURCED", "IN_QUALIFICATION", "QUALIFIED"]).optional(),
  hr_notes: z.string().optional(),
  
  // Hidden fields (not displayed in the form)
  company_id: z.number(),
  user_id: z.literal(null).optional(),
  photo_url: z.string().optional(),
});

export type TalentFormValues = z.infer<typeof formSchema>;

interface TalentMultiStepFormProps {
  cvAnalysisResult?: CvAnalysisResult;
  companyId: number;
  onSuccess?: (consultantId: number) => void;
  onCancel?: () => void;
  onStepChange?: (currentStep: number, totalSteps: number) => void;
}

export const TalentMultiStepForm: React.FC<TalentMultiStepFormProps> = ({
  cvAnalysisResult,
  companyId,
  onSuccess,
  onCancel,
  onStepChange,
}) => {
  const [currentStep, setCurrentStep] = useState(0);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [autoFilledFields, setAutoFilledFields] = useState<string[]>([]);
  const [savedConsultantId, setSavedConsultantId] = useState<number | null>(null);
  const [isSaving, setIsSaving] = useState(false);
  const [lastSaved, setLastSaved] = useState<Date | null>(null);
  
  const navigate = useNavigate();
  
  // Create form methods
  const methods = useForm<TalentFormValues>({
    resolver: zodResolver(formSchema),
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
      hr_status: "SOURCED", // Default initial status
    },
  });
  
  // Pre-fill form with CV analysis result if available
  useEffect(() => {
    if (cvAnalysisResult) {
      const autoFilled: string[] = [];
      
      // Extract name components
      const nameParts = cvAnalysisResult.candidate.name.split(" ");
      if (nameParts.length >= 2) {
        methods.setValue("first_name", nameParts[0]);
        methods.setValue("last_name", nameParts.slice(1).join(" "));
        autoFilled.push("first_name", "last_name");
      }
      
      // Map skills
      if (cvAnalysisResult.candidate.skills.length > 0) {
        const mappedSkills = cvAnalysisResult.candidate.skills.map(skill => ({
          name: skill.name,
          level: skill.level || "",
          years: skill.years,
          category: skill.category || "Technique",
          hr_rating: undefined, // HR will need to rate these
        }));
        
        methods.setValue("skills", mappedSkills);
        autoFilled.push("skills");
      }
      
      // Map projects from experience
      if (cvAnalysisResult.candidate.experience.length > 0) {
        const mappedProjects = cvAnalysisResult.candidate.experience.map(exp => ({
          title: exp.role + " @ " + exp.company,
          description: exp.description || "",
          period: exp.period || "",
          complexity_rating: undefined,
          impact_rating: undefined,
          autonomy_rating: undefined,
        }));
        
        methods.setValue("projects", mappedProjects);
        autoFilled.push("projects");
      }
      
      // Guess title from most recent experience if available
      if (cvAnalysisResult.candidate.experience.length > 0) {
        methods.setValue("title", cvAnalysisResult.candidate.experience[0].role);
        autoFilled.push("title");
      }
      
      setAutoFilledFields(autoFilled);
    }
  }, [cvAnalysisResult, methods]);
  
  // Calculate total steps
  const totalSteps = 5;
  
  // Notify parent component about step changes
  useEffect(() => {
    if (onStepChange) {
      onStepChange(currentStep, totalSteps);
    }
  }, [currentStep, totalSteps, onStepChange]);
  
  // Generate step titles and descriptions
  const steps = [
    { title: "Identité & Disponibilité", description: "Informations de base et disponibilité" },
    { title: "Compétences", description: "Compétences techniques et fonctionnelles" },
    { title: "Projets", description: "Références de projets et réalisations" },
    { title: "Soft Skills & Préférences", description: "Compétences comportementales et mobilité" },
    { title: "Synthèse & Validation", description: "Récapitulatif et validation finale" },
  ];
  
  // Fonction pour sauvegarder le talent avec status SOURCED
  const saveAsDraft = useCallback(async (formData: TalentFormValues) => {
    try {
      setIsSaving(true);
      
      // Préparation des données minimales pour la sauvegarde
      const minimumData: ConsultantCreate = {
        first_name: formData.first_name || "",
        last_name: formData.last_name || "",
        title: formData.title || "Candidat en qualification",
        company_id: formData.company_id,
        user_id: null,
        availability_status: AvailabilityStatus.SOURCED, // Utiliser SOURCED pour les drafts
        skills: formData.skills?.filter(skill => skill.name).map(skill => ({
          name: skill.name,
          category: skill.category,
          level: skill.level,
          years: skill.years
        })),
        availability_date: formData.availability_date,
        bio: formData.bio,
      };

      // Si nous avons déjà un ID de consultant, mettre à jour plutôt que créer
      if (savedConsultantId) {
        await consultantService.updateConsultant(savedConsultantId, minimumData);
      } else {
        const createdConsultant = await consultantService.createConsultant(minimumData);
        setSavedConsultantId(createdConsultant.id);
      }

      setLastSaved(new Date());
      return true;
    } catch (error) {
      console.error("Erreur lors de la sauvegarde du brouillon:", error);
      return false;
    } finally {
      setIsSaving(false);
    }
  }, [savedConsultantId]);

  // Sauvegarde automatique à chaque changement d'étape
  const handleAutoSave = async () => {
    const formData = methods.getValues();
    if (formData.first_name && formData.last_name) {
      await saveAsDraft(formData);
    }
  };

  // Sauvegarder et quitter
  const handleSaveAndExit = async () => {
    const formData = methods.getValues();
    const success = await saveAsDraft(formData);
    
    if (success) {
      toast({
        title: "Brouillon sauvegardé",
        description: "Vous pourrez reprendre la saisie plus tard.",
      });
      if (onCancel) {
        onCancel();
      } else {
        navigate("/consultants");
      }
    }
  };

  // Handle next step
  const handleNext = async () => {
    // Validate current step
    const fieldsToValidate = getFieldsForStep(currentStep);
    const isValid = await methods.trigger(fieldsToValidate);
    
    if (isValid) {
      if (currentStep < totalSteps - 1) {
        // Sauvegarde automatique avant de passer à l'étape suivante
        await handleAutoSave();
        setCurrentStep(prev => prev + 1);
      } else {
        // Submit form if on last step
        methods.handleSubmit(onSubmit)();
      }
    }
  };
  
  // Handle previous step
  const handlePrevious = async () => {
    if (currentStep > 0) {
      // Sauvegarde automatique avant de revenir à l'étape précédente
      await handleAutoSave();
      setCurrentStep(prev => prev - 1);
    }
  };
  
  // Get fields to validate for a specific step
  const getFieldsForStep = (step: number): (keyof TalentFormValues)[] => {
    switch (step) {
      case 0:
        return ["first_name", "last_name", "title"];
      case 1:
        return ["skills"];
      case 2:
        return ["projects"];
      case 3:
        return ["soft_skills", "location", "remote_work", "daily_rate"];
      case 4:
        return ["hr_status"];
      default:
        return [];
    }
  };
  
  // Submit form data
  const onSubmit = async (data: TalentFormValues) => {
    try {
      setIsSubmitting(true);
      
      // Map form data to ConsultantCreate
      const consultantData: ConsultantCreate = {
        first_name: data.first_name,
        last_name: data.last_name,
        title: data.title,
        experience_years: data.experience_years,
        company_id: data.company_id,
        user_id: null, // We're creating a consultant without a user for now
        
        // Map availability status based on HR status
        availability_status: mapHrStatusToAvailabilityStatus(data.hr_status),
        availability_date: data.availability_date,
        
        // Other fields
        bio: data.bio,
        location: data.location,
        remote_work: data.remote_work,
        max_travel_distance: data.max_travel_distance,
        daily_rate: data.daily_rate,
        
        // Map skills (excluding HR ratings)
        skills: data.skills?.filter(skill => skill.name).map(skill => ({
          name: skill.name,
          level: skill.level,
          years: skill.years,
          category: skill.category,
        })),
        
        photo_url: data.photo_url,
      };
      
      let consultantId: number;
      
      // Si nous avons déjà un ID de consultant (brouillon), mettre à jour plutôt que créer
      if (savedConsultantId) {
        const updatedConsultant = await consultantService.updateConsultant(savedConsultantId, consultantData);
        consultantId = updatedConsultant.id;
        
        toast({
          title: "Talent mis à jour avec succès",
          description: `${data.first_name} ${data.last_name} a été qualifié.`,
        });
      } else {
        // Create new consultant
        const createdConsultant = await consultantService.createConsultant(consultantData);
        consultantId = createdConsultant.id;
        
        toast({
          title: "Talent créé avec succès",
          description: `${data.first_name} ${data.last_name} a été ajouté.`,
        });
      }
      
      // Call onSuccess callback or navigate
      if (onSuccess) {
        onSuccess(consultantId);
      } else {
        navigate("/consultants");
      }
    } catch (error) {
      console.error("Erreur lors de la création du talent:", error);
      toast({
        title: "Erreur",
        description: "Une erreur est survenue lors de la création du talent.",
        variant: "destructive",
      });
    } finally {
      setIsSubmitting(false);
    }
  };
  
  // Map HR status to availability status
  const mapHrStatusToAvailabilityStatus = (
    hrStatus?: "SOURCED" | "IN_QUALIFICATION" | "QUALIFIED"
  ): AvailabilityStatus => {
    switch (hrStatus) {
      case "SOURCED":
        return AvailabilityStatus.SOURCED;
      case "IN_QUALIFICATION":
        return AvailabilityStatus.SOURCED; // Phase de qualification = toujours SOURCED
      case "QUALIFIED":
        return AvailabilityStatus.QUALIFIED;
      default:
        return AvailabilityStatus.SOURCED;
    }
  };
  
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
  
  return (
    <FormProvider {...methods}>
      <div className="w-full">
        {/* Title of current step */}
        <div className="mb-8">
          <h2 className="text-2xl font-semibold mb-2">{steps[currentStep].title}</h2>
          <p className="text-muted-foreground">{steps[currentStep].description}</p>
        </div>
        
        <div className="space-y-8">
          <form className="space-y-8 rounded-xl p-6 shadow-inner bg-white/95 border border-gray-200">
            {renderStepContent()}
          </form>
          
          {/* Indicateur de sauvegarde automatique */}
          {lastSaved && (
            <div className="text-sm text-muted-foreground mt-6 flex items-center gap-2">
              <div className={isSaving
                ? "animate-pulse bg-blue-500"
                : "bg-emerald-500"
              }
                   style={{ width: "10px", height: "10px", borderRadius: "50%" }} />
              {isSaving
                ? "Sauvegarde en cours..."
                : `Progression sauvegardée automatiquement (${lastSaved.toLocaleTimeString()})`}
            </div>
          )}
        </div>
        
        <div className="flex justify-between pt-8 mt-8 border-t border-gray-200">
          <div className="flex gap-3">
            <Button
              type="button"
              variant="outline"
              size="lg"
              onClick={currentStep === 0 ? onCancel : handlePrevious}
              className="rounded-xl shadow-sm hover:shadow-md transition-all bg-white border border-gray-200"
            >
              {currentStep === 0 ? "Annuler" : "Précédent"}
            </Button>
            
            <Button
              type="button"
              variant="secondary"
              size="lg"
              onClick={handleSaveAndExit}
              disabled={isSubmitting || isSaving}
              className="rounded-xl shadow-sm hover:shadow-md transition-all bg-white border border-gray-200"
            >
              Sauvegarder et quitter
            </Button>
          </div>
          
          <Button
            type="button"
            size="lg"
            onClick={handleNext}
            disabled={isSubmitting || isSaving}
            className="min-w-[120px] rounded-xl shadow-sm hover:shadow-md transition-all bg-emerald-600 hover:bg-emerald-700 text-white"
          >
            {(isSubmitting || isSaving) && <Loader2 className="mr-2 h-5 w-5 animate-spin" />}
            {currentStep < totalSteps - 1 ? "Suivant" : "Finaliser"}
          </Button>
        </div>
      </div>
    </FormProvider>
  );
};