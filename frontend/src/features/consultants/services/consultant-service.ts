/**
 * Service pour la gestion des consultants
 * Organisation selon la structure spécifiée
 */

import apiClient from "@/lib/api/api-client";
import { 
  Consultant, 
  ConsultantFilters, 
  ConsultantCreate, 
  ConsultantUpdate, 
  ConsultantDisplay,
  AvailabilityStatus 
} from "../types";

// Fonction utilitaire pour mapper la réponse du backend vers le format d'affichage
const mapToConsultantDisplay = (consultant: Consultant): ConsultantDisplay => {
  return {
    id: consultant.id,
    name: consultant.user?.full_name || "Inconnu",
    role: consultant.title,
    experience: consultant.experience_years ? `${consultant.experience_years} ans` : "Non spécifié",
    skills: consultant.skills || [],
    status: mapAvailabilityStatusToDisplay(consultant.availability_status),
    email: consultant.user?.email,
    availabilityDate: consultant.availability_date,
  };
};

// Fonction utilitaire pour traduire le statut en français pour l'affichage
const mapAvailabilityStatusToDisplay = (status: AvailabilityStatus): string => {
  switch (status) {
    case AvailabilityStatus.AVAILABLE:
      return "Disponible";
    case AvailabilityStatus.PARTIALLY_AVAILABLE:
      return "Partiellement disponible";
    case AvailabilityStatus.UNAVAILABLE:
      return "Indisponible";
    case AvailabilityStatus.ON_MISSION:
      return "En mission";
    default:
      return "Statut inconnu";
  }
};

// Construction des paramètres de requête pour les filtres
const buildQueryParams = (filters?: ConsultantFilters): URLSearchParams => {
  const params = new URLSearchParams();
  
  if (filters) {
    if (filters.search) {
      params.append('search', filters.search);
    }
    if (filters.status) {
      params.append('status', filters.status);
    }
    if (filters.skills && filters.skills.length > 0) {
      filters.skills.forEach(skill => params.append('skills', skill));
    }
    if (filters.experience_years !== undefined) {
      params.append('experience_years', filters.experience_years.toString());
    }
  }
  
  return params;
};

export const consultantService = {
  /**
   * Récupère la liste des consultants avec filtres optionnels
   */
  async getConsultants(filters?: ConsultantFilters): Promise<ConsultantDisplay[]> {
    const queryParams = buildQueryParams(filters);
    const endpoint = `/v1/consultants?${queryParams.toString()}`;
    
    try {
      const response = await apiClient.get<Consultant[]>(endpoint);
      return response.map(mapToConsultantDisplay);
    } catch (error) {
      console.error("Erreur lors de la récupération des consultants:", error);
      throw error;
    }
  },

  /**
   * Récupère un consultant par son ID
   */
  async getConsultantById(id: number): Promise<ConsultantDisplay | null> {
    try {
      const consultant = await apiClient.get<Consultant>(`/v1/consultants/${id}`);
      return mapToConsultantDisplay(consultant);
    } catch (error) {
      console.error(`Erreur lors de la récupération du consultant ID ${id}:`, error);
      return null;
    }
  },

  /**
   * Récupère les données brutes d'un consultant (sans mapping pour l'affichage)
   */
  async getConsultantRawData(id: number): Promise<Consultant | null> {
    try {
      return await apiClient.get<Consultant>(`/v1/consultants/${id}`);
    } catch (error) {
      console.error(`Erreur lors de la récupération des données brutes du consultant ID ${id}:`, error);
      return null;
    }
  },

  /**
   * Crée un nouveau consultant
   */
  async createConsultant(consultant: ConsultantCreate): Promise<ConsultantDisplay> {
    try {
      const newConsultant = await apiClient.post<Consultant>('/v1/consultants', consultant);
      return mapToConsultantDisplay(newConsultant);
    } catch (error) {
      console.error("Erreur lors de la création du consultant:", error);
      throw error;
    }
  },

  /**
   * Met à jour un consultant existant
   */
  async updateConsultant(id: number, consultant: ConsultantUpdate): Promise<ConsultantDisplay> {
    try {
      const updatedConsultant = await apiClient.put<Consultant>(`/v1/consultants/${id}`, consultant);
      return mapToConsultantDisplay(updatedConsultant);
    } catch (error) {
      console.error(`Erreur lors de la mise à jour du consultant ID ${id}:`, error);
      throw error;
    }
  },

  /**
   * Supprime un consultant
   */
  async deleteConsultant(id: number): Promise<void> {
    try {
      await apiClient.delete<void>(`/v1/consultants/${id}`);
    } catch (error) {
      console.error(`Erreur lors de la suppression du consultant ID ${id}:`, error);
      throw error;
    }
  }
};
