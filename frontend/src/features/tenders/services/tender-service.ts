/**
 * Service pour la gestion des appels d'offres
 * Organisation selon la structure spécifiée
 */

import apiClient from "@/lib/api/api-client";
import { 
  Tender, 
  TenderFilters, 
  TenderCreate, 
  TenderUpdate, 
  TenderDisplay,
  TenderStatus 
} from "../types";

// Fonction utilitaire pour mapper la réponse du backend vers le format d'affichage
const mapToTenderDisplay = (tender: Tender): TenderDisplay => {
  // Formatage des dates
  const startDate = new Date(tender.start_date);
  const endDate = new Date(tender.end_date);
  
  // Extraction des compétences clés (les plus importantes ou requises)
  const keySkills = tender.skills
    .filter(skillReq => skillReq.is_required || skillReq.importance >= 5)
    .map(skillReq => skillReq.skill.name)
    .slice(0, 5); // Limiter à 5 compétences clés pour l'affichage
  
  // Formatage du budget
  let budget = "Non spécifié";
  if (tender.budget_min && tender.budget_max) {
    budget = `${tender.budget_min.toLocaleString('fr-FR')}€ - ${tender.budget_max.toLocaleString('fr-FR')}€`;
  } else if (tender.budget_min) {
    budget = `Min. ${tender.budget_min.toLocaleString('fr-FR')}€`;
  } else if (tender.budget_max) {
    budget = `Max. ${tender.budget_max.toLocaleString('fr-FR')}€`;
  }

  // Formatage de la durée (sans utiliser date-fns)
  const formatDate = (date: Date) => {
    return date.toLocaleDateString('fr-FR', {
      day: '2-digit',
      month: 'short',
      year: 'numeric'
    });
  };
  
  return {
    id: tender.id,
    title: tender.title,
    company: tender.company_name || "Entreprise inconnue",
    duration: `${formatDate(startDate)} - ${formatDate(endDate)}`,
    location: tender.location,
    status: mapTenderStatusToDisplay(tender.status),
    budget: budget,
    keySkills: keySkills,
    remote: tender.remote_allowed,
    startDate: startDate.toISOString().split('T')[0], // format YYYY-MM-DD
    endDate: endDate.toISOString().split('T')[0] // format YYYY-MM-DD
  };
};

// Fonction utilitaire pour traduire le statut en français pour l'affichage
const mapTenderStatusToDisplay = (status: TenderStatus): string => {
  switch (status) {
    case TenderStatus.DRAFT:
      return "Brouillon";
    case TenderStatus.OPEN:
      return "Ouvert";
    case TenderStatus.IN_PROGRESS:
      return "En cours";
    case TenderStatus.CLOSED:
      return "Fermé";
    case TenderStatus.CANCELLED:
      return "Annulé";
    default:
      return "Statut inconnu";
  }
};

// Construction des paramètres de requête pour les filtres
const buildQueryParams = (filters?: TenderFilters): URLSearchParams => {
  const params = new URLSearchParams();
  
  if (filters) {
    if (filters.search) {
      params.append('search', filters.search);
    }
    if (filters.status) {
      params.append('status', filters.status);
    }
    if (filters.company_id) {
      params.append('company_id', filters.company_id.toString());
    }
    if (filters.skills && filters.skills.length > 0) {
      filters.skills.forEach(skillId => params.append('skills', skillId.toString()));
    }
    if (filters.start_date_after) {
      params.append('start_date_after', filters.start_date_after);
    }
    if (filters.end_date_before) {
      params.append('end_date_before', filters.end_date_before);
    }
    if (filters.budget_min !== undefined) {
      params.append('budget_min', filters.budget_min.toString());
    }
    if (filters.budget_max !== undefined) {
      params.append('budget_max', filters.budget_max.toString());
    }
    if (filters.location) {
      params.append('location', filters.location);
    }
    if (filters.remote_allowed !== undefined) {
      params.append('remote_allowed', filters.remote_allowed.toString());
    }
  }
  
  return params;
};

export const tenderService = {
  /**
   * Récupère la liste des appels d'offres avec filtres optionnels
   */
  async getTenders(filters?: TenderFilters): Promise<TenderDisplay[]> {
    const queryParams = buildQueryParams(filters);
    const endpoint = `/v1/tenders?${queryParams.toString()}`;
    
    try {
      const response = await apiClient.get<Tender[]>(endpoint);
      return response.map(mapToTenderDisplay);
    } catch (error) {
      console.error("Erreur lors de la récupération des appels d'offres:", error);
      throw error;
    }
  },

  /**
   * Récupère un appel d'offres par son ID
   */
  async getTenderById(id: number): Promise<TenderDisplay | null> {
    try {
      const tender = await apiClient.get<Tender>(`/v1/tenders/${id}`);
      return mapToTenderDisplay(tender);
    } catch (error) {
      console.error(`Erreur lors de la récupération de l'appel d'offres ID ${id}:`, error);
      return null;
    }
  },

  /**
   * Récupère les données brutes d'un appel d'offres (sans mapping pour l'affichage)
   */
  async getTenderRawData(id: number): Promise<Tender | null> {
    try {
      return await apiClient.get<Tender>(`/v1/tenders/${id}`);
    } catch (error) {
      console.error(`Erreur lors de la récupération des données brutes de l'appel d'offres ID ${id}:`, error);
      return null;
    }
  },

  /**
   * Crée un nouvel appel d'offres
   */
  async createTender(tender: TenderCreate): Promise<TenderDisplay> {
    try {
      const newTender = await apiClient.post<Tender>('/v1/tenders', tender);
      return mapToTenderDisplay(newTender);
    } catch (error) {
      console.error("Erreur lors de la création de l'appel d'offres:", error);
      throw error;
    }
  },

  /**
   * Met à jour un appel d'offres existant
   */
  async updateTender(id: number, tender: TenderUpdate): Promise<TenderDisplay> {
    try {
      const updatedTender = await apiClient.put<Tender>(`/v1/tenders/${id}`, tender);
      return mapToTenderDisplay(updatedTender);
    } catch (error) {
      console.error(`Erreur lors de la mise à jour de l'appel d'offres ID ${id}:`, error);
      throw error;
    }
  },

  /**
   * Change le statut d'un appel d'offres
   */
  async updateTenderStatus(id: number, status: TenderStatus): Promise<TenderDisplay> {
    try {
      const updatedTender = await apiClient.patch<Tender>(`/v1/tenders/${id}/status`, { status });
      return mapToTenderDisplay(updatedTender);
    } catch (error) {
      console.error(`Erreur lors de la mise à jour du statut de l'appel d'offres ID ${id}:`, error);
      throw error;
    }
  },

  /**
   * Supprime un appel d'offres
   */
  async deleteTender(id: number): Promise<void> {
    try {
      await apiClient.delete<void>(`/v1/tenders/${id}`);
    } catch (error) {
      console.error(`Erreur lors de la suppression de l'appel d'offres ID ${id}:`, error);
      throw error;
    }
  }
};