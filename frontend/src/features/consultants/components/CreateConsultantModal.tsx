import React, { useState, useEffect } from "react";
import axios from "axios";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { ConsultantForm } from "./ConsultantForm";
import { 
  Select, 
  SelectContent, 
  SelectItem, 
  SelectTrigger, 
  SelectValue 
} from "@/components/ui/select";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { toast } from "@/hooks/use-toast";

interface User {
  id: number;
  email: string;
  first_name: string;
  last_name: string;
}

interface CreateConsultantModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSuccess: () => void;
  companyId: number;
}

export const CreateConsultantModal: React.FC<CreateConsultantModalProps> = ({
  isOpen,
  onClose,
  onSuccess,
  companyId,
}) => {
  const [loading, setLoading] = useState(false);
  
  // Selon l'US1.1, le manager d'ESN crée directement un consultant
  // sans vérifier si l'utilisateur existe déjà, donc on va directement
  // au formulaire de création
  
  // Ne pas utiliser d'ID utilisateur pour permettre la création de consultants sans conflit
  // Les utilisateurs pourront être associés ultérieurement
  const defaultUserId = null; // Aucun ID utilisateur pour éviter les conflits

  useEffect(() => {
    if (isOpen) {
      setLoading(false);
    }
  }, [isOpen]);

  // Fonction pour gérer la fermeture du modal et le rappel de succès
  const handleSuccess = () => {
    onSuccess();
    onClose();
  };

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="sm:max-w-[700px]">
        <DialogHeader>
          <DialogTitle>Créer un nouveau consultant</DialogTitle>
          <DialogDescription>
            Remplissez le formulaire pour créer un nouveau profil consultant. Les champs marqués d'un astérisque (*) sont obligatoires.
          </DialogDescription>
        </DialogHeader>
        
        <ConsultantForm
          onCancel={onClose}
          onSuccess={handleSuccess}
          userId={defaultUserId}
          companyId={companyId}
        />
      </DialogContent>
    </Dialog>
  );
};