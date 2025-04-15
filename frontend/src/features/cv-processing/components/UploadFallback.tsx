import React from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { AlertTriangle, FileX } from 'lucide-react';

interface UploadFallbackProps {
  error: string;
  fileName?: string;
  onRetry: () => void;
  onManualCreate: () => void;
}

const UploadFallback: React.FC<UploadFallbackProps> = ({ 
  error, 
  fileName, 
  onRetry, 
  onManualCreate 
}) => {
  return (
    <Card className="w-full max-w-md mx-auto">
      <CardHeader>
        <div className="flex items-center gap-2">
          <AlertTriangle className="h-5 w-5 text-destructive" />
          <CardTitle>Erreur lors de l'analyse</CardTitle>
        </div>
        <CardDescription>
          Nous n'avons pas pu extraire correctement les informations du CV
        </CardDescription>
      </CardHeader>
      <CardContent>
        <div className="flex flex-col items-center gap-4 py-6">
          <FileX className="h-16 w-16 text-muted-foreground" />
          <div className="text-center">
            <p className="font-medium">
              {fileName ? `Le fichier "${fileName}" n'a pas pu être analysé` : "Le CV n'a pas pu être analysé"}
            </p>
            <p className="mt-1 text-sm text-muted-foreground">
              {error || "Une erreur s'est produite lors de l'extraction des données"}
            </p>
          </div>
          <div className="w-full max-w-xs mt-4 p-4 bg-muted rounded-md text-sm">
            <ul className="list-disc pl-4 space-y-1 text-muted-foreground">
              <li>Vérifiez que le fichier n'est pas corrompu</li>
              <li>Assurez-vous que le CV contient du texte sélectionnable (pas juste une image)</li>
              <li>Essayez avec un format différent si possible</li>
            </ul>
          </div>
        </div>
      </CardContent>
      <CardFooter className="flex flex-col sm:flex-row gap-3">
        <Button 
          variant="outline" 
          className="w-full sm:w-auto"
          onClick={onRetry}
        >
          Réessayer avec un autre fichier
        </Button>
        <Button 
          className="w-full sm:w-auto"
          onClick={onManualCreate}
        >
          Créer manuellement
        </Button>
      </CardFooter>
    </Card>
  );
};

export default UploadFallback;