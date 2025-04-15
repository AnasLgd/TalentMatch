import React from "react";
import { AlertCircle, ServerCrash, Clock } from "lucide-react";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";

export enum ErrorType {
  UNEXPECTED = "UNEXPECTED",
  SERVICE_UNAVAILABLE = "SERVICE_UNAVAILABLE",
  MAINTENANCE = "MAINTENANCE",
  VALIDATION = "VALIDATION",
  NETWORK = "NETWORK"
}

interface ErrorDetailMap {
  title: string;
  description: string;
  icon: React.ReactNode;
}

const defaultErrorMessages: Record<ErrorType, ErrorDetailMap> = {
  [ErrorType.UNEXPECTED]: {
    title: "Erreur inattendue",
    description: "Une erreur inattendue est survenue. Veuillez réessayer.",
    icon: <AlertCircle className="h-5 w-5" />,
  },
  [ErrorType.SERVICE_UNAVAILABLE]: {
    title: "Service indisponible",
    description: "Service temporairement indisponible. Merci de réessayer.",
    icon: <ServerCrash className="h-5 w-5" />,
  },
  [ErrorType.MAINTENANCE]: {
    title: "Maintenance en cours",
    description: "Le service est en maintenance. Veuillez patienter.",
    icon: <Clock className="h-5 w-5" />,
  },
  [ErrorType.VALIDATION]: {
    title: "Erreur de validation",
    description: "Veuillez vérifier les données saisies et réessayer.",
    icon: <AlertCircle className="h-5 w-5" />,
  },
  [ErrorType.NETWORK]: {
    title: "Erreur réseau",
    description: "Problème de connexion. Vérifiez votre connexion et réessayez.",
    icon: <ServerCrash className="h-5 w-5" />,
  },
};

interface GlobalErrorProps {
  type: ErrorType;
  title?: string;
  description?: string;
  className?: string;
}

export const GlobalError: React.FC<GlobalErrorProps> = ({
  type,
  title,
  description,
  className = "",
}) => {
  const errorDetails = defaultErrorMessages[type];

  return (
    <Alert variant="destructive" className={`mb-4 ${className}`}>
      <div className="flex items-start">
        <div className="mr-2 mt-0.5 text-red-500">{errorDetails.icon}</div>
        <div>
          <AlertTitle>{title || errorDetails.title}</AlertTitle>
          <AlertDescription>
            {description || errorDetails.description}
          </AlertDescription>
        </div>
      </div>
    </Alert>
  );
};

/**
 * Fonction utilitaire pour mapper les codes HTTP aux types d'erreur
 * @param statusCode Le code HTTP de l'erreur
 * @returns Le type d'erreur correspondant
 */
export const mapHttpStatusToErrorType = (statusCode: number): ErrorType => {
  switch (statusCode) {
    case 500:
      return ErrorType.UNEXPECTED;
    case 502:
      return ErrorType.SERVICE_UNAVAILABLE;
    case 503:
      return ErrorType.MAINTENANCE;
    case 400:
    case 422:
      return ErrorType.VALIDATION;
    default:
      return ErrorType.UNEXPECTED;
  }
};