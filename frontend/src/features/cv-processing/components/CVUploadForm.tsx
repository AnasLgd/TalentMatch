import React, { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { AlertTriangle, FileUp, Loader2 } from 'lucide-react';
import { cvProcessingService } from '../services/cv-processing-service';
import { CvFileStatus, CvUploadResponse, CvAnalysisResult } from '../types';
import { useToast } from '@/hooks/use-toast';

interface CVUploadFormProps {
  onUploadSuccess: (result: CvAnalysisResult) => void;
  onUploadError: (error: string) => void;
}

const CVUploadForm: React.FC<CVUploadFormProps> = ({ onUploadSuccess, onUploadError }) => {
  const [file, setFile] = useState<File | null>(null);
  const [isDragging, setIsDragging] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const { toast } = useToast();

  const acceptedFileTypes = [
    'application/pdf',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'application/msword'
  ];
  const acceptedExtensions = ['.pdf', '.docx', '.doc'];

  const handleDragOver = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragging(false);
  };

  const handleDrop = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragging(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      const droppedFile = e.dataTransfer.files[0];
      validateAndSetFile(droppedFile);
    }
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      const selectedFile = e.target.files[0];
      validateAndSetFile(selectedFile);
    }
  };

  const validateAndSetFile = (file: File) => {
    const fileExtension = `.${file.name.split('.').pop()?.toLowerCase()}`;
    
    if (!acceptedExtensions.includes(fileExtension)) {
      setError(`Format de fichier non supporté. Formats acceptés: ${acceptedExtensions.join(', ')}`);
      setFile(null);
      return;
    }
    
    if (file.size === 0) {
      setError('Le fichier est vide');
      setFile(null);
      return;
    }
    
    if (file.size > 10 * 1024 * 1024) {
      setError('Le fichier est trop volumineux (max: 10MB)');
      setFile(null);
      return;
    }
    
    setError(null);
    setFile(file);
  };

  const handleUpload = async () => {
    if (!file) return;
    
    try {
      setUploading(true);
      setError(null);
      
      // Utilisation du service pour télécharger et analyser le CV en une seule opération
      const result = await cvProcessingService.uploadAndAnalyzeCv(file);
      
      toast({
        title: "CV reçu",
        description: "Le CV a été analysé avec succès",
        variant: "default",
      });
      
      onUploadSuccess(result);
    } catch (error) {
      console.error("Erreur lors de l'upload du CV:", error);
      const errorMessage = error instanceof Error ? error.message : "Une erreur s'est produite lors de l'upload du CV";
      setError(errorMessage);
      onUploadError(errorMessage);
      
      toast({
        title: "Erreur",
        description: errorMessage,
        variant: "destructive",
      });
    } finally {
      setUploading(false);
    }
  };

  return (
    <Card className="w-full max-w-md mx-auto">
      <CardHeader>
        <CardTitle>Upload de CV</CardTitle>
        <CardDescription>
          Déposez un fichier CV pour créer automatiquement un profil consultant
        </CardDescription>
      </CardHeader>
      <CardContent>
        <div
          className={`border-2 border-dashed rounded-lg p-6 text-center cursor-pointer transition-colors ${
            isDragging ? 'border-primary bg-primary/10' : 'border-muted-foreground/20'
          }`}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
          onClick={() => document.getElementById('file-upload')?.click()}
        >
          <FileUp className="mx-auto h-12 w-12 text-muted-foreground" />
          <p className="mt-2 text-sm text-muted-foreground">
            Glissez-déposez un fichier ici ou cliquez pour parcourir
          </p>
          <p className="mt-1 text-xs text-muted-foreground">
            Formats supportés: PDF, DOCX, DOC (max: 10MB)
          </p>
          <input
            id="file-upload"
            type="file"
            className="hidden"
            accept={acceptedFileTypes.join(',')}
            onChange={handleFileChange}
          />
        </div>

        {file && (
          <div className="mt-4 p-3 bg-muted rounded-md flex items-center justify-between">
            <span className="text-sm font-medium truncate max-w-[200px]">{file.name}</span>
            <span className="text-xs text-muted-foreground">
              {(file.size / 1024 / 1024).toFixed(2)} MB
            </span>
          </div>
        )}

        {error && (
          <div className="mt-4 p-3 bg-destructive/10 text-destructive rounded-md flex items-center">
            <AlertTriangle className="h-4 w-4 mr-2 flex-shrink-0" />
            <span className="text-sm">{error}</span>
          </div>
        )}
      </CardContent>
      <CardFooter>
        <Button 
          onClick={handleUpload} 
          disabled={!file || uploading} 
          className="w-full"
        >
          {uploading ? (
            <>
              <Loader2 className="mr-2 h-4 w-4 animate-spin" />
              Analyse en cours...
            </>
          ) : (
            'Uploader et analyser'
          )}
        </Button>
      </CardFooter>
    </Card>
  );
};

export default CVUploadForm;