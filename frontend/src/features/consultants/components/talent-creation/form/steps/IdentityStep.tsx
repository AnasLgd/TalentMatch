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
import { Switch } from "@/components/ui/switch";
import { TalentFormValues } from "../../schemas/TalentFormSchema";
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

      {/* Coordonnées & Mobilité */}
      <div className="mt-8 pt-6 border-t">
        <h3 className="text-lg font-medium mb-4">Coordonnées & Mobilité</h3>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {/* Téléphone */}
          <FormField
            control={control}
            name="phone"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Téléphone</FormLabel>
                <FormControl>
                  <Input
                    placeholder="Ex: +33 6 12 34 56 78"
                    {...field}
                  />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />

          {/* Email */}
          <FormField
            control={control}
            name="email"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Email</FormLabel>
                <FormControl>
                  <Input
                    type="email"
                    placeholder="Ex: candidat@email.com"
                    {...field}
                  />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
        </div>

        {/* Mobilité */}
        <div className="mt-4">
          <h4 className="text-sm font-medium text-muted-foreground mb-3">Mobilité</h4>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {/* Permis de conduire */}
            <FormField
              control={control}
              name="driving_license"
              render={({ field }) => (
                <FormItem className="flex flex-row items-center justify-between rounded-lg border p-3 shadow-sm">
                  <div className="space-y-0.5">
                    <FormLabel>Permis de conduire</FormLabel>
                  </div>
                  <FormControl>
                    <Switch
                      checked={field.value}
                      onCheckedChange={field.onChange}
                    />
                  </FormControl>
                </FormItem>
              )}
            />

            {/* Véhicule personnel */}
            <FormField
              control={control}
              name="own_vehicle"
              render={({ field }) => (
                <FormItem className="flex flex-row items-center justify-between rounded-lg border p-3 shadow-sm">
                  <div className="space-y-0.5">
                    <FormLabel>Véhicule personnel</FormLabel>
                  </div>
                  <FormControl>
                    <Switch
                      checked={field.value}
                      onCheckedChange={field.onChange}
                    />
                  </FormControl>
                </FormItem>
              )}
            />
          </div>
        </div>

      </div>

      {/* Bio */}
      <FormField
        control={control}
        name="bio"
        render={({ field }) => (
          <FormItem className="mt-6">
            <FormLabel>Bio / Description</FormLabel>
            <FormControl>
              <Textarea
                placeholder="Brève description du profil..."
                className="resize-none h-24 rounded-xl shadow-inner"
                {...field}
              />
            </FormControl>
            <FormMessage />
          </FormItem>
        )}
      />
    </div>
  );
};