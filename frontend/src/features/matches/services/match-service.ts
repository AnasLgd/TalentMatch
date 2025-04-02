/**
 * Service pour la gestion des mises en relation (matches)
 * Organisation selon la structure spécifiée
 */

import apiClient from "@/lib/api/api-client";
import { 
  Match, 
  MatchFilters, 
  MatchCreate, 
  MatchUpdate, 
  MatchDisplay,
  MatchStatus 
} from "../types";

// Fonction utilitaire pour mapper la réponse du backend vers le format d'affichage
const mapToMatchDisplay = (match: Match): MatchDisplay => {
  return {
    id: match.id,
    consultant: {
      id: match.consultant_id,
      name: match.consultant?.user?.full_name || "Consultant inconnu",
      role: match.consultant?.title || "Rôle non spécifié"
    },
    tender: {
      id: match.tender_id,
      title: match.tender?.title || "Appel d'offres inconnu",
      company: match.tender?.company_name || "Entreprise inconnue"
    },
    score: match.score,
    status: mapMatchStatusToDisplay(match.status),
    createdAt: new Date(match.created_at).toLocaleDateString('fr-FR')
  };
};

// Fonction utilitaire pour traduire le statut en français pour l'affichage
const mapMatchStatusToDisplay = (status: MatchStatus): string => {
  switch (status) {
    case MatchStatus.PENDING:
      return "En attente";
    case MatchStatus.PROPOSED:
      return "Proposé";
    case MatchStatus.ACCEPTED:
      return "Accepté";
    case MatchStatus.REJECTED:
      return "Refusé";
    case MatchStatus.CANCELLED:
      return "Annulé";
    default:
      return "Statut inconnu";
  }
};

// Construction des paramètres de requête pour les filtres
const buildQueryParams = (filters?: MatchFilters): URLSearchParams => {
  const params = new URLSearchParams();
  
  if (filters) {
    if (filters.consultant_id) {
      params.append('consultant_id', filters.consultant_id.toString());
    }
    if (filters.tender_id) {
      params.append('tender_id', filters.tender_id.toString());
    }
    if (filters.status) {
      params.append('status', filters.status);
    }
    if (filters.min_score !== undefined) {
      params.append('min_score', filters.min_score.toString());
    }
    if (filters.created_after) {
      params.append('created_after', filters.created_after);
    }
    if (filters.created_before) {
      params.append('created_before', filters.created_before);
    }
  }
  
  return params;
};

export const matchService = {
  /**
   * Récupère la liste des matches avec filtres optionnels
   */
  async getMatches(filters?: MatchFilters): Promise<MatchDisplay[]> {
    const queryParams = buildQueryParams(filters);
    const endpoint = `/v1/matches?${queryParams.toString()}`;
    
    try {
      const response = await apiClient.get<Match[]>(endpoint);
      return response.map(mapToMatchDisplay);
    } catch (error) {
      console.error("Erreur lors de la récupération des matches:", error);
      throw error;
    }
  },

  /**
   * Récupère un match par son ID
   */
  async getMatchById(id: number): Promise<MatchDisplay | null> {
    try {
      const match = await apiClient.get<Match>(`/v1/matches/${id}`);
      return mapToMatchDisplay(match);
    } catch (error) {
      console.error(`Erreur lors de la récupération du match ID ${id}:`, error);
      return null;
    }
  },

  /**
   * Récupère les données brutes d'un match (sans mapping pour l'affichage)
   */
  async getMatchRawData(id: number): Promise<Match | null> {
    try {
      return await apiClient.get<Match>(`/v1/matches/${id}`);
    } catch (error) {
      console.error(`Erreur lors de la récupération des données brutes du match ID ${id}:`, error);
      return null;
    }
  },

  /**
   * Récupère les matches par consultant
   */
  async getMatchesByConsultant(consultantId: number): Promise<MatchDisplay[]> {
    return this.getMatches({ consultant_id: consultantId });
  },

  /**
   * Récupère les matches par appel d'offres
   */
  async getMatchesByTender(tenderId: number): Promise<MatchDisplay[]> {
    return this.getMatches({ tender_id: tenderId });
  },

  /**
   * Crée un nouveau match
   */
  async createMatch(match: MatchCreate): Promise<MatchDisplay> {
    try {
      const newMatch = await apiClient.post<Match>('/v1/matches', match);
      return mapToMatchDisplay(newMatch);
    } catch (error) {
      console.error("Erreur lors de la création du match:", error);
      throw error;
    }
  },

  /**
   * Met à jour un match existant
   */
  async updateMatch(id: number, match: MatchUpdate): Promise<MatchDisplay> {
    try {
      const updatedMatch = await apiClient.put<Match>(`/v1/matches/${id}`, match);
      return mapToMatchDisplay(updatedMatch);
    } catch (error) {
      console.error(`Erreur lors de la mise à jour du match ID ${id}:`, error);
      throw error;
    }
  },

  /**
   * Met à jour le statut d'un match
   */
  async updateMatchStatus(id: number, status: MatchStatus): Promise<MatchDisplay> {
    return this.updateMatch(id, { status });
  },

  /**
   * Supprime un match
   */
  async deleteMatch(id: number): Promise<void> {
    try {
      await apiClient.delete<void>(`/v1/matches/${id}`);
    } catch (error) {
      console.error(`Erreur lors de la suppression du match ID ${id}:`, error);
      throw error;
    }
  },
  
  /**
   * Lance un calcul automatique de match entre consultants et appels d'offres
   */
  async calculateMatches(consultantId?: number, tenderId?: number): Promise<MatchDisplay[]> {
    try {
      const params = new URLSearchParams();
      if (consultantId) {
        params.append('consultant_id', consultantId.toString());
      }
      if (tenderId) {
        params.append('tender_id', tenderId.toString());
      }
      
      const endpoint = `/v1/matches/calculate?${params.toString()}`;
      const response = await apiClient.post<Match[]>(endpoint, {});
      return response.map(mapToMatchDisplay);
    } catch (error) {
      console.error("Erreur lors du calcul des matches:", error);
      throw error;
    }
  }
};