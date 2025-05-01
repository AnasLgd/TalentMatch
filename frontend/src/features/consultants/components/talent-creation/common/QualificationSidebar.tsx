/**
 * QualificationSidebar.tsx
 * Orchestrateur des blocs de qualification RH pour le formulaire multi-étapes.
 * Sélectionne dynamiquement le composant de qualification en fonction du step actif.
 * Tous les composants sont situés dans /qualifications et sont découplés du formulaire principal.
 */

import React from "react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { QualificationIdentity } from "../qualifications/QualificationIdentity";
import { QualificationSkills } from "../qualifications/QualificationSkills";
import { QualificationProjects } from "../qualifications/QualificationProjects";
import { QualificationSoftSkills } from "../qualifications/QualificationSoftSkills";
import { QualificationSummary } from "../qualifications/QualificationSummary";
import { UserRound, Star, BriefcaseBusiness, Brain, FileText } from "lucide-react";

interface QualificationSidebarProps {
  currentStep: number;
}

export const QualificationSidebar: React.FC<QualificationSidebarProps> = ({ currentStep }) => {
  // Sélectionner l'icône en fonction de l'étape
  const getStepIcon = () => {
    switch (currentStep) {
      case 0:
        return <UserRound className="h-4 w-4 text-primary" />;
      case 1:
        return <Star className="h-4 w-4 text-primary" />;
      case 2:
        return <BriefcaseBusiness className="h-4 w-4 text-primary" />;
      case 3:
        return <Brain className="h-4 w-4 text-primary" />;
      case 4:
        return <FileText className="h-4 w-4 text-primary" />;
      default:
        return <UserRound className="h-4 w-4 text-primary" />;
    }
  };

  // Obtenir le titre en fonction de l'étape
  const getStepTitle = () => {
    switch (currentStep) {
      case 0:
        return "Qualification Identité";
      case 1:
        return "Qualification Compétences";
      case 2:
        return "Qualification Projets";
      case 3:
        return "Qualification Soft Skills";
      case 4:
        return "Synthèse Qualification";
      default:
        return "Qualification RH";
    }
  };

  // Obtenir la description en fonction de l'étape
  const getStepDescription = () => {
    switch (currentStep) {
      case 0:
        return "Évaluation et notes sur le profil";
      case 1:
        return "Évaluation des compétences techniques";
      case 2:
        return "Qualification des références projets";
      case 3:
        return "Évaluation des soft skills et préférences";
      case 4:
        return "Récapitulatif global de qualification";
      default:
        return "Informations confidentielles à usage interne";
    }
  };

  // Sélection dynamique du composant en fonction de l'étape
  const renderQualificationByStep = () => {
    switch (currentStep) {
      case 0:
        return <QualificationIdentity />;
      case 1:
        return <QualificationSkills />;
      case 2:
        return <QualificationProjects />;
      case 3:
        return <QualificationSoftSkills />;
      case 4:
        return <QualificationSummary />;
      default:
        return <QualificationIdentity />;
    }
  };

  return (
    <Card className="rounded-2xl shadow-sm bg-white/95 border border-gray-200 backdrop-blur-sm h-full">
      <CardHeader className="pb-3 border-b">
        <CardTitle className="text-base flex items-center gap-2">
          {getStepIcon()}
          {getStepTitle()}
        </CardTitle>
        <CardDescription className="text-xs">
          {getStepDescription()}
        </CardDescription>
      </CardHeader>
      <CardContent className="p-6 overflow-auto">
        {renderQualificationByStep()}
      </CardContent>
    </Card>
  );
};