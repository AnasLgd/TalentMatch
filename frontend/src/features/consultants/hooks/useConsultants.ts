/**
 * Hook React pour la gestion des consultants
 * Utilise React Query pour la gestion des états et du cache
 */

import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { consultantService } from '../services/consultant-service';
import { ConsultantFilters, ConsultantCreate, ConsultantUpdate, ConsultantDisplay } from '../types';
import { toast } from '@/hooks/use-toast';

export function useConsultants(filters?: ConsultantFilters) {
  const queryClient = useQueryClient();
  
  // Clé de requête qui inclut les filtres
  const queryKey = ['consultants', filters];
  
  // Requête pour récupérer les consultants
  const consultantsQuery = useQuery({
    queryKey,
    queryFn: () => consultantService.getConsultants(filters),
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
  
  // Mutation pour créer un consultant
  const createConsultantMutation = useMutation({
    mutationFn: (newConsultant: ConsultantCreate) => 
      consultantService.createConsultant(newConsultant),
    onSuccess: () => {
      // Invalider la requête des consultants pour forcer un rechargement
      queryClient.invalidateQueries({ queryKey: ['consultants'] });
      toast({
        title: 'Consultant créé',
        description: 'Le consultant a été créé avec succès',
        variant: 'default',
      });
    },
    onError: (error) => {
      toast({
        title: 'Erreur',
        description: `Erreur lors de la création du consultant: ${error}`,
        variant: 'destructive',
      });
    },
  });
  
  // Mutation pour mettre à jour un consultant
  const updateConsultantMutation = useMutation({
    mutationFn: ({ id, data }: { id: number; data: ConsultantUpdate }) => 
      consultantService.updateConsultant(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['consultants'] });
      toast({
        title: 'Consultant mis à jour',
        description: 'Le consultant a été mis à jour avec succès',
        variant: 'default',
      });
    },
    onError: (error) => {
      toast({
        title: 'Erreur',
        description: `Erreur lors de la mise à jour du consultant: ${error}`,
        variant: 'destructive',
      });
    },
  });
  
  // Mutation pour supprimer un consultant
  const deleteConsultantMutation = useMutation({
    mutationFn: (id: number) => consultantService.deleteConsultant(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['consultants'] });
      toast({
        title: 'Consultant supprimé',
        description: 'Le consultant a été supprimé avec succès',
        variant: 'default',
      });
    },
    onError: (error) => {
      toast({
        title: 'Erreur',
        description: `Erreur lors de la suppression du consultant: ${error}`,
        variant: 'destructive',
      });
    },
  });
  
  // Hook pour récupérer un consultant spécifique
  const useConsultant = (id: number) => {
    return useQuery({
      queryKey: ['consultant', id],
      queryFn: () => consultantService.getConsultantById(id),
      staleTime: 5 * 60 * 1000, // 5 minutes
    });
  };
  
  return {
    // Données et états pour la liste des consultants
    consultants: consultantsQuery.data || [],
    isLoading: consultantsQuery.isLoading,
    isError: consultantsQuery.isError,
    error: consultantsQuery.error,
    
    // Fonctions de mutation
    createConsultant: createConsultantMutation.mutate,
    isCreating: createConsultantMutation.isPending,
    
    updateConsultant: updateConsultantMutation.mutate,
    isUpdating: updateConsultantMutation.isPending,
    
    deleteConsultant: deleteConsultantMutation.mutate,
    isDeleting: deleteConsultantMutation.isPending,
    
    // Hook pour un consultant spécifique
    useConsultant,
    
    // Fonction de rafraîchissement manuel
    refetch: consultantsQuery.refetch,
  };
}
