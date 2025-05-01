import React from "react";
import { useFormContext } from "react-hook-form";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";
import { BriefcaseBusiness } from "lucide-react";
import { TalentFormValues } from "../schemas/TalentFormSchema";
import { FormControl, FormField, FormItem, FormLabel } from "@/components/ui/form";
import { HrRating } from "../common/HrRating";

export const QualificationProjects: React.FC = () => {
  const { control, watch } = useFormContext<TalentFormValues>();
  const projects = watch("projects") || [];

  return (
    <div className="space-y-6">
      {/* Évaluation globale */}
      <FormField
        control={control}
        name="potential_evaluation"
        render={({ field, fieldState }) => (
          <FormItem>
            <FormLabel className="flex items-center justify-between">
              <span>Évaluation globale du potentiel</span>
              <Badge variant="outline" className="font-normal">
                {field.value || 0}/5
              </Badge>
            </FormLabel>
            <FormControl>
              <HrRating
                value={field.value || 3}
                onChange={(value) => field.onChange(value)}
              />
            </FormControl>
            <p className="text-xs text-muted-foreground mt-1">
              Cette note représente l'évaluation RH globale du candidat
            </p>
          </FormItem>
        )}
      />

      <Separator />

      {/* Liste des projets */}
      <div className="space-y-4">
        <h3 className="text-sm font-medium flex items-center gap-2">
          <BriefcaseBusiness className="h-4 w-4" />
          Qualification RH des projets
        </h3>

        {projects.length === 0 ? (
          <p className="text-sm text-muted-foreground italic">
            Aucun projet référencé pour le moment
          </p>
        ) : (
          <ScrollArea className="h-[300px] pr-3">
            <div className="space-y-4">
              {projects.map((project, index) => (
                <div key={index} className="rounded-lg border border-gray-100 overflow-hidden">
                  <div className="bg-gray-50 p-3">
                    <h4 className="text-sm font-medium">{project.title}</h4>
                    <p className="text-xs text-muted-foreground mt-1 line-clamp-2">
                      {project.description || "Description non spécifiée"}
                    </p>
                    <Badge variant="outline" className="mt-2 text-xs">
                      {project.period || "Période non spécifiée"}
                    </Badge>
                  </div>
                  
                  <div className="p-3 bg-white space-y-3">
                    {/* Complexité */}
                    <FormField
                      control={control}
                      name={`projects.${index}.complexity_rating`}
                      render={({ field }) => (
                        <FormItem className="space-y-1">
                          <div className="flex justify-between items-center">
                            <FormLabel className="text-xs text-muted-foreground m-0">Complexité</FormLabel>
                            <FormControl>
                              <HrRating
                                value={field.value || 0}
                                onChange={field.onChange}
                                size="sm"
                              />
                            </FormControl>
                          </div>
                        </FormItem>
                      )}
                    />
                    
                    {/* Impact */}
                    <FormField
                      control={control}
                      name={`projects.${index}.impact_rating`}
                      render={({ field }) => (
                        <FormItem className="space-y-1">
                          <div className="flex justify-between items-center">
                            <FormLabel className="text-xs text-muted-foreground m-0">Impact</FormLabel>
                            <FormControl>
                              <HrRating
                                value={field.value || 0}
                                onChange={field.onChange}
                                size="sm"
                              />
                            </FormControl>
                          </div>
                        </FormItem>
                      )}
                    />
                    
                    {/* Autonomie */}
                    <FormField
                      control={control}
                      name={`projects.${index}.autonomy_rating`}
                      render={({ field }) => (
                        <FormItem className="space-y-1">
                          <div className="flex justify-between items-center">
                            <FormLabel className="text-xs text-muted-foreground m-0">Autonomie</FormLabel>
                            <FormControl>
                              <HrRating
                                value={field.value || 0}
                                onChange={field.onChange}
                                size="sm"
                              />
                            </FormControl>
                          </div>
                        </FormItem>
                      )}
                    />
                  </div>
                </div>
              ))}
            </div>
          </ScrollArea>
        )}

        <p className="text-xs text-muted-foreground mt-2">
          Ces évaluations permettent de valoriser l'expérience du talent auprès des clients
        </p>
      </div>

      <Separator />
      
      {/* Prétentions salariales */}
      <FormField
        control={control}
        name="salary_expectations"
        render={({ field }) => (
          <FormItem>
            <FormLabel>Prétentions salariales</FormLabel>
            <FormControl>
              <input
                className="w-full p-2 border rounded-xl shadow-inner"
                placeholder="Ex : 45K€ brut annuel"
                {...field}
              />
            </FormControl>
          </FormItem>
        )}
      />
      
      <FormField
        control={control}
        name="salary_details"
        render={({ field }) => (
          <FormItem>
            <FormControl>
              <div className="relative">
                <textarea
                  className="w-full min-h-[80px] p-2 border rounded-xl shadow-inner resize-none"
                  placeholder="Détails du package, variables, avantages en nature..."
                  {...field}
                />
              </div>
            </FormControl>
          </FormItem>
        )}
      />
      
      {/* Notes RH */}
      <FormField
        control={control}
        name="hr_notes"
        render={({ field }) => (
          <FormItem>
            <FormLabel>Notes RH (usage interne)</FormLabel>
            <FormControl>
              <div className="relative">
                <textarea
                  className="w-full min-h-[100px] p-2 border rounded-xl shadow-inner resize-none"
                  placeholder="Observations, points forts, axes d'amélioration..."
                  {...field}
                />
              </div>
            </FormControl>
          </FormItem>
        )}
      />
    </div>
  );
};