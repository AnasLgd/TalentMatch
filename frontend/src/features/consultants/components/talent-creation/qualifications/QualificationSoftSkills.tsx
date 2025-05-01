import React from "react";
import { useFormContext } from "react-hook-form";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";
import { Brain, Target } from "lucide-react";
import { TalentFormValues } from "../schemas/TalentFormSchema";
import { FormControl, FormField, FormItem, FormLabel } from "@/components/ui/form";
import { HrRating } from "../common/HrRating";

export const QualificationSoftSkills: React.FC = () => {
  const { control, watch } = useFormContext<TalentFormValues>();
  const softSkills = watch("soft_skills") || [];

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

      {/* Liste des soft skills */}
      <div className="space-y-4">
        <h3 className="text-sm font-medium flex items-center gap-2">
          <Brain className="h-4 w-4" />
          Évaluation des soft skills
        </h3>

        {softSkills.length === 0 ? (
          <p className="text-sm text-muted-foreground italic">
            Aucun soft skill identifié pour le moment
          </p>
        ) : (
          <ScrollArea className="h-[200px] pr-3">
            <div className="space-y-3">
              {softSkills.map((softSkill, index) => (
                <div key={index} className="flex justify-between items-center p-2 rounded-lg bg-gray-50 border border-gray-100">
                  <div className="text-sm font-medium">{softSkill.name}</div>
                  
                  {/* Rating pour chaque soft skill */}
                  <FormField
                    control={control}
                    name={`soft_skills.${index}.rating`}
                    render={({ field }) => (
                      <FormItem className="mb-0">
                        <FormControl>
                          <HrRating
                            value={field.value || 0}
                            onChange={field.onChange}
                            size="sm"
                          />
                        </FormControl>
                      </FormItem>
                    )}
                  />
                </div>
              ))}
            </div>
          </ScrollArea>
        )}

        <p className="text-xs text-muted-foreground mt-2">
          L'évaluation des soft skills est basée sur l'entretien RH et les références
        </p>
      </div>

      <Separator />
      
      {/* Attentes & Préférences */}
      <FormField
        control={control}
        name="expectations"
        render={({ field }) => (
          <FormItem>
            <FormLabel className="flex items-center gap-2">
              <Target className="h-4 w-4" />
              Attentes & Préférences
            </FormLabel>
            <FormControl>
              <div className="relative">
                <textarea
                  className="w-full min-h-[100px] p-2 border rounded-xl shadow-inner resize-none"
                  placeholder="Ex : Recherche des missions en full remote, secteur fintech, environnement Agile..."
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