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
import { Textarea } from "@/components/ui/textarea";
import { Card, CardContent } from "@/components/ui/card";
import { HrRating } from "../HrRating";
import { TalentFormValues } from "../TalentMultiStepForm";
import { Badge } from "@/components/ui/badge";
import { cn } from "@/lib/utils";
import { PlusCircle, Trash2 } from "lucide-react";

interface ProjectsStepProps {
  autoFilledFields: string[];
}

export const ProjectsStep: React.FC<ProjectsStepProps> = ({ 
  autoFilledFields 
}) => {
  const { control, watch, setValue } = useFormContext<TalentFormValues>();
  const [newTitle, setNewTitle] = useState("");
  const [newDescription, setNewDescription] = useState("");
  const [newPeriod, setNewPeriod] = useState("");
  
  // Use field array for dynamic projects array
  const { fields, append, remove } = useFieldArray({
    control,
    name: "projects",
  });
  
  // Handle adding a new project
  const handleAddProject = () => {
    if (newTitle.trim()) {
      append({
        title: newTitle.trim(),
        description: newDescription.trim(),
        period: newPeriod.trim(),
        complexity_rating: 3,
        impact_rating: 3,
        autonomy_rating: 3,
      });
      
      // Reset form
      setNewTitle("");
      setNewDescription("");
      setNewPeriod("");
    }
  };
  
  return (
    <div className="space-y-6">
      <div className="bg-muted p-4 rounded-md">
        <h3 className="text-lg font-medium mb-4">Ajouter un projet / référence</h3>
        
        <div className="space-y-4">
          {/* Project title */}
          <div>
            <FormLabel>Titre du projet*</FormLabel>
            <Input
              placeholder="ex: Refonte du SI client pour Entreprise X"
              value={newTitle}
              onChange={(e) => setNewTitle(e.target.value)}
            />
          </div>
          
          {/* Project description */}
          <div>
            <FormLabel>Description</FormLabel>
            <Textarea
              placeholder="Contexte, technologies, réalisations..."
              value={newDescription}
              onChange={(e) => setNewDescription(e.target.value)}
              className="min-h-[100px]"
            />
          </div>
          
          {/* Project period */}
          <div>
            <FormLabel>Période</FormLabel>
            <Input
              placeholder="ex: Jan 2023 - Mars 2023"
              value={newPeriod}
              onChange={(e) => setNewPeriod(e.target.value)}
            />
          </div>
          
          <Button 
            type="button" 
            onClick={handleAddProject}
            disabled={!newTitle.trim()}
          >
            <PlusCircle className="h-4 w-4 mr-2" /> Ajouter ce projet
          </Button>
        </div>
      </div>
      
      {/* List of projects */}
      <div className="space-y-4">
        <h3 className="text-lg font-medium">Projets et références ({fields.length})</h3>
        
        {fields.length === 0 && (
          <div className="text-center py-8 text-muted-foreground">
            Aucun projet ajouté. Utilisez le formulaire ci-dessus pour ajouter des projets.
          </div>
        )}
        
        {fields.map((field, index) => (
          <Card 
            key={field.id} 
            className={cn(
              "relative border",
              autoFilledFields.includes("projects") && "bg-blue-50"
            )}
          >
            <CardContent className="p-4">
              <div className="flex flex-col">
                <div className="flex justify-between mb-2">
                  <div className="font-medium flex items-center">
                    {watch(`projects.${index}.title`)}
                    {autoFilledFields.includes("projects") && (
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
                
                {/* Project period */}
                <div className="text-sm text-muted-foreground mb-2">
                  {watch(`projects.${index}.period`)}
                </div>
                
                {/* Project description */}
                <div className="text-sm mb-4">
                  {watch(`projects.${index}.description`)}
                </div>
                
                {/* HR Ratings section */}
                <div className="mt-4 pt-4 border-t">
                  <h4 className="font-medium mb-3 flex items-center">
                    <span className="mr-2">Qualification RH du projet</span>
                    <Badge variant="outline">Interne</Badge>
                  </h4>
                  
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    {/* Complexity Rating */}
                    <FormField
                      control={control}
                      name={`projects.${index}.complexity_rating`}
                      render={({ field }) => (
                        <FormItem>
                          <FormLabel>Complexité</FormLabel>
                          <FormControl>
                            <HrRating
                              value={field.value || 0}
                              onChange={field.onChange}
                              size="sm"
                            />
                          </FormControl>
                          <p className="text-xs text-muted-foreground mt-1">
                            Évaluez la complexité technique
                          </p>
                        </FormItem>
                      )}
                    />
                    
                    {/* Impact Rating */}
                    <FormField
                      control={control}
                      name={`projects.${index}.impact_rating`}
                      render={({ field }) => (
                        <FormItem>
                          <FormLabel>Impact</FormLabel>
                          <FormControl>
                            <HrRating
                              value={field.value || 0}
                              onChange={field.onChange}
                              size="sm"
                            />
                          </FormControl>
                          <p className="text-xs text-muted-foreground mt-1">
                            Évaluez l'impact business
                          </p>
                        </FormItem>
                      )}
                    />
                    
                    {/* Autonomy Rating */}
                    <FormField
                      control={control}
                      name={`projects.${index}.autonomy_rating`}
                      render={({ field }) => (
                        <FormItem>
                          <FormLabel>Autonomie</FormLabel>
                          <FormControl>
                            <HrRating
                              value={field.value || 0}
                              onChange={field.onChange}
                              size="sm"
                            />
                          </FormControl>
                          <p className="text-xs text-muted-foreground mt-1">
                            Évaluez le niveau d'autonomie
                          </p>
                        </FormItem>
                      )}
                    />
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
};