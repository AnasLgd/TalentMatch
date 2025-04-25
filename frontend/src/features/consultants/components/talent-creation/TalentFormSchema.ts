import * as z from "zod";

// Define the form schema with Zod
export const formSchema = z.object({
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

// Interface for form actions that can be called by parent components
export interface TalentFormActions {
  handleNext: () => Promise<void>;
  handlePrevious: () => Promise<void>;
  handleSaveAndExit: () => Promise<void>;
  isSubmitting: boolean;
  isSaving: boolean;
  currentStep: number;
  totalSteps: number;
}

// Get fields to validate for a specific step
export const getFieldsForStep = (step: number): (keyof TalentFormValues)[] => {
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

// Define step structure
export const formSteps = [
  { title: "Identité & Disponibilité", description: "Informations de base et disponibilité" },
  { title: "Compétences", description: "Compétences techniques et fonctionnelles" },
  { title: "Projets", description: "Références de projets et réalisations" },
  { title: "Soft Skills & Préférences", description: "Compétences comportementales et mobilité" },
  { title: "Synthèse & Validation", description: "Récapitulatif et validation finale" },
];