/**
 * Hook React pour la gestion des consultants
 * Utilise React Query pour la gestion des états et du cache
 */

import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { consultantService } from '../services/consultant-service';
import { ConsultantFilters, ConsultantCreate, ConsultantUpdate, ConsultantDisplay } from '../types';
import { toast } from '@/hooks/use-toast';
import { ApiError } from '@/lib/api/error-handler';
import { ErrorType } from '@/components/common/GlobalError';

export function useConsultants(filters?: ConsultantFilters) {
  const queryClient = useQueryClient();
  
  // Clé de requête qui inclut les filtres
  const queryKey = ['consultants', filters];
  
  // Requête pour récupérer les consultants
  const consultantsQuery = useQuery({
    queryKey,
    queryFn: () => {
      console.log('[useConsultants] Démarrage de la requête avec filtres:', filters);
      return consultantService.getConsultants(filters)
        .then(data => {
          console.log('[useConsultants] Données récupérées:', data);
          return data;
        })
        .catch(error => {
          console.error('[useConsultants] Erreur API:', error);
          throw error;
        });
    },
    staleTime: 5 * 60 * 1000, // 5 minutes
    retry: 1 // Limiter le nombre de tentatives pour éviter trop d'appels en cas d'erreur
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
    onError: (error: unknown) => {
      // Gestion spécifique des erreurs selon le type
      const apiError = error as ApiError;
      
      // Message d'erreur spécifique au code HTTP
      let title = 'Erreur';
      let description = 'Une erreur est survenue lors de la création du consultant';
      
      // Utiliser le système d'erreur centralisé pour mapper les erreurs
      if (apiError.errorType) {
        switch (apiError.errorType) {
          case ErrorType.UNEXPECTED:
            title = 'Erreur inattendue';
            description = 'Une erreur inattendue est survenue. Veuillez réessayer.';
            break;
          case ErrorType.SERVICE_UNAVAILABLE:
            title = 'Service indisponible';
            description = 'Service temporairement indisponible. Merci de réessayer.';
            break;
          case ErrorType.MAINTENANCE:
            title = 'Maintenance en cours';
            description = 'Le service est en maintenance. Veuillez patienter.';
            break;
          case ErrorType.VALIDATION:
            title = 'Données invalides';
            description = 'Veuillez vérifier les informations saisies et réessayer.';
            break;
          default:
            // Utiliser les valeurs par défaut
        }
      }
      
      toast({
        title,
        description,
        variant: 'destructive',
      });
      
      // Si nous sommes en développement, afficher l'erreur complète dans la console
      if (import.meta.env.DEV) {
        console.error('[useConsultants] Erreur détaillée:', apiError);
      }
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
      queryFn: () => {
        console.log(`[useConsultant] Récupération du consultant ID: ${id}`);
        return consultantService.getConsultantById(id)
          .then(data => {
            console.log(`[useConsultant] Données du consultant ${id} récupérées:`, data);
            return data;
          })
          .catch(error => {
            console.error(`[useConsultant] Erreur lors de la récupération du consultant ${id}:`, error);
            throw error;
          });
      },
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
