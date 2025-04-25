import React, { useState } from "react";
import { useFormContext, useFieldArray } from "react-hook-form";
import {
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Card, CardContent } from "@/components/ui/card";
import { HrRating } from "../HrRating";
import { TalentFormValues } from "../TalentMultiStepForm";
import { Badge } from "@/components/ui/badge";
import { cn } from "@/lib/utils";
import { PlusCircle, Trash2 } from "lucide-react";

interface SkillsStepProps {
  autoFilledFields: string[];
}

// Skill categories
const SKILL_CATEGORIES = [
  "Frontend",
  "Backend",
  "DevOps",
  "Database",
  "Mobile",
  "Cloud",
  "Architecture",
  "Méthodes",
  "Fonctionnel",
  "Langues",
  "Outils",
  "Autre"
];

// Experience levels
const SKILL_LEVELS = [
  "Débutant",
  "Intermédiaire",
  "Avancé",
  "Expert"
];

export const SkillsStep: React.FC<SkillsStepProps> = ({ 
  autoFilledFields 
}) => {
  const { control, watch, setValue } = useFormContext<TalentFormValues>();
  const [newSkill, setNewSkill] = useState("");
  const [newCategory, setNewCategory] = useState(SKILL_CATEGORIES[0]);
  
  // Use field array for dynamic skills array
  const { fields, append, remove } = useFieldArray({
    control,
    name: "skills",
  });
  
  // Handle adding a new skill
  const handleAddSkill = () => {
    if (newSkill.trim()) {
      append({
        name: newSkill.trim(),
        category: newCategory,
        level: "Intermédiaire",
        years: 1,
        hr_rating: 3,
      });
      
      setNewSkill("");
    }
  };
  
  return (
    <div className="space-y-6">
      <div className="bg-muted p-4 rounded-md">
        <h3 className="text-lg font-medium mb-4">Compétences</h3>
        
        <div className="space-y-4">
          {/* Add new skill */}
          <div className="flex flex-col gap-3 sm:flex-row sm:items-end">
            <div className="flex-1">
              <FormLabel>Nouvelle compétence</FormLabel>
              <Input
                placeholder="Ajouter une compétence..."
                value={newSkill}
                onChange={(e) => setNewSkill(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === "Enter") {
                    e.preventDefault();
                    handleAddSkill();
                  }
                }}
              />
            </div>
            
            <div className="w-full sm:w-40">
              <FormLabel>Catégorie</FormLabel>
              <Select value={newCategory} onValueChange={setNewCategory}>
                <SelectTrigger>
                  <SelectValue placeholder="Catégorie" />
                </SelectTrigger>
                <SelectContent>
                  {SKILL_CATEGORIES.map((category) => (
                    <SelectItem key={category} value={category}>
                      {category}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
            
            <Button type="button" onClick={handleAddSkill} className="w-full sm:w-auto">
              <PlusCircle className="h-4 w-4 mr-2" /> Ajouter
            </Button>
          </div>
        </div>
      </div>
      
      {/* List of skills */}
      <div className="space-y-4">
        <h3 className="text-lg font-medium">Compétences ({fields.length})</h3>
        
        {fields.length === 0 && (
          <div className="text-center py-8 text-muted-foreground">
            Aucune compétence ajoutée. Utilisez le formulaire ci-dessus pour ajouter des compétences.
          </div>
        )}
        
        {fields.map((field, index) => (
          <Card 
            key={field.id} 
            className={cn(
              "relative border",
              autoFilledFields.includes("skills") && "bg-blue-50"
            )}
          >
            <CardContent className="p-4">
              <div className="flex flex-col">
                <div className="flex justify-between mb-2">
                  <div className="font-medium flex items-center">
                    {`${field.name} `}
                    <Badge variant="secondary" className="ml-2">
                      {watch(`skills.${index}.category`) || "Non catégorisé"}
                    </Badge>
                    {autoFilledFields.includes("skills") && (
                      <Badge variant="outline" className="ml-2 bg-blue-100">
                        CV
                      </Badge>
                    )}
                  </div>
                  <Button 
                    variant="ghost" 
                    size="icon" 
                    onClick={() => remove(index)}
                    className="h-8 w-8"
                  >
                    <Trash2 className="h-4 w-4" />
                  </Button>
                </div>
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-2">
                  {/* Skill level */}
                  <FormField
                    control={control}
                    name={`skills.${index}.level`}
                    render={({ field }) => (
                      <FormItem>
                        <FormLabel>Niveau</FormLabel>
                        <Select
                          value={field.value}
                          onValueChange={field.onChange}
                        >
                          <SelectTrigger>
                            <SelectValue placeholder="Niveau de compétence" />
                          </SelectTrigger>
                          <SelectContent>
                            {SKILL_LEVELS.map((level) => (
                              <SelectItem key={level} value={level}>
                                {level}
                              </SelectItem>
                            ))}
                          </SelectContent>
                        </Select>
                        <FormMessage />
                      </FormItem>
                    )}
                  />
                  
                  {/* Years of experience */}
                  <FormField
                    control={control}
                    name={`skills.${index}.years`}
                    render={({ field }) => (
                      <FormItem>
                        <FormLabel>Années d'expérience</FormLabel>
                        <FormControl>
                          <Input
                            type="number"
                            min={0}
                            max={30}
                            {...field}
                            onChange={(e) => field.onChange(parseInt(e.target.value) || 0)}
                          />
                        </FormControl>
                        <FormMessage />
                      </FormItem>
                    )}
                  />
                </div>
                
                {/* HR Rating section */}
                <div className="mt-4 pt-4 border-t">
                  <FormField
                    control={control}
                    name={`skills.${index}.hr_rating`}
                    render={({ field }) => (
                      <FormItem>
                        <FormLabel className="flex items-center">
                          <span className="mr-2">Évaluation RH</span>
                          <Badge variant="outline">Interne</Badge>
                        </FormLabel>
                        <FormControl>
                          <HrRating
                            value={field.value || 0}
                            onChange={field.onChange}
                          />
                        </FormControl>
                        <p className="text-xs text-muted-foreground mt-1">
                          Évaluez cette compétence sur une échelle de 1 à 5 étoiles
                        </p>
                      </FormItem>
                    )}
                  />
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
};