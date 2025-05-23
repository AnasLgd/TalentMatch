import React from "react";
import { useFormContext } from "react-hook-form";
import {
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { Textarea } from "@/components/ui/textarea";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group";
import { Label } from "@/components/ui/label";
import { TalentFormValues } from "../../schemas/TalentFormSchema";
import { HrRating } from "../../common/HrRating";
import { User, Star, FileText, Sparkles } from "lucide-react";

// Types spécifiques pour améliorer la sécurité de type
interface RatedItem {
  [key: string]: string | number | boolean | undefined;
}

interface SkillWithRating extends RatedItem {
  name: string;
  hr_rating?: number;
}

interface ProjectWithRating extends RatedItem {
  title: string;
  complexity_rating?: number;
  impact_rating?: number;
  autonomy_rating?: number;
}

interface SoftSkillWithRating extends RatedItem {
  name: string;
  rating?: number;
}

// Utilitaire pour calculer la moyenne des notes
const calculateAverageRating = <T extends RatedItem>(
  items: T[],
  ratingField: string | ((item: T) => number)
): number => {
  if (!items || items.length === 0) return 0;
  
  const getItemRating = typeof ratingField === 'function'
    ? ratingField
    : (item: T) => item[ratingField] || 0;
    
  const sum = items.reduce((acc, item) => acc + getItemRating(item), 0);
  return sum / items.length;
};

// Utilitaire pour calculer la moyenne des notes de projet
const calculateProjectRating = (project: ProjectWithRating): number => {
  const ratings = [
    project.complexity_rating || 0,
    project.impact_rating || 0,
    project.autonomy_rating || 0
  ];
  return ratings.reduce((a, b) => a + b, 0) / ratings.length;
};

export const SummaryStep: React.FC = () => {
  const { control, watch } = useFormContext<TalentFormValues>();
  
  // Get form values
  const formValues = watch();
  
  const {
    first_name,
    last_name,
    title,
    experience_years,
    skills = [],
    projects = [],
    soft_skills = [],
    potential_evaluation,
  } = formValues;
  
  // Calculate average ratings using utility functions
  const skillsRating = calculateAverageRating(skills, 'hr_rating');
  const projectsRating = calculateAverageRating(projects, calculateProjectRating);
  const softSkillsRating = calculateAverageRating(soft_skills, 'rating');
  
  return (
    <div className="space-y-6">
      <h3 className="text-lg font-medium">Récapitulatif du profil</h3>
      
      {/* Summary cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {/* Identity card */}
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-base flex items-center">
              <User className="h-4 w-4 mr-2" /> Identité
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-2">
              <div>
                <h4 className="font-medium text-lg">{first_name} {last_name}</h4>
                <p className="text-muted-foreground">{title}</p>
              </div>
              
              {experience_years && (
                <p className="text-sm">
                  {experience_years} {experience_years > 1 ? "années" : "année"} d'expérience
                </p>
              )}
              
              {potential_evaluation && (
                <div className="flex items-center mt-4">
                  <span className="text-sm mr-2">Potentiel global:</span>
                  <HrRating value={potential_evaluation} readOnly={true} size="sm" />
                </div>
              )}
            </div>
          </CardContent>
        </Card>
        
        {/* Skills card */}
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-base flex items-center">
              <Star className="h-4 w-4 mr-2" /> Compétences ({skills.length})
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-2">
              <div className="flex flex-wrap gap-2">
                {skills.slice(0, 6).map((skill, index) => (
                  <Badge key={index} variant="outline">
                    {skill.name}
                  </Badge>
                ))}
                {skills.length > 6 && (
                  <Badge variant="outline">+{skills.length - 6}</Badge>
                )}
              </div>
              
              {skillsRating > 0 && (
                <div className="flex items-center mt-4">
                  <span className="text-sm mr-2">Évaluation moyenne:</span>
                  <HrRating value={Math.round(skillsRating)} readOnly={true} size="sm" />
                </div>
              )}
            </div>
          </CardContent>
        </Card>
        
        {/* Projects card */}
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-base flex items-center">
              <FileText className="h-4 w-4 mr-2" /> Projets ({projects.length})
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-2">
              {projects.length > 0 ? (
                <div>
                  <ul className="text-sm list-disc list-inside">
                    {projects.slice(0, 3).map((project, index) => (
                      <li key={index}>{project.title}</li>
                    ))}
                  </ul>
                  
                  {projects.length > 3 && (
                    <p className="text-xs text-muted-foreground mt-1">
                      +{projects.length - 3} autres projets
                    </p>
                  )}
                </div>
              ) : (
                <p className="text-sm text-muted-foreground">Aucun projet renseigné</p>
              )}
              
              {projectsRating > 0 && (
                <div className="flex items-center mt-4">
                  <span className="text-sm mr-2">Évaluation moyenne:</span>
                  <HrRating value={Math.round(projectsRating)} readOnly={true} size="sm" />
                </div>
              )}
            </div>
          </CardContent>
        </Card>
        
        {/* Soft Skills card */}
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-base flex items-center">
              <Sparkles className="h-4 w-4 mr-2" /> Soft Skills ({soft_skills.length})
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-2">
              <div className="flex flex-wrap gap-2">
                {soft_skills.slice(0, 6).map((skill, index) => (
                  <Badge key={index} variant="secondary">
                    {skill.name}
                  </Badge>
                ))}
                {soft_skills.length > 6 && (
                  <Badge variant="secondary">+{soft_skills.length - 6}</Badge>
                )}
              </div>
              
              {softSkillsRating > 0 && (
                <div className="flex items-center mt-4">
                  <span className="text-sm mr-2">Évaluation moyenne:</span>
                  <HrRating value={Math.round(softSkillsRating)} readOnly={true} size="sm" />
                </div>
              )}
            </div>
          </CardContent>
        </Card>
      </div>
      
      {/* HR Qualification Section */}
      <div className="mt-8 pt-6 border-t">
        <h3 className="text-lg font-medium mb-4">Qualification RH finale</h3>
        
        {/* Status */}
        <FormField
          control={control}
          name="hr_status"
          render={({ field }) => (
            <FormItem className="mb-6">
              <FormLabel>Statut du talent</FormLabel>
              <FormControl>
                <RadioGroup
                  value={field.value}
                  onValueChange={field.onChange}
                  className="flex flex-col space-y-1"
                >
                  <div className="flex items-center space-x-2">
                    <RadioGroupItem value="SOURCED" id="status-sourced" />
                    <Label htmlFor="status-sourced" className="font-normal">
                      Sourcé - Nouvellement ajouté à la base
                    </Label>
                  </div>
                  <div className="flex items-center space-x-2">
                    <RadioGroupItem value="IN_QUALIFICATION" id="status-in-qualification" />
                    <Label htmlFor="status-in-qualification" className="font-normal">
                      En qualification - En cours d'évaluation RH
                    </Label>
                  </div>
                  <div className="flex items-center space-x-2">
                    <RadioGroupItem value="QUALIFIED" id="status-qualified" />
                    <Label htmlFor="status-qualified" className="font-normal">
                      Qualifié - Prêt pour le vivier de talents
                    </Label>
                  </div>
                </RadioGroup>
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
        
        {/* HR Notes */}
        <FormField
          control={control}
          name="hr_notes"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Notes RH (usage interne uniquement)</FormLabel>
              <FormControl>
                <Textarea
                  placeholder="Ajoutez des notes sur ce profil (entretien, observations, etc.)..."
                  className="h-24"
                  {...field}
                />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
      </div>
    </div>
  );
};