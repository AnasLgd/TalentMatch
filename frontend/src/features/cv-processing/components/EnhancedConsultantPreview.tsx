import React from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Loader2 } from 'lucide-react';
import { CvAnalysisResult } from '../types';
import { useToast } from '@/hooks/use-toast';
import { TalentCreationModal } from '@/features/consultants/components/talent-creation/TalentCreationModal';

interface EnhancedConsultantPreviewProps {
  analysisResult: CvAnalysisResult;
  companyId: number;
  onConsultantCreated: (consultantId: number) => void;
  onCancel: () => void;
}

const EnhancedConsultantPreview: React.FC<EnhancedConsultantPreviewProps> = ({
  analysisResult,
  companyId,
  onConsultantCreated,
  onCancel,
}) => {
  const [isModalOpen, setIsModalOpen] = React.useState(false);
  const { toast } = useToast();
  const candidate = analysisResult.candidate;

  // Handles opening the detailed form
  const handleOpenForm = () => {
    setIsModalOpen(true);
  };

  // Handles the success callback when a consultant is created
  const handleConsultantCreated = (consultantId: number) => {
    toast({
      title: "Talent créé",
      description: "Le profil a été créé avec succès",
      variant: "default",
    });
    
    setIsModalOpen(false);
    onConsultantCreated(consultantId);
  };

  return (
    <>
      <Card className="w-full max-w-4xl mx-auto">
        <CardHeader>
          <CardTitle>Prévisualisation du profil</CardTitle>
          <CardDescription>
            Informations extraites du CV
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-6">
            {/* Section d'informations personnelles */}
            <div className="space-y-4">
              <h3 className="text-lg font-medium">Informations personnelles</h3>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="space-y-1">
                  <p className="text-sm text-muted-foreground">Nom complet</p>
                  <div className="p-2 bg-muted rounded-md">{candidate.name}</div>
                </div>
                
                <div className="space-y-1">
                  <p className="text-sm text-muted-foreground">Email</p>
                  <div className="p-2 bg-muted rounded-md">{candidate.email}</div>
                </div>
                
                <div className="space-y-1">
                  <p className="text-sm text-muted-foreground">Téléphone</p>
                  <div className="p-2 bg-muted rounded-md">{candidate.phone}</div>
                </div>
              </div>
            </div>
            
            {/* Section des compétences */}
            <div className="space-y-4">
              <h3 className="text-lg font-medium">Compétences ({candidate.skills.length})</h3>
              <div className="flex flex-wrap gap-2">
                {candidate.skills.slice(0, 10).map((skill, index) => (
                  <Badge 
                    key={index} 
                    variant="secondary"
                    className="px-3 py-1 text-sm"
                  >
                    {skill.name} {skill.level && `(${skill.level})`}
                  </Badge>
                ))}
                {candidate.skills.length > 10 && (
                  <Badge variant="outline">+{candidate.skills.length - 10}</Badge>
                )}
              </div>
            </div>
            
            {/* Section de l'expérience professionnelle */}
            <div className="space-y-4">
              <h3 className="text-lg font-medium">Expérience professionnelle ({candidate.experience.length})</h3>
              <div className="space-y-4">
                {candidate.experience.slice(0, 3).map((exp, index) => (
                  <div key={index} className="p-4 border rounded-md">
                    <h4 className="font-medium">{exp.role}</h4>
                    <div className="text-sm text-muted-foreground">
                      {exp.company} • {exp.period}
                    </div>
                    {exp.description && (
                      <p className="mt-2 text-sm line-clamp-2">{exp.description}</p>
                    )}
                  </div>
                ))}
                {candidate.experience.length > 3 && (
                  <p className="text-sm text-muted-foreground">
                    +{candidate.experience.length - 3} autres expériences professionnelles
                  </p>
                )}
              </div>
            </div>
            
            {/* Section de l'éducation */}
            <div className="space-y-4">
              <h3 className="text-lg font-medium">Formation ({candidate.education.length})</h3>
              <div className="space-y-4">
                {candidate.education.slice(0, 2).map((edu, index) => (
                  <div key={index} className="p-4 border rounded-md">
                    <h4 className="font-medium">{edu.degree}</h4>
                    <div className="text-sm text-muted-foreground">
                      {edu.institution} • {edu.period}
                    </div>
                  </div>
                ))}
                {candidate.education.length > 2 && (
                  <p className="text-sm text-muted-foreground">
                    +{candidate.education.length - 2} autres formations
                  </p>
                )}
              </div>
            </div>
          </div>
        </CardContent>
        <CardFooter className="flex justify-between">
          <Button 
            variant="outline" 
            onClick={onCancel}
          >
            Retour
          </Button>
          <Button onClick={handleOpenForm}>
            Continuer avec ces informations
          </Button>
        </CardFooter>
      </Card>

      <TalentCreationModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        onSuccess={handleConsultantCreated}
        companyId={companyId}
        cvAnalysisResult={analysisResult}
      />
    </>
  );
};

export default EnhancedConsultantPreview;