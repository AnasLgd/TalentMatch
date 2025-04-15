/**
 * Service pour gérer l'upload des fichiers (photos de profil, etc.)
 * Utilise une API REST pour communiquer avec le backend qui gère MinIO
 * Implémente les validations selon FF-US1.1.3
 */

import apiClient from "@/lib/api/api-client";

// Types d'erreurs gérées
export enum UploadErrorType {
  FORMAT_INVALID = "FORMAT_INVALID",
  SIZE_EXCEEDED = "SIZE_EXCEEDED",
  UPLOAD_FAILED = "UPLOAD_FAILED"
}

// Configuration des formats et tailles acceptés
export const UPLOAD_CONFIG = {
  MAX_SIZE_MB: 5,
  ACCEPTED_IMAGE_FORMATS: ['.jpg', '.jpeg', '.png'],
  ACCEPTED_MIME_TYPES: ['image/jpeg', 'image/png']
};

// Interface d'erreur d'upload
export interface UploadError {
  type: UploadErrorType;
  message: string;
}

export const uploadService = {
  /**
   * Valide le format et la taille d'un fichier
   * @param file Le fichier à valider
   * @returns Un objet erreur ou null si tout est valide
   */
  validateFile(file: File): UploadError | null {
    // Vérifier le type MIME
    if (!UPLOAD_CONFIG.ACCEPTED_MIME_TYPES.includes(file.type)) {
      return {
        type: UploadErrorType.FORMAT_INVALID,
        message: `Format d'image non pris en charge. Formats acceptés: ${UPLOAD_CONFIG.ACCEPTED_IMAGE_FORMATS.join(', ')}`
      };
    }

    // Vérifier la taille
    const maxSizeInBytes = UPLOAD_CONFIG.MAX_SIZE_MB * 1024 * 1024;
    if (file.size > maxSizeInBytes) {
      return {
        type: UploadErrorType.SIZE_EXCEEDED,
        message: `Taille d'image trop importante. Maximum: ${UPLOAD_CONFIG.MAX_SIZE_MB}MB`
      };
    }

    return null;
  },

  /**
   * Télécharge un fichier vers le serveur avec validation
   * @param file Le fichier à télécharger
   * @param folder Le dossier de destination (optionnel)
   * @returns L'URL du fichier téléchargé
   * @throws {UploadError} Si le fichier ne respecte pas les contraintes
   */
  async uploadFile(file: File, folder: string = 'profiles'): Promise<string> {
    // Valider le fichier avant l'upload
    const validationError = this.validateFile(file);
    if (validationError) {
      throw validationError;
    }
    
    try {
      // Créer un FormData pour l'upload
      const formData = new FormData();
      formData.append('file', file);
      formData.append('folder', folder);

      // Dans une application réelle, cela appellerait une vraie API d'upload
      const response = await apiClient.post<{ url: string }>('/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      // Retourner l'URL du fichier téléchargé
      return response.url;
    } catch (error) {
      console.error('Erreur lors de l\'upload du fichier:', error);
      throw new Error('Impossible de télécharger le fichier. Veuillez réessayer.');
    }
  },

  /**
   * Supprime un fichier du serveur
   * @param url L'URL du fichier à supprimer
   */
  async deleteFile(url: string): Promise<void> {
    try {
      // Extraire le chemin du fichier de l'URL
      const filePath = url.split('/').slice(-2).join('/');
      await apiClient.delete(`/upload/${encodeURIComponent(filePath)}`);
    } catch (error) {
      console.error('Erreur lors de la suppression du fichier:', error);
      throw new Error('Impossible de supprimer le fichier.');
    }
  }
};