import React, { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Badge } from '@/components/ui/badge';
import { Check, Edit2, X, Loader2 } from 'lucide-react';
import { CvAnalysisResult } from '../types';
import { cvProcessingService } from '../services/cv-processing-service';
import { useToast } from '@/hooks/use-toast';
import { Skill, Experience, Education } from '@/features/consultants/types';

interface ConsultantPreviewProps {
  analysisResult: CvAnalysisResult;
  companyId: number;
  onConsultantCreated: (consultantId: number) => void;
  onCancel: () => void;
}

const ConsultantPreview: React.FC<ConsultantPreviewProps> = ({
  analysisResult,
  companyId,
  onConsultantCreated,
  onCancel,
}) => {
  const [isEditing, setIsEditing] = useState(false);
  const [creating, setCreating] = useState(false);
  const [candidate, setCandidate] = useState(analysisResult.candidate);
  const { toast } = useToast();

  const handleCreateConsultant = async () => {
    try {
      setCreating(true);
      // Appel au service pour créer un consultant à partir du CV analysé
      const consultantId = await cvProcessingService.createConsultantFromCv(
        analysisResult.fileId,
        companyId
      );
      
      toast({
        title: "Consultant créé",
        description: "Le profil consultant a été créé avec succès",
        variant: "default",
      });
      
      onConsultantCreated(consultantId);
    } catch (error) {
      console.error("Erreur lors de la création du consultant:", error);
      const errorMessage = error instanceof Error ? error.message : "Une erreur s'est produite lors de la création du consultant";
      
      toast({
        title: "Erreur",
        description: errorMessage,
        variant: "destructive",
      });
    } finally {
      setCreating(false);
    }
  };

  const handleFieldChange = (field: string, value: string) => {
    setCandidate(prev => ({
      ...prev,
      [field]: value
    }));
  };

  return (
    <Card className="w-full max-w-4xl mx-auto">
      <CardHeader className="flex flex-row items-center justify-between">
        <div>
          <CardTitle>Prévisualisation du profil</CardTitle>
          <CardDescription>
            Vérifiez et validez les informations extraites du CV
          </CardDescription>
        </div>
        <Button 
          variant="outline" 
          size="sm"
          onClick={() => setIsEditing(!isEditing)}
        >
          {isEditing ? (
            <>
              <Check className="mr-2 h-4 w-4" />
              Terminer
            </>
          ) : (
            <>
              <Edit2 className="mr-2 h-4 w-4" />
              Modifier
            </>
          )}
        </Button>
      </CardHeader>
      <CardContent>
        <div className="space-y-6">
          {/* Section d'informations personnelles */}
          <div className="space-y-4">
            <h3 className="text-lg font-medium">Informations personnelles</h3>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="name">Nom complet</Label>
                {isEditing ? (
                  <Input
                    id="name"
                    value={candidate.name}
                    onChange={(e) => handleFieldChange('name', e.target.value)}
                  />
                ) : (
                  <div className="p-2 bg-muted rounded-md">{candidate.name}</div>
                )}
              </div>
              
              <div className="space-y-2">
                <Label htmlFor="email">Email</Label>
                {isEditing ? (
                  <Input
                    id="email"
                    type="email"
                    value={candidate.email}
                    onChange={(e) => handleFieldChange('email', e.target.value)}
                  />
                ) : (
                  <div className="p-2 bg-muted rounded-md">{candidate.email}</div>
                )}
              </div>
              
              <div className="space-y-2">
                <Label htmlFor="phone">Téléphone</Label>
                {isEditing ? (
                  <Input
                    id="phone"
                    value={candidate.phone}
                    onChange={(e) => handleFieldChange('phone', e.target.value)}
                  />
                ) : (
                  <div className="p-2 bg-muted rounded-md">{candidate.phone}</div>
                )}
              </div>
            </div>
          </div>
          
          {/* Section des compétences */}
          <div className="space-y-4">
            <h3 className="text-lg font-medium">Compétences</h3>
            <div className="flex flex-wrap gap-2">
              {candidate.skills.map((skill: Skill, index: number) => (
                <Badge 
                  key={index} 
                  variant="secondary"
                  className="px-3 py-1 text-sm"
                >
                  {skill.name} {skill.level && `(${skill.level})`}
                  {isEditing && (
                    <X 
                      className="ml-2 h-3 w-3 cursor-pointer" 
                      onClick={() => {
                        setCandidate(prev => ({
                          ...prev,
                          skills: prev.skills.filter((_, i) => i !== index)
                        }));
                      }}
                    />
                  )}
                </Badge>
              ))}
            </div>
          </div>
          
          {/* Section de l'expérience professionnelle */}
          <div className="space-y-4">
            <h3 className="text-lg font-medium">Expérience professionnelle</h3>
            <div className="space-y-4">
              {candidate.experience.map((exp: Experience, index: number) => (
                <div key={index} className="p-4 border rounded-md">
                  {isEditing ? (
                    <div className="space-y-2">
                      <Input
                        value={exp.role}
                        onChange={(e) => {
                          const updatedExperiences = [...candidate.experience];
                          updatedExperiences[index] = { ...exp, role: e.target.value };
                          setCandidate(prev => ({
                            ...prev,
                            experience: updatedExperiences
                          }));
                        }}
                        className="font-medium"
                        placeholder="Poste"
                      />
                      <div className="flex space-x-2">
                        <Input
                          value={exp.company}
                          onChange={(e) => {
                            const updatedExperiences = [...candidate.experience];
                            updatedExperiences[index] = { ...exp, company: e.target.value };
                            setCandidate(prev => ({
                              ...prev,
                              experience: updatedExperiences
                            }));
                          }}
                          placeholder="Entreprise"
                        />
                        <Input
                          value={exp.period}
                          onChange={(e) => {
                            const updatedExperiences = [...candidate.experience];
                            updatedExperiences[index] = { ...exp, period: e.target.value };
                            setCandidate(prev => ({
                              ...prev,
                              experience: updatedExperiences
                            }));
                          }}
                          placeholder="Période"
                        />
                      </div>
                      <Textarea
                        value={exp.description || ''}
                        onChange={(e) => {
                          const updatedExperiences = [...candidate.experience];
                          updatedExperiences[index] = { ...exp, description: e.target.value };
                          setCandidate(prev => ({
                            ...prev,
                            experience: updatedExperiences
                          }));
                        }}
                        placeholder="Description"
                      />
                    </div>
                  ) : (
                    <>
                      <h4 className="font-medium">{exp.role}</h4>
                      <div className="text-sm text-muted-foreground">
                        {exp.company} • {exp.period}
                      </div>
                      {exp.description && (
                        <p className="mt-2 text-sm">{exp.description}</p>
                      )}
                    </>
                  )}
                </div>
              ))}
            </div>
          </div>
          
          {/* Section de l'éducation */}
          <div className="space-y-4">
            <h3 className="text-lg font-medium">Formation</h3>
            <div className="space-y-4">
              {candidate.education.map((edu: Education, index: number) => (
                <div key={index} className="p-4 border rounded-md">
                  {isEditing ? (
                    <div className="space-y-2">
                      <Input
                        value={edu.degree}
                        onChange={(e) => {
                          const updatedEducation = [...candidate.education];
                          updatedEducation[index] = { ...edu, degree: e.target.value };
                          setCandidate(prev => ({
                            ...prev,
                            education: updatedEducation
                          }));
                        }}
                        className="font-medium"
                        placeholder="Diplôme"
                      />
                      <div className="flex space-x-2">
                        <Input
                          value={edu.institution}
                          onChange={(e) => {
                            const updatedEducation = [...candidate.education];
                            updatedEducation[index] = { ...edu, institution: e.target.value };
                            setCandidate(prev => ({
                              ...prev,
                              education: updatedEducation
                            }));
                          }}
                          placeholder="Institution"
                        />
                        <Input
                          value={edu.period}
                          onChange={(e) => {
                            const updatedEducation = [...candidate.education];
                            updatedEducation[index] = { ...edu, period: e.target.value };
                            setCandidate(prev => ({
                              ...prev,
                              education: updatedEducation
                            }));
                          }}
                          placeholder="Période"
                        />
                      </div>
                    </div>
                  ) : (
                    <>
                      <h4 className="font-medium">{edu.degree}</h4>
                      <div className="text-sm text-muted-foreground">
                        {edu.institution} • {edu.period}
                      </div>
                    </>
                  )}
                </div>
              ))}
            </div>
          </div>
        </div>
      </CardContent>
      <CardFooter className="flex justify-between">
        <Button 
          variant="outline" 
          onClick={onCancel}
          disabled={creating}
        >
          Annuler
        </Button>
        <Button 
          onClick={handleCreateConsultant}
          disabled={creating}
        >
          {creating ? (
            <>
              <Loader2 className="mr-2 h-4 w-4 animate-spin" />
              Création en cours...
            </>
          ) : (
            'Créer le profil consultant'
          )}
        </Button>
      </CardFooter>
    </Card>
  );
};

export default ConsultantPreview;