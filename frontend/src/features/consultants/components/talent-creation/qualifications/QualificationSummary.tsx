import React from "react";
import { useFormContext } from "react-hook-form";
import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";
import { 
  User, Briefcase, Star, Award, Calendar, 
  MapPin, Timer, Banknote, Laptop 
} from "lucide-react";
import { TalentFormValues } from "../schemas/TalentFormSchema";
import { Card } from "@/components/ui/card";
import { HrRating } from "../common/HrRating";

/**
 * Composant en lecture seule qui affiche un récapitulatif de toutes les qualifications RH du talent
 * Utilisé dans l'étape de synthèse pour avoir une vue d'ensemble avant validation finale
 */
export const QualificationSummary: React.FC = () => {
  const { watch } = useFormContext<TalentFormValues>();
  
  // Récupération des données du formulaire
  const {
    first_name,
    last_name,
    title,
    experience_years,
    availability_date,
    location,
    remote_work,
    skills = [],
    projects = [],
    soft_skills = [],
    daily_rate,
    potential_evaluation,
    candidate_status,
    expectations,
    salary_expectations,
    salary_details,
    hr_notes,
    hr_status
  } = watch();

  return (
    <div className="space-y-6">
      {/* Header avec évaluation globale */}
      <div className="text-center pb-4 border-b">
        <Badge 
          variant={hr_status === "QUALIFIED" ? "default" : "outline"}
          className="mb-2"
        >
          {hr_status === "QUALIFIED" ? "Talent qualifié" : hr_status === "IN_QUALIFICATION" ? "En qualification" : "Profil sourcé"}
        </Badge>
        
        <div className="flex justify-center items-center py-2">
          <div className="flex">
            <HrRating value={potential_evaluation || 0} readOnly size="md" />
          </div>
        </div>
        
        <p className="text-xs text-muted-foreground">
          Évaluation globale du potentiel
        </p>
      </div>

      {/* Identité */}
      <div className="space-y-2">
        <h3 className="text-sm font-medium flex items-center gap-2">
          <User className="h-4 w-4" />
          Identité
        </h3>
        
        <Card className="p-3 bg-gray-50">
          <p className="font-medium">{first_name} {last_name}</p>
          <p className="text-sm">{title}</p>
          {experience_years && <p className="text-xs text-muted-foreground">{experience_years} ans d'expérience</p>}
        </Card>
      </div>

      {/* Disponibilité */}
      <div className="space-y-2">
        <h3 className="text-sm font-medium flex items-center gap-2">
          <Calendar className="h-4 w-4" />
          Disponibilité
        </h3>
        
        <Card className="p-3 bg-gray-50">
          <p className="text-sm">{availability_date || "Non spécifiée"}</p>
          <p className="text-xs text-muted-foreground mt-1">{candidate_status || "Statut non renseigné"}</p>
        </Card>
      </div>
      
      {/* Localisation */}
      <div className="space-y-2">
        <h3 className="text-sm font-medium flex items-center gap-2">
          <MapPin className="h-4 w-4" />
          Localisation
        </h3>
        
        <Card className="p-3 bg-gray-50">
          <p className="text-sm">{location || "Non spécifiée"}</p>
          {remote_work && (
            <Badge variant="outline" className="mt-1">
              <Laptop className="h-3 w-3 mr-1" /> Télétravail
            </Badge>
          )}
        </Card>
      </div>

      {/* Tarif */}
      <div className="space-y-2">
        <h3 className="text-sm font-medium flex items-center gap-2">
          <Banknote className="h-4 w-4" />
          Tarification
        </h3>
        
        <Card className="p-3 bg-gray-50">
          {daily_rate ? (
            <p className="text-sm">TJM: {daily_rate}€ / jour</p>
          ) : (
            <p className="text-sm">TJM non renseigné</p>
          )}
          {salary_expectations && (
            <p className="text-sm mt-1">Prétentions: {salary_expectations}</p>
          )}
          {salary_details && (
            <p className="text-xs text-muted-foreground mt-1">{salary_details}</p>
          )}
        </Card>
      </div>

      {/* Compétences */}
      {skills.length > 0 && (
        <div className="space-y-2">
          <h3 className="text-sm font-medium flex items-center gap-2">
            <Star className="h-4 w-4" />
            Compétences évaluées
          </h3>
          
          <Card className="p-3 bg-gray-50">
            <div className="grid grid-cols-2 gap-2">
              {skills.slice(0, 6).map((skill, index) => (
                <div key={index} className="flex justify-between items-center">
                  <p className="text-sm truncate">{skill.name}</p>
                  <div className="flex">
                    <HrRating value={skill.hr_rating || 0} readOnly size="sm" />
                  </div>
                </div>
              ))}
            </div>
            {skills.length > 6 && (
              <p className="text-xs text-muted-foreground mt-2 text-center">
                + {skills.length - 6} autres compétences évaluées
              </p>
            )}
          </Card>
        </div>
      )}

      {/* Projets */}
      {projects.length > 0 && (
        <div className="space-y-2">
          <h3 className="text-sm font-medium flex items-center gap-2">
            <Briefcase className="h-4 w-4" />
            Projets référencés
          </h3>
          
          <Card className="p-3 bg-gray-50">
            <p className="text-sm font-medium">{projects.length} projet(s) qualifié(s)</p>
            <div className="mt-2 space-y-1">
              {projects.slice(0, 3).map((project, index) => (
                <div key={index} className="text-xs">
                  • {project.title}
                </div>
              ))}
            </div>
            {projects.length > 3 && (
              <p className="text-xs text-muted-foreground mt-2">
                + {projects.length - 3} autres projets
              </p>
            )}
          </Card>
        </div>
      )}

      {/* Soft Skills */}
      {soft_skills.length > 0 && (
        <div className="space-y-2">
          <h3 className="text-sm font-medium flex items-center gap-2">
            <Award className="h-4 w-4" />
            Soft Skills
          </h3>
          
          <Card className="p-3 bg-gray-50">
            <div className="flex flex-wrap gap-1">
              {soft_skills.slice(0, 10).map((skill, index) => (
                <Badge key={index} variant="outline">
                  {skill.name}
                </Badge>
              ))}
              {soft_skills.length > 10 && (
                <Badge variant="outline">+{soft_skills.length - 10}</Badge>
              )}
            </div>
          </Card>
        </div>
      )}

      {/* Notes RH */}
      {hr_notes && (
        <div className="space-y-2">
          <Separator />
          <h3 className="text-sm font-medium">Notes internes RH</h3>
          <Card className="p-3 bg-gray-50">
            <p className="text-xs italic whitespace-pre-line">{hr_notes}</p>
          </Card>
        </div>
      )}

      {/* Attentes */}
      {expectations && (
        <div className="space-y-2">
          <h3 className="text-sm font-medium">Attentes & préférences</h3>
          <Card className="p-3 bg-gray-50">
            <p className="text-xs whitespace-pre-line">{expectations}</p>
          </Card>
        </div>
      )}
    </div>
  );
};