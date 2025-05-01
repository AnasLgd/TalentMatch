import React from "react";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { TalentMultiStepForm } from "../form/TalentMultiStepForm";
import { CvAnalysisResult } from "@/features/cv-processing/types";

interface TalentCreationModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSuccess: (consultantId: number) => void;
  companyId: number;
  cvAnalysisResult?: CvAnalysisResult;
}

export const TalentCreationModal: React.FC<TalentCreationModalProps> = ({
  isOpen,
  onClose,
  onSuccess,
  companyId,
  cvAnalysisResult,
}) => {
  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="max-w-4xl max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle>
            {cvAnalysisResult 
              ? "Créer un talent à partir du CV" 
              : "Créer un nouveau talent"}
          </DialogTitle>
          <DialogDescription>
            {cvAnalysisResult 
              ? "Les informations extraites du CV ont été pré-remplies. Complétez le formulaire et qualifiez le profil."
              : "Remplissez le formulaire pour créer un nouveau profil talent. Les champs marqués d'un astérisque (*) sont obligatoires."}
          </DialogDescription>
        </DialogHeader>
        
        <TalentMultiStepForm 
          cvAnalysisResult={cvAnalysisResult}
          companyId={companyId}
          onSuccess={onSuccess}
          onCancel={onClose}
        />
      </DialogContent>
    </Dialog>
  );
};