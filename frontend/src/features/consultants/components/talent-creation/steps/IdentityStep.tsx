import React, { useState, useEffect } from "react";
import { useFormContext } from "react-hook-form";
import {
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Tooltip } from "@/components/ui/tooltip";
import { HrRating } from "../HrRating";
import { TalentFormValues } from "../TalentMultiStepForm";
import { cn } from "@/lib/utils";
import { InfoIcon } from "lucide-react";

interface IdentityStepProps {
  autoFilledFields: string[];
}

export const IdentityStep: React.FC<IdentityStepProps> = ({
  autoFilledFields
}) => {
  const { control, watch, setValue } = useFormContext<TalentFormValues>();
  const [availabilityType, setAvailabilityType] = useState<"immediate" | "future">("future");
  
  // Surveiller la date de disponibilité
  const availabilityDate = watch("availability_date");
  
  // Initialiser le type de disponibilité en fonction de la date
  useEffect(() => {
    if (availabilityDate) {
      const today = new Date();
      const selectedDate = new Date(availabilityDate);
      
      // Comparer uniquement les dates (ignorer l'heure)
      today.setHours(0, 0, 0, 0);
      selectedDate.setHours(0, 0, 0, 0);
      
      if (selectedDate.getTime() <= today.getTime()) {
        setAvailabilityType("immediate");
      } else {
        setAvailabilityType("future");
      }
    }
  }, [availabilityDate]);
  
  // Gérer le changement de type de disponibilité
  const handleAvailabilityTypeChange = (value: string) => {
    if (value === "immediate") {
      // Définir la date du jour
      const today = new Date();
      const formattedDate = today.toISOString().split('T')[0];
      setValue("availability_date", formattedDate);
      setAvailabilityType("immediate");
    } else {
      setAvailabilityType("future");
      // Conserver la date actuelle ou définir une date dans le futur si c'est aujourd'hui
      if (!availabilityDate || new Date(availabilityDate).toISOString().split('T')[0] === new Date().toISOString().split('T')[0]) {
        const futureDate = new Date();
        futureDate.setDate(futureDate.getDate() + 30); // par défaut: dans 30 jours
        setValue("availability_date", futureDate.toISOString().split('T')[0]);
      }
    }
  };
  
  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {/* Prénom */}
        <FormField
          control={control}
          name="first_name"
          render={({ field }) => (
            <FormItem className={cn(
              autoFilledFields.includes("first_name") && "bg-blue-50 p-2 rounded-md"
            )}>
              <FormLabel>Prénom*</FormLabel>
              <FormControl>
                <Input placeholder="Prénom" {...field} />
              </FormControl>
              <FormMessage />
              {autoFilledFields.includes("first_name") && (
                <p className="text-xs text-blue-500">Pré-rempli depuis le CV</p>
              )}
            </FormItem>
          )}
        />

        {/* Nom */}
        <FormField
          control={control}
          name="last_name"
          render={({ field }) => (
            <FormItem className={cn(
              autoFilledFields.includes("last_name") && "bg-blue-50 p-2 rounded-md"
            )}>
              <FormLabel>Nom*</FormLabel>
              <FormControl>
                <Input placeholder="Nom" {...field} />
              </FormControl>
              <FormMessage />
              {autoFilledFields.includes("last_name") && (
                <p className="text-xs text-blue-500">Pré-rempli depuis le CV</p>
              )}
            </FormItem>
          )}
        />
      </div>

      {/* Rôle / Titre */}
      <FormField
        control={control}
        name="title"
        render={({ field }) => (
          <FormItem className={cn(
            autoFilledFields.includes("title") && "bg-blue-50 p-2 rounded-md"
          )}>
            <FormLabel>Rôle / Titre*</FormLabel>
            <FormControl>
              <Input placeholder="Développeur, DevOps, Chef de projet..." {...field} />
            </FormControl>
            <FormMessage />
            {autoFilledFields.includes("title") && (
              <p className="text-xs text-blue-500">Pré-rempli depuis le CV</p>
            )}
          </FormItem>
        )}
      />

      {/* Années d'expérience */}
      <FormField
        control={control}
        name="experience_years"
        render={({ field }) => (
          <FormItem>
            <FormLabel>Années d'expérience</FormLabel>
            <FormControl>
              <Input
                type="number"
                placeholder="Années d'expérience"
                {...field}
                value={field.value || ""}
                onChange={(e) => field.onChange(e.target.value === "" ? "" : parseInt(e.target.value, 10))}
                min={0}
                max={50}
              />
            </FormControl>
            <FormMessage />
          </FormItem>
        )}
      />

      {/* Disponibilité améliorée */}
      <div>
        <FormLabel>Disponibilité</FormLabel>
        <div className="mt-2 space-y-3">
          <Select
            value={availabilityType}
            onValueChange={handleAvailabilityTypeChange}
          >
            <SelectTrigger>
              <SelectValue placeholder="Type de disponibilité" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="immediate">Immédiate</SelectItem>
              <SelectItem value="future">À partir du</SelectItem>
            </SelectContent>
          </Select>

          {availabilityType === "future" && (
            <FormField
              control={control}
              name="availability_date"
              render={({ field }) => (
                <FormItem>
                  <FormControl>
                    <Input
                      type="date"
                      {...field}
                    />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
          )}
        </div>
      </div>

      {/* Bio */}
      <FormField
        control={control}
        name="bio"
        render={({ field }) => (
          <FormItem>
            <FormLabel>Bio / Description</FormLabel>
            <FormControl>
              <Textarea
                placeholder="Brève description du profil..."
                className="resize-none h-24"
                {...field}
              />
            </FormControl>
            <FormMessage />
          </FormItem>
        )}
      />

      {/* Évaluation du potentiel par RH */}
      <div className="p-4 border rounded-md bg-amber-50">
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
    </div>
  );
};