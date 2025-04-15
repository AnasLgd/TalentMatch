/**
 * Gestionnaire d'erreurs centralisé pour les requêtes API
 * Implémente les exigences du critère FF-US1.1.4
 */

import { ErrorType, mapHttpStatusToErrorType } from "@/components/common/GlobalError";

/**
 * Interface pour les erreurs API
 */
export interface ApiError extends Error {
  statusCode?: number;
  errorType: ErrorType;
  originalError?: unknown;
}

/**
 * Crée une erreur API enrichie à partir d'une erreur de requête
 * @param error L'erreur d'origine
 * @returns Une erreur API avec des informations supplémentaires
 */
export function createApiError(error: unknown): ApiError {
  // Récupérer le status code si disponible
  let statusCode = 500;
  if (error instanceof Response) {
    statusCode = error.status;
  } else if (error instanceof Error && "status" in error) {
    // Create a type for errors with status property
    interface ErrorWithStatus {
      status: number;
    }
    
    statusCode = ((error as unknown) as ErrorWithStatus).status;
  }

  // Mapper le code HTTP au type d'erreur
  const errorType = mapHttpStatusToErrorType(statusCode);

  // Générer un message approprié selon le type d'erreur
  let message = 'Une erreur inattendue est survenue.';
  switch (errorType) {
    case ErrorType.SERVICE_UNAVAILABLE:
      message = 'Service temporairement indisponible. Merci de réessayer.';
      break;
    case ErrorType.MAINTENANCE:
      message = 'Le service est en maintenance. Veuillez patienter.';
      break;
    case ErrorType.VALIDATION:
      message = 'Veuillez vérifier les données saisies et réessayer.';
      break;
    case ErrorType.NETWORK:
      message = 'Problème de connexion. Vérifiez votre connexion et réessayez.';
      break;
  }

  // Créer l'erreur enrichie
  const apiError: ApiError = new Error(message) as ApiError;
  apiError.name = 'ApiError';
  apiError.statusCode = statusCode;
  apiError.errorType = errorType;
  apiError.originalError = error;
  
  // Ajouter la journalisation des erreurs 
  logError(apiError);
  
  return apiError;
}

/**
 * Journalise les erreurs API, peut être configuré pour envoyer à un service externe
 * comme Sentry dans un environnement de production
 */
function logError(error: ApiError): void {
  // Journalisation console (pour développement)
  console.error('[API Error]', {
    message: error.message,
    statusCode: error.statusCode,
    errorType: error.errorType,
    stack: error.stack
  });
  
  // En production, on pourrait envoyer à Sentry, NewRelic, etc.
  if (import.meta.env.MODE === 'production') {
    // Implémentation fictive pour l'envoi à Sentry
    /* 
    Sentry.captureException(error, {
      level: 'error',
      tags: {
        statusCode: error.statusCode,
        errorType: error.errorType
      }
    });
    */
  }
}