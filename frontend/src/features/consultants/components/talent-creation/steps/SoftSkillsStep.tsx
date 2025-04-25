import React, { useState } from "react";
import { useFormContext, useFieldArray } from "react-hook-form";
import {
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
  FormDescription,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { HrRating } from "../HrRating";
import { TalentFormValues } from "../TalentMultiStepForm";
import { Badge } from "@/components/ui/badge";
import { Switch } from "@/components/ui/switch";
import { PlusCircle, Trash2 } from "lucide-react";

// Common soft skills that can be suggested
const COMMON_SOFT_SKILLS = [
  "Communication",
  "Travail d'équipe",
  "Adaptabilité",
  "Résolution de problèmes",
  "Gestion du temps",
  "Leadership",
  "Créativité",
  "Esprit critique",
  "Attitude positive",
  "Autonomie",
  "Sens du détail",
  "Orientation client",
];

interface SoftSkillsStepProps {
  autoFilledFields: string[];
}

export const SoftSkillsStep: React.FC<SoftSkillsStepProps> = ({ 
  autoFilledFields 
}) => {
  const { control, watch, setValue } = useFormContext<TalentFormValues>();
  const [newSoftSkill, setNewSoftSkill] = useState("");
  
  // Use field array for dynamic soft skills array
  const { fields, append, remove } = useFieldArray({
    control,
    name: "soft_skills",
  });
  
  // Handle adding a new soft skill
  const handleAddSoftSkill = () => {
    if (newSoftSkill.trim()) {
      append({
        name: newSoftSkill.trim(),
        rating: 3,
      });
      
      setNewSoftSkill("");
    }
  };
  
  // Handle adding a pre-defined soft skill
  const handleAddPredefinedSkill = (skill: string) => {
    // Check if skill already exists
    const exists = fields.some(field => 
      field.name.toLowerCase() === skill.toLowerCase()
    );
    
    if (!exists) {
      append({
        name: skill,
        rating: 3,
      });
    }
  };
  
  return (
    <div className="space-y-6">
      {/* Soft Skills Section */}
      <div className="space-y-4">
        <h3 className="text-lg font-medium">Soft Skills</h3>
        
        <div className="bg-muted p-4 rounded-md">
          <div className="flex flex-col sm:flex-row gap-2">
            <div className="flex-1">
              <Input
                placeholder="Ajouter une soft skill..."
                value={newSoftSkill}
                onChange={(e) => setNewSoftSkill(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === "Enter") {
                    e.preventDefault();
                    handleAddSoftSkill();
                  }
                }}
              />
            </div>
            <Button type="button" onClick={handleAddSoftSkill}>
              <PlusCircle className="h-4 w-4 mr-2" /> Ajouter
            </Button>
          </div>
          
          <div className="mt-4">
            <p className="text-sm mb-2">Suggestions :</p>
            <div className="flex flex-wrap gap-2">
              {COMMON_SOFT_SKILLS.map((skill) => (
                <Badge 
                  key={skill}
                  variant="outline"
                  className="cursor-pointer hover:bg-accent"
                  onClick={() => handleAddPredefinedSkill(skill)}
                >
                  {skill}
                </Badge>
              ))}
            </div>
          </div>
        </div>
        
        {/* List of soft skills */}
        <div className="space-y-3">
          {fields.length === 0 && (
            <div className="text-center py-4 text-muted-foreground">
              Aucune soft skill ajoutée.
            </div>
          )}
          
          {fields.map((field, index) => (
            <Card key={field.id} className="relative border">
              <CardContent className="p-3">
                <div className="flex justify-between items-center">
                  <div className="font-medium mr-2">{field.name}</div>
                  
                  <div className="flex items-center gap-4">
                    <FormField
                      control={control}
                      name={`soft_skills.${index}.rating`}
                      render={({ field: ratingField }) => (
                        <FormItem>
                          <FormControl>
                            <HrRating
                              value={ratingField.value || 0}
                              onChange={ratingField.onChange}
                              size="sm"
                            />
                          </FormControl>
                        </FormItem>
                      )}
                    />
                    
                    <Button 
                      variant="ghost" 
                      size="icon" 
                      onClick={() => remove(index)}
                      className="h-8 w-8"
                    >
                      <Trash2 className="h-4 w-4" />
                    </Button>
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
      
      {/* Preferences Section */}
      <div className="space-y-4 pt-6 border-t">
        <h3 className="text-lg font-medium">Préférences</h3>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {/* Location */}
          <FormField
            control={control}
            name="location"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Localisation</FormLabel>
                <FormControl>
                  <Input placeholder="Ville, Région, Pays..." {...field} />
                </FormControl>
                <FormDescription>
                  Emplacement géographique préféré
                </FormDescription>
                <FormMessage />
              </FormItem>
            )}
          />
          
          {/* Daily rate */}
          <FormField
            control={control}
            name="daily_rate"
            render={({ field }) => (
              <FormItem>
                <FormLabel>TJM (€)</FormLabel>
                <FormControl>
                  <Input
                    type="number"
                    placeholder="Tarif journalier moyen"
                    {...field}
                    value={field.value || ""}
                    onChange={(e) => field.onChange(e.target.value === "" ? "" : parseFloat(e.target.value))}
                    min={0}
                  />
                </FormControl>
                <FormDescription>
                  Tarif journalier moyen
                </FormDescription>
                <FormMessage />
              </FormItem>
            )}
          />
        </div>
        
        {/* Max travel distance */}
        <FormField
          control={control}
          name="max_travel_distance"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Distance maximale de déplacement (km)</FormLabel>
              <FormControl>
                <Input
                  type="number"
                  placeholder="Distance maximale de déplacement..."
                  {...field}
                  value={field.value || ""}
                  onChange={(e) => field.onChange(e.target.value === "" ? "" : parseInt(e.target.value))}
                  min={0}
                />
              </FormControl>
              <FormDescription>
                Distance maximale que le talent est prêt à parcourir
              </FormDescription>
              <FormMessage />
            </FormItem>
          )}
        />
        
        {/* Remote work */}
        <FormField
          control={control}
          name="remote_work"
          render={({ field }) => (
            <FormItem className="flex flex-row items-center justify-between rounded-lg border p-3 shadow-sm">
              <div className="space-y-0.5">
                <FormLabel>Télétravail</FormLabel>
                <FormDescription>
                  Le talent est-il disponible pour travailler à distance ?
                </FormDescription>
              </div>
              <FormControl>
                <Switch
                  checked={field.value || false}
                  onCheckedChange={field.onChange}
                />
              </FormControl>
            </FormItem>
          )}
        />
      </div>
    </div>
  );
};