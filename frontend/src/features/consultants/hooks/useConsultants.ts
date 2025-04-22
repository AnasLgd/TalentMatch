import { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { consultantService } from "../services/consultant-service";
import { ConsultantCreate, ConsultantDisplay, ConsultantUpdate, Consultant } from "../types";

export const useConsultants = () => {
  const queryClient = useQueryClient();
  const [isFiltering, setIsFiltering] = useState(false);

  // Récupérer tous les consultants
  const {
    data: consultants,
    isLoading,
    isError,
    error,
    refetch,
  } = useQuery({
    queryKey: ["consultants"],
    queryFn: () => consultantService.getConsultants(),
    staleTime: 5 * 60 * 1000, // 5 minutes
  });

  // Créer un consultant
  const {
    mutate: createConsultant,
    isPending: isCreating,
    error: createError,
  } = useMutation({
    mutationFn: (newConsultant: ConsultantCreate) => consultantService.createConsultant(newConsultant),
    onSuccess: (newConsultant) => {
      // Mise à jour du cache pour ajouter le nouveau consultant
      queryClient.setQueryData(
        ["consultants"],
        (oldData: ConsultantDisplay[] = []) => [...oldData, newConsultant]
      );
      
      // Invalider la requête pour forcer un rechargement et assurer que
      // les données sont à jour avec le backend
      queryClient.invalidateQueries({
        queryKey: ["consultants"]
      });
    },
  });

  // Mise à jour d'un consultant
  const {
    mutate: updateConsultant,
    isPending: isUpdating,
    error: updateError,
  } = useMutation({
    mutationFn: ({ id, consultant }: { id: number; consultant: ConsultantUpdate }) =>
      consultantService.updateConsultant(id, consultant),
    onSuccess: (updatedConsultant) => {
      // Mettre à jour le cache avec le consultant mis à jour
      queryClient.setQueryData(
        ["consultants"],
        (oldData: ConsultantDisplay[] = []) =>
          oldData.map((c) =>
            c.id === updatedConsultant.id ? updatedConsultant : c
          )
      );
      
      // Invalidation du cache pour le consultant spécifique
      queryClient.invalidateQueries({
        queryKey: ["consultant", updatedConsultant.id]
      });
    },
  });

  // Suppression d'un consultant
  const {
    mutate: deleteConsultant,
    isPending: isDeleting,
    error: deleteError,
  } = useMutation({
    mutationFn: (id: number) => consultantService.deleteConsultant(id),
    onSuccess: (_, variables) => {
      // Mettre à jour le cache en supprimant le consultant
      queryClient.setQueryData(
        ["consultants"],
        (oldData: ConsultantDisplay[] = []) =>
          oldData.filter((c) => c.id !== variables)
      );
    },
  });

  return {
    consultants,
    isLoading,
    isError,
    error,
    refetch,
    createConsultant,
    isCreating,
    createError,
    updateConsultant,
    isUpdating,
    updateError,
    deleteConsultant,
    isDeleting,
    deleteError,
    isFiltering,
    setIsFiltering,
  };
};
