import React, { useState, useRef } from 'react';
import { Button } from '@/components/ui/button';
import { FormLabel } from '@/components/ui/form';
import { toast } from '@/hooks/use-toast';
import { Upload, AlertTriangle } from 'lucide-react';

interface UploadImageProps {
  onImageSelected: (file: File | null) => void;
  label?: string;
  maxSizeInMB?: number;
  acceptedFormats?: string[];
}

export const UploadImage: React.FC<UploadImageProps> = ({
  onImageSelected,
  label = "Photo de profil (optionnelle)",
  maxSizeInMB = 5,
  acceptedFormats = ['.jpg', '.jpeg', '.png']
}) => {
  const [imagePreview, setImagePreview] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  // Convertir les formats en types MIME pour la validation
  const acceptedMimeTypes = {
    '.jpg': 'image/jpeg',
    '.jpeg': 'image/jpeg',
    '.png': 'image/png',
    '.gif': 'image/gif'
  };

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    setError(null);
    
    if (!file) {
      setImagePreview(null);
      onImageSelected(null);
      return;
    }

    // Vérifier le type MIME
    const fileExt = `.${file.name.split('.').pop()?.toLowerCase()}`;
    const isValidFormat = acceptedFormats.includes(fileExt);
    if (!isValidFormat) {
      setError(`Format d'image non pris en charge. Formats acceptés: ${acceptedFormats.join(', ')}`);
      setImagePreview(null);
      onImageSelected(null);
      return;
    }

    // Vérifier la taille
    const maxSizeInBytes = maxSizeInMB * 1024 * 1024;
    if (file.size > maxSizeInBytes) {
      setError(`Taille d'image trop importante. Maximum: ${maxSizeInMB}MB`);
      setImagePreview(null);
      onImageSelected(null);
      return;
    }

    // Créer un aperçu de l'image
    const previewUrl = URL.createObjectURL(file);
    setImagePreview(previewUrl);
    onImageSelected(file);
  };

  const triggerFileInput = () => {
    fileInputRef.current?.click();
  };

  const clearImage = () => {
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
    setImagePreview(null);
    setError(null);
    onImageSelected(null);
  };

  return (
    <div className="space-y-2">
      <FormLabel>{label}</FormLabel>
      <div className="flex items-start gap-4">
        <div 
          className={`w-24 h-24 border-2 border-dashed rounded-md flex items-center justify-center cursor-pointer hover:bg-muted/50 transition-colors ${error ? 'border-red-400' : 'border-border'}`}
          onClick={triggerFileInput}
        >
          {imagePreview ? (
            <img 
              src={imagePreview} 
              alt="Aperçu" 
              className="w-full h-full object-cover rounded-md" 
            />
          ) : error ? (
            <AlertTriangle className="w-8 h-8 text-red-500" />
          ) : (
            <Upload className="w-8 h-8 text-muted-foreground" />
          )}
        </div>
        <div className="flex-1 space-y-2">
          <input
            type="file"
            ref={fileInputRef}
            onChange={handleFileChange}
            accept={acceptedFormats.join(',')}
            className="hidden"
          />
          <div className="flex space-x-2">
            <Button 
              type="button" 
              variant="outline" 
              onClick={triggerFileInput}
              className="flex-1"
            >
              Sélectionner une image
            </Button>
            {imagePreview && (
              <Button 
                type="button" 
                variant="ghost" 
                onClick={clearImage}
                className="px-2"
              >
                Effacer
              </Button>
            )}
          </div>
          {error ? (
            <p className="text-xs text-red-500">{error}</p>
          ) : (
            <p className="text-xs text-muted-foreground">
              Formats acceptés: {acceptedFormats.join(', ')}. Taille maximale: {maxSizeInMB} MB
            </p>
          )}
        </div>
      </div>
    </div>
  );
};