
/**
 * Types pour la fonctionnalité d'analyse des CV
 * Organisation selon la structure spécifiée
 */

import { Skill, Experience, Education } from "../../consultants/types";

export type CvFileType = "pdf" | "docx" | "doc";
export type CvFileStatus = "uploaded" | "analyzing" | "analyzed" | "error";

export interface CvFile {
  id: number;
  name: string;
  size: string;
  type: CvFileType;
  status: CvFileStatus;
  progress: number;
  candidate?: {
    name: string;
    email: string;
    phone: string;
    skills: Skill[];
    experience: Experience[];
    education: Education[];
  };
}

export interface CvUploadResponse {
  fileId: number;
  status: CvFileStatus;
  message?: string;
}

export interface CvAnalysisResult {
  fileId: number;
  candidate: {
    name: string;
    email: string;
    phone: string;
    skills: Skill[];
    experience: Experience[];
    education: Education[];
  };
}

export interface CvProcessingError {
  fileId: number;
  message: string;
  code?: string;
}
