/**
 * Service pour la gestion de l'analyse des CV
 * Organisation selon la structure spécifiée
 */

import apiClient from "@/lib/api/api-client";
import { CvFile, CvUploadResponse, CvAnalysisResult, CvFileStatus } from "../types";

export const cvProcessingService = {
  /**
   * Télécharge un CV pour analyse
   */
  async uploadCv(file: File): Promise<CvUploadResponse> {
    try {
      // Création d'un FormData pour l'upload de fichier
      const formData = new FormData();
      formData.append('file', file);
      
      // Configuration headers spécifiques pour l'upload de fichier
      const headers = {
        'Content-Type': 'multipart/form-data',
      };
      
      // Appel API pour télécharger le fichier
      const response = await apiClient.post<CvUploadResponse>('/v1/cv-analysis/upload', formData, headers);
      return response;
    } catch (error) {
      console.error("Erreur lors du téléchargement du CV:", error);
      throw error;
    }
  },

  /**
   * Récupère la liste des CV téléchargés
   */
  async getCvFiles(): Promise<CvFile[]> {
    try {
      return await apiClient.get<CvFile[]>('/v1/cv-analysis/files');
    } catch (error) {
      console.error("Erreur lors de la récupération des fichiers CV:", error);
      throw error;
    }
  },

  /**
   * Récupère les détails d'un CV spécifique
   */
  async getCvFileById(fileId: number): Promise<CvFile> {
    try {
      return await apiClient.get<CvFile>(`/v1/cv-analysis/files/${fileId}`);
    } catch (error) {
      console.error(`Erreur lors de la récupération du fichier CV ID ${fileId}:`, error);
      throw error;
    }
  },

  /**
   * Lance l'analyse d'un CV préalablement téléchargé
   */
  async analyzeCv(fileId: number): Promise<CvFile> {
    try {
      return await apiClient.post<CvFile>(`/v1/cv-analysis/analyze/${fileId}`, {});
    } catch (error) {
      console.error(`Erreur lors de l'analyse du CV ID ${fileId}:`, error);
      throw error;
    }
  },

  /**
   * Récupère les résultats d'analyse d'un CV
   */
  async getCvAnalysisResult(fileId: number): Promise<CvAnalysisResult> {
    try {
      return await apiClient.get<CvAnalysisResult>(`/v1/cv-analysis/results/${fileId}`);
    } catch (error) {
      console.error(`Erreur lors de la récupération des résultats d'analyse du CV ID ${fileId}:`, error);
      throw error;
    }
  },

  /**
   * Vérifie le statut d'analyse d'un CV
   */
  async checkCvStatus(fileId: number): Promise<CvFileStatus> {
    try {
      const response = await apiClient.get<{ status: CvFileStatus }>(`/v1/cv-analysis/status/${fileId}`);
      return response.status;
    } catch (error) {
      console.error(`Erreur lors de la vérification du statut du CV ID ${fileId}:`, error);
      throw error;
    }
  },

  /**
   * Supprime un fichier CV
   */
  async deleteCvFile(fileId: number): Promise<void> {
    try {
      await apiClient.delete<void>(`/v1/cv-analysis/files/${fileId}`);
    } catch (error) {
      console.error(`Erreur lors de la suppression du fichier CV ID ${fileId}:`, error);
      throw error;
    }
  },

  /**
   * Télécharge et analyse un CV en une seule opération
   */
  async uploadAndAnalyzeCv(file: File): Promise<CvAnalysisResult> {
    try {
      // Création d'un FormData pour l'upload de fichier
      const formData = new FormData();
      formData.append('file', file);
      
      // Configuration headers spécifiques pour l'upload de fichier
      const headers = {
        'Content-Type': 'multipart/form-data',
      };
      
      // Appel API pour télécharger et analyser le fichier en une seule opération
      return await apiClient.post<CvAnalysisResult>('/v1/cv-analysis/upload-analyze', formData, headers);
    } catch (error) {
      console.error("Erreur lors du téléchargement et de l'analyse du CV:", error);
      throw error;
    }
  },

  /**
   * Crée un consultant à partir d'un CV analysé
   */
  async createConsultantFromCv(fileId: number, companyId: number): Promise<number> {
    try {
      const response = await apiClient.post<{ consultant_id: number }>('/v1/cv-analysis/create-consultant', {
        file_id: fileId,
        company_id: companyId
      });
      return response.consultant_id;
    } catch (error) {
      console.error(`Erreur lors de la création d'un consultant à partir du CV ID ${fileId}:`, error);
      throw error;
    }
  }
};