import { TalentFormValues } from "./TalentFormSchema";
import { CvAnalysisResult } from "@/features/cv-processing/types";
import { AvailabilityStatus, ConsultantCreate } from "../../types";
import { consultantService } from "../../services/consultant-service";
import { toast } from "@/hooks/use-toast";

// Map HR status to availability status
export const mapHrStatusToAvailabilityStatus = (
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

// Prepare consultant data from form values
export const prepareConsultantData = (data: TalentFormValues): ConsultantCreate => {
  return {
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
};

// Prepare minimum data for draft saving
export const prepareMinimumData = (formData: TalentFormValues): ConsultantCreate => {
  return {
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
};

// Save or update consultant data
export const saveOrUpdateConsultant = async (
  data: ConsultantCreate, 
  savedId: number | null
): Promise<{ success: boolean; id?: number }> => {
  try {
    if (savedId) {
      await consultantService.updateConsultant(savedId, data);
      return { success: true, id: savedId };
    } else {
      const createdConsultant = await consultantService.createConsultant(data);
      return { success: true, id: createdConsultant.id };
    }
  } catch (error) {
    console.error("Error saving consultant data:", error);
    toast({
      title: "Erreur",
      description: "Une erreur est survenue lors de la sauvegarde.",
      variant: "destructive",
    });
    return { success: false };
  }
};

// Process CV analysis result to prefill form data
export const processCvAnalysisResult = (
  cvAnalysisResult: CvAnalysisResult | undefined,
  setValue: <T extends keyof TalentFormValues>(field: T, value: TalentFormValues[T]) => void
): string[] => {
  const autoFilled: string[] = [];
  
  // Extract name components
  if (cvAnalysisResult?.candidate?.name) {
    const nameParts = cvAnalysisResult.candidate.name.split(" ");
    if (nameParts.length >= 2) {
      setValue("first_name", nameParts[0]);
      setValue("last_name", nameParts.slice(1).join(" "));
      autoFilled.push("first_name", "last_name");
    }
  }
  
  // Map skills
  if (cvAnalysisResult?.candidate?.skills?.length > 0) {
    const mappedSkills = cvAnalysisResult.candidate.skills.map((skill) => ({
      name: skill.name,
      level: skill.level || "",
      years: skill.years,
      category: skill.category || "Technique",
      hr_rating: undefined, // HR will need to rate these
    }));
    
    setValue("skills", mappedSkills);
    autoFilled.push("skills");
  }
  
  // Map projects from experience
  if (cvAnalysisResult?.candidate?.experience?.length > 0) {
    const mappedProjects = cvAnalysisResult.candidate.experience.map((exp) => ({
      title: exp.role + " @ " + exp.company,
      description: exp.description || "",
      period: exp.period || "",
      complexity_rating: undefined,
      impact_rating: undefined,
      autonomy_rating: undefined,
    }));
    
    setValue("projects", mappedProjects);
    autoFilled.push("projects");
    
    // Guess title from most recent experience if available
    setValue("title", cvAnalysisResult.candidate.experience[0].role);
    autoFilled.push("title");
  }
  
  return autoFilled;
};