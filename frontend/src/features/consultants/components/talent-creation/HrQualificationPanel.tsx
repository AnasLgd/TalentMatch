import React from "react";
import { useFormContext } from "react-hook-form";
import { InfoIcon } from "lucide-react";
import { HrRating } from "./HrRating";
import { TalentFormValues } from "./TalentMultiStepForm";
import {
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";

export const HrQualificationPanel: React.FC = () => {
  const { control, setValue, watch } = useFormContext<TalentFormValues>();
  const potentialEvaluation = watch("potential_evaluation");

  return (
    <div className="space-y-6">
      <div className="p-4 border rounded-xl bg-amber-50 shadow-sm">
        <h3 className="text-lg font-medium mb-2 flex items-center gap-2">
          Qualification RH
          <InfoIcon className="h-4 w-4 text-muted-foreground cursor-help" />
        </h3>
        <FormField
          control={control}
          name="potential_evaluation"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Potentiel global</FormLabel>
              <FormControl>
                <HrRating
                  value={field.value || 0}
                  onChange={(value) => setValue("potential_evaluation", value)}
                />
              </FormControl>
              <FormMessage />
              <p className="text-xs text-muted-foreground mt-1">
                Évaluez le potentiel global du candidat sur une échelle de 1 à 5 étoiles.
                Cette évaluation est à usage interne uniquement.
              </p>
            </FormItem>
          )}
        />
      </div>
      
      <div className="p-4 border border-dashed rounded-xl bg-white/50">
        <h3 className="text-base font-medium mb-2 text-muted-foreground">Zones d'opportunités</h3>
        <p className="text-sm text-muted-foreground">
          Cette section sera enrichie pour permettre une qualification plus détaillée du profil consultant.
        </p>
      </div>
    </div>
  );
};