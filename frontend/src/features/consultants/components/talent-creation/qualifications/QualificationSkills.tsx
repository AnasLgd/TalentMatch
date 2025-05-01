import React from "react";
import { useFormContext } from "react-hook-form";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";
import { Star } from "lucide-react";
import { TalentFormValues } from "../schemas/TalentFormSchema";
import { cn } from "@/lib/utils";
import { HrRating } from "../common/HrRating";
import { FormControl, FormField, FormItem, FormLabel } from "@/components/ui/form";

export const QualificationSkills: React.FC = () => {
  const { control, watch } = useFormContext<TalentFormValues>();
  const skills = watch("skills") || [];

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

      {/* Liste des compétences */}
      <div className="space-y-4">
        <h3 className="text-sm font-medium flex items-center gap-2">
          <Star className="h-4 w-4" />
          Évaluation RH des compétences
        </h3>

        {skills.length === 0 ? (
          <p className="text-sm text-muted-foreground italic">
            Aucune compétence ajoutée pour le moment
          </p>
        ) : (
          <ScrollArea className="h-[300px] pr-3">
            <div className="space-y-3">
              {skills.map((skill, index) => (
                <div key={index} className="space-y-2">
                  <div className="flex items-center justify-between p-2 rounded-lg bg-gray-50 border border-gray-100">
                    <div className="text-sm font-medium">{skill.name}</div>
                    
                    {/* HR Rating de la compétence */}
                    <FormField
                      control={control}
                      name={`skills.${index}.hr_rating`}
                      render={({ field }) => (
                        <FormItem className="mb-0">
                          <FormControl>
                            <div className="flex">
                              {[1, 2, 3, 4, 5].map((star) => (
                                <Star
                                  key={star}
                                  className={cn(
                                    "h-4 w-4 cursor-pointer transition-colors",
                                    star <= (field.value || 0) ? "text-amber-400 fill-amber-400" : "text-gray-200"
                                  )}
                                  onClick={() => field.onChange(star)}
                                />
                              ))}
                            </div>
                          </FormControl>
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
          La notation reflète le niveau de maîtrise évalué lors de l'entretien RH
        </p>
      </div>

      <Separator />
      
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
      
      {/* Actualité du candidat */}
      <FormField
        control={control}
        name="candidate_status"
        render={({ field }) => (
          <FormItem>
            <FormLabel>Actualité du candidat</FormLabel>
            <FormControl>
              <div className="relative">
                <textarea
                  className="w-full min-h-[80px] p-2 border rounded-xl shadow-inner resize-none"
                  placeholder="Status actuel du candidat..."
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