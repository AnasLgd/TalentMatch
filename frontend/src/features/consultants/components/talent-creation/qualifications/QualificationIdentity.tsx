import React, { useState, useEffect } from "react";
import { useFormContext } from "react-hook-form";
import { FormControl, FormField, FormItem, FormLabel, FormMessage } from "@/components/ui/form";
import { Textarea } from "@/components/ui/textarea";
import { Input } from "@/components/ui/input";
import { HrRating } from "../common/HrRating";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";
import { UserRound, Target, Banknote } from "lucide-react";
import { TalentFormValues } from "../schemas/TalentFormSchema";
import { cn } from "@/lib/utils";

// Limite de caractères pour les notes RH
const MAX_NOTES_CHARS = 1000;

// Composant pour afficher un compteur de caractères
const CharCounter = ({ count, max, className }: { count: number; max: number; className?: string }) => {
  const isApproachingLimit = count > max * 0.8;
  const isOverLimit = count > max;
  
  return (
    <div
      className={cn(
        "text-xs mt-1 text-right",
        isApproachingLimit ? "text-amber-500" : "text-muted-foreground",
        isOverLimit && "text-red-500",
        className
      )}
    >
      {count}/{max}
    </div>
  );
};

export const QualificationIdentity: React.FC = () => {
  const { control, watch } = useFormContext<TalentFormValues>();
  
  // Observer les valeurs des champs texte pour mettre à jour les compteurs
  const hrNotes = watch("hr_notes") || "";
  const candidateStatus = watch("candidate_status") || "";
  const expectations = watch("expectations") || "";
  const salaryDetails = watch("salary_details") || "";
  
  // Compteurs de caractères
  const [charCounts, setCharCounts] = useState({
    hrNotes: 0,
    candidateStatus: 0,
    expectations: 0,
    salaryDetails: 0,
  });
  
  useEffect(() => {
    setCharCounts({
      hrNotes: hrNotes.length,
      candidateStatus: candidateStatus.length,
      expectations: expectations.length,
      salaryDetails: salaryDetails.length,
    });
  }, [hrNotes, candidateStatus, expectations, salaryDetails]);
  
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
            {fieldState.error && <FormMessage>{fieldState.error.message}</FormMessage>}
            <p className="text-xs text-muted-foreground mt-1">
              Cette note représente l'évaluation RH globale du candidat
            </p>
          </FormItem>
        )}
      />
      
      <Separator />
      
      {/* Actualité du Candidat */}
      <FormField
        control={control}
        name="candidate_status"
        render={({ field, fieldState }) => (
          <FormItem>
            <FormLabel className="flex items-center gap-2">
              <UserRound className="h-4 w-4" />
              Actualité du Candidat
            </FormLabel>
            <FormControl>
              <div className="relative">
                <Textarea
                  placeholder="Ex : En recherche active, en veille, en cours de process chez d'autres clients..."
                  className="h-20 resize-none rounded-xl shadow-inner"
                  {...field}
                />
                <CharCounter count={charCounts.candidateStatus} max={500} />
              </div>
            </FormControl>
            {fieldState.error && <FormMessage>{fieldState.error.message}</FormMessage>}
          </FormItem>
        )}
      />
      
      {/* Attentes & Préférences */}
      <FormField
        control={control}
        name="expectations"
        render={({ field, fieldState }) => (
          <FormItem>
            <FormLabel className="flex items-center gap-2">
              <Target className="h-4 w-4" />
              Attentes & Préférences
            </FormLabel>
            <FormControl>
              <div className="relative">
                <Textarea
                  placeholder="Ex : Recherche des missions en full remote, secteur fintech, environnement Agile..."
                  className="h-20 resize-none rounded-xl shadow-inner"
                  {...field}
                />
                <CharCounter count={charCounts.expectations} max={500} />
              </div>
            </FormControl>
            {fieldState.error && <FormMessage>{fieldState.error.message}</FormMessage>}
          </FormItem>
        )}
      />
      
      {/* Prétentions Salariales */}
      <FormField
        control={control}
        name="salary_expectations"
        render={({ field, fieldState }) => (
          <FormItem>
            <FormLabel className="flex items-center gap-2">
              <Banknote className="h-4 w-4" />
              Prétentions Salariales
            </FormLabel>
            <FormControl>
              <Input
                placeholder="Ex : 45K€ brut annuel"
                className="rounded-xl shadow-sm"
                {...field}
              />
            </FormControl>
            {fieldState.error && <FormMessage>{fieldState.error.message}</FormMessage>}
          </FormItem>
        )}
      />
      
      <FormField
        control={control}
        name="salary_details"
        render={({ field, fieldState }) => (
          <FormItem className="mt-2">
            <FormControl>
              <div className="relative">
                <Textarea
                  placeholder="Détails du package, variables, avantages en nature..."
                  className="h-16 resize-none rounded-xl shadow-inner"
                  {...field}
                />
                <CharCounter count={charCounts.salaryDetails} max={300} />
              </div>
            </FormControl>
            {fieldState.error && <FormMessage>{fieldState.error.message}</FormMessage>}
          </FormItem>
        )}
      />
      
      <Separator />
      
      {/* Notes RH */}
      <FormField
        control={control}
        name="hr_notes"
        render={({ field, fieldState }) => (
          <FormItem>
            <FormLabel>Notes RH (usage interne)</FormLabel>
            <FormControl>
              <div className="relative">
                <Textarea
                  placeholder="Observations, points forts, axes d'amélioration..."
                  className="h-32 resize-none rounded-xl shadow-inner"
                  maxLength={MAX_NOTES_CHARS}
                  {...field}
                />
                <CharCounter count={charCounts.hrNotes} max={MAX_NOTES_CHARS} />
              </div>
            </FormControl>
            {fieldState.error && <FormMessage>{fieldState.error.message}</FormMessage>}
          </FormItem>
        )}
      />
    </div>
  );
};