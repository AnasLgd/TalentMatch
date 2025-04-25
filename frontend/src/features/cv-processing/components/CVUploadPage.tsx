import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Container } from '@/components/ui/container';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Button } from '@/components/ui/button';
import { ArrowLeft } from 'lucide-react';
import CVUploadForm from './CVUploadForm';
import EnhancedConsultantPreview from './EnhancedConsultantPreview';
import UploadFallback from './UploadFallback';
import { CvAnalysisResult } from '../types';

const CVUploadPage: React.FC = () => {
  const navigate = useNavigate();
  const [currentStep, setCurrentStep] = useState<'upload' | 'preview' | 'error'>('upload');
  const [analysisResult, setAnalysisResult] = useState<CvAnalysisResult | null>(null);
  const [errorMessage, setErrorMessage] = useState<string>('');
  const [fileName, setFileName] = useState<string>('');
  
  // TODO: Get companyId from context or user state in a real implementation
  const companyId = 1;

  const handleUploadSuccess = (result: CvAnalysisResult) => {
    setAnalysisResult(result);
    setCurrentStep('preview');
  };

  const handleUploadError = (error: string) => {
    setErrorMessage(error);
    setCurrentStep('error');
  };

  const handleConsultantCreated = (consultantId: number) => {
    // Navigate to the consultant details page
    navigate(`/consultants/${consultantId}`);
  };

  const handleRetry = () => {
    setCurrentStep('upload');
    setAnalysisResult(null);
    setErrorMessage('');
  };

  const handleManualCreate = () => {
    // Navigate to consultants page - the modal will be opened from there
    navigate('/consultants');
  };

  return (
    <Container className="py-8">
      <div className="mb-6">
        <Button
          variant="ghost"
          className="flex items-center gap-1 px-2"
          onClick={() => navigate('/consultants')}
        >
          <ArrowLeft className="h-4 w-4" />
          Retour aux consultants
        </Button>
        
        <h1 className="text-3xl font-bold tracking-tight mt-4">Upload & Parsing de CV</h1>
        <p className="text-muted-foreground mt-1">
          Créez rapidement un profil talent à partir d'un CV
        </p>
      </div>

      <div className="mt-8">
        {currentStep === 'upload' && (
          <CVUploadForm 
            onUploadSuccess={handleUploadSuccess} 
            onUploadError={handleUploadError} 
          />
        )}

        {currentStep === 'preview' && analysisResult && (
          <EnhancedConsultantPreview 
            analysisResult={analysisResult}
            companyId={companyId}
            onConsultantCreated={handleConsultantCreated}
            onCancel={handleRetry}
          />
        )}

        {currentStep === 'error' && (
          <UploadFallback 
            error={errorMessage}
            fileName={fileName}
            onRetry={handleRetry}
            onManualCreate={handleManualCreate}
          />
        )}
      </div>

      <div className="mt-16">
        <h2 className="text-xl font-semibold mb-4">Guide d'utilisation</h2>
        <Tabs defaultValue="format">
          <TabsList>
            <TabsTrigger value="format">Formats supportés</TabsTrigger>
            <TabsTrigger value="structure">Structure recommandée</TabsTrigger>
            <TabsTrigger value="tips">Astuces</TabsTrigger>
          </TabsList>
          <TabsContent value="format" className="p-4 bg-muted rounded-md mt-2">
            <ul className="list-disc pl-5 space-y-2">
              <li><strong>PDF</strong> - Format recommandé pour une meilleure extraction</li>
              <li><strong>DOCX</strong> - Compatible avec les versions récentes de Word</li>
              <li><strong>DOC</strong> - Compatible avec les versions anciennes de Word</li>
              <li>Les fichiers doivent être inférieurs à 10Mo</li>
            </ul>
          </TabsContent>
          <TabsContent value="structure" className="p-4 bg-muted rounded-md mt-2">
            <p className="mb-2">Pour des résultats optimaux, les CV devraient inclure clairement:</p>
            <ul className="list-disc pl-5 space-y-2">
              <li>Informations de contact (nom, email, téléphone)</li>
              <li>Compétences techniques clairement listées</li>
              <li>Expérience professionnelle avec dates et description</li>
              <li>Formation avec dates et institutions</li>
            </ul>
          </TabsContent>
          <TabsContent value="tips" className="p-4 bg-muted rounded-md mt-2">
            <ul className="list-disc pl-5 space-y-2">
              <li>Privilégiez les CV avec texte sélectionnable plutôt que des images</li>
              <li>Évitez les mises en page complexes (colonnes multiples, tables, etc.)</li>
              <li>Vérifiez que les données extraites sont correctes avant création</li>
              <li>En cas d'échec, essayez de convertir le fichier en PDF simple</li>
            </ul>
          </TabsContent>
        </Tabs>
      </div>
    </Container>
  );
};

export default CVUploadPage;