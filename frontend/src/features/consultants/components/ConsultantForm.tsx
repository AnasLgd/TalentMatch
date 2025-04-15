import React, { useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import * as z from "zod";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { uploadService, UploadErrorType, UploadError } from "../services/upload-service";
import { UploadImage } from "./UploadImage";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { useConsultants } from "../hooks/useConsultants";
import { AvailabilityStatus, ConsultantCreate } from "../types";
import { toast } from "@/hooks/use-toast";
import { Loader2 } from "lucide-react";

// Schéma de validation Zod
const consultantFormSchema = z.object({
  first_name: z.string().min(1, { message: "Le champ prénom est requis" }),
  last_name: z.string().min(1, { message: "Le champ nom est requis" }),
  title: z.string().min(1, { message: "Le champ titre est requis" }),
  experience_years: z.preprocess(
    (value) => (value === "" ? undefined : Number(value)),
    z.number().min(0).max(50).superRefine((val, ctx) => {
      if (val === undefined) {
        ctx.addIssue({
          code: z.ZodIssueCode.custom,
          message: "Le champ expérience est requis",
        });
        return z.NEVER;
      }
    })
  ),
  company_id: z.number(),
  // Définir user_id comme acceptant explicitement null
  user_id: z.literal(null),
  bio: z.string().optional(),
  // Autres champs optionnels
  availability_status: z.nativeEnum(AvailabilityStatus).optional(),
  availability_date: z.string().optional(),
});

// Type d'entrée du formulaire basé sur le schéma Zod
type ConsultantFormValues = z.infer<typeof consultantFormSchema>;

interface ConsultantFormProps {
  onCancel: () => void;
  onSuccess: () => void;
  userId: number | null;
  companyId: number;
}

export const ConsultantForm: React.FC<ConsultantFormProps> = ({
  onCancel,
  onSuccess,
  userId,
  companyId,
}) => {
  const { createConsultant, isCreating } = useConsultants();
  const [photoFile, setPhotoFile] = useState<File | null>(null);
  
  // Initialiser le formulaire avec les valeurs par défaut
  const form = useForm<ConsultantFormValues>({
    resolver: zodResolver(consultantFormSchema),
    defaultValues: {
      user_id: userId,
      company_id: companyId,
      first_name: "",
      last_name: "",
      title: "",
      experience_years: undefined,
      bio: "",
    },
  });
  
  // Fonction pour gérer la sélection de photo
  const handleImageSelected = (file: File | null) => {
    setPhotoFile(file);
  };

  // Gestion de la soumission du formulaire
  const onSubmit = async (data: ConsultantFormValues) => {
    try {
      
      // Construire l'objet consultant
      const consultantData: ConsultantCreate = {
        // Inclure user_id seulement s'il est défini
        ...(data.user_id ? { user_id: data.user_id } : {}),
        company_id: data.company_id,
        title: data.title,
        experience_years: data.experience_years,
        bio: data.bio,
        availability_status: data.availability_status || AvailabilityStatus.AVAILABLE,
        // Inclure first_name et last_name pour mettre à jour le nom de l'utilisateur
        first_name: data.first_name,
        last_name: data.last_name
      };

      // Upload de la photo si présente
      let photoUrl = null;
      if (photoFile) {
        try {
          // Utiliser le service d'upload pour envoyer la photo vers MinIO
          photoUrl = await uploadService.uploadFile(photoFile, 'consultants/profiles');
          
          // Ajouter l'URL de la photo au consultant
          consultantData.photo_url = photoUrl;
        } catch (error: unknown) {
          const uploadError = error as UploadError;
          console.error("Erreur lors de l'upload de la photo:", error);
          
          // Gestion spécifique selon le type d'erreur
          if (uploadError.type === UploadErrorType.FORMAT_INVALID) {
            toast({
              title: "Format d'image non pris en charge",
              description: uploadError.message,
              variant: "destructive",
            });
            return; // Arrêter la création du consultant
          } else if (uploadError.type === UploadErrorType.SIZE_EXCEEDED) {
            toast({
              title: "Taille d'image excessive",
              description: uploadError.message,
              variant: "destructive",
            });
            return; // Arrêter la création du consultant
          } else {
            // Erreur d'upload mais on continue sans la photo
            toast({
              title: "Erreur d'upload",
              description: "La photo n'a pas pu être téléchargée, mais le profil sera créé sans photo.",
              variant: "destructive",
            });
          }
        }
      }

      // Créer le consultant
      await createConsultant(consultantData);
      
      // Notification de succès
      toast({
        title: "Consultant créé",
        description: "Le profil consultant a été créé avec succès",
        variant: "default",
      });

      // Appeler la fonction de callback onSuccess
      onSuccess();
    } catch (error) {
      toast({
        title: "Erreur",
        description: "Une erreur est survenue lors de la création du consultant",
        variant: "destructive",
      });
      console.error("Erreur lors de la création du consultant:", error);
    }
  };

  return (
    <div className="max-w-2xl mx-auto p-6 bg-background rounded-lg shadow-md">
      <h2 className="text-2xl font-bold mb-6 text-center">Créer un nouveau consultant</h2>

      <Form {...form}>
        <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {/* Prénom */}
            <FormField
              control={form.control}
              name="first_name"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Prénom*</FormLabel>
                  <FormControl>
                    <Input placeholder="Prénom" {...field} />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />

            {/* Nom */}
            <FormField
              control={form.control}
              name="last_name"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Nom*</FormLabel>
                  <FormControl>
                    <Input placeholder="Nom" {...field} />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
          </div>

          {/* Titre */}
          <FormField
            control={form.control}
            name="title"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Titre*</FormLabel>
                <FormControl>
                  <Input placeholder="Titre (ex: Développeur Java, DevOps, etc.)" {...field} />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />

          {/* Années d'expérience */}
          <FormField
            control={form.control}
            name="experience_years"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Années d'expérience*</FormLabel>
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

          {/* Bio */}
          <FormField
            control={form.control}
            name="bio"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Bio</FormLabel>
                <FormControl>
                  <Textarea 
                    placeholder="Description du consultant..." 
                    {...field} 
                    className="min-h-[100px]"
                  />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />

          {/* Upload de photo - Utilisation du composant dédié */}
          <UploadImage
            onImageSelected={handleImageSelected}
            label="Photo de profil (optionnelle)"
            maxSizeInMB={5}
            acceptedFormats={['.jpg', '.jpeg', '.png']}
          />

          <div className="flex justify-end space-x-2 pt-4">
            <Button type="button" variant="outline" onClick={onCancel}>
              Annuler
            </Button>
            <Button type="submit" disabled={isCreating}>
              {isCreating && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
              Créer le consultant
            </Button>
          </div>
        </form>
      </Form>
    </div>
  );
};