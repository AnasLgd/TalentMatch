/**
 * Types pour la fonctionnalité des appels d'offres
 * Organisation selon la structure spécifiée
 */

import { Skill } from "../../consultants/types";

export enum TenderStatus {
  DRAFT = "draft",
  OPEN = "open",
  IN_PROGRESS = "in_progress",
  CLOSED = "closed",
  CANCELLED = "cancelled"
}

export interface TenderSkillRequirement {
  skill_id: number;
  skill: Skill;
  is_required: boolean;
  minimum_years: number;
  importance: number;
}

export interface Tender {
  id: number;
  title: string;
  description: string;
  company_id: number;
  company_name?: string;
  start_date: string;
  end_date: string;
  location: string;
  remote_allowed: boolean;
  status: TenderStatus;
  budget_min?: number;
  budget_max?: number;
  skills: TenderSkillRequirement[];
  created_at: string;
  updated_at?: string;
}

export interface TenderCreate {
  title: string;
  description: string;
  company_id: number;
  start_date: string;
  end_date: string;
  location: string;
  remote_allowed?: boolean;
  status?: TenderStatus;
  budget_min?: number;
  budget_max?: number;
  skills?: {
    skill_id: number;
    is_required?: boolean;
    minimum_years?: number;
    importance?: number;
  }[];
}

export interface TenderUpdate {
  title?: string;
  description?: string;
  start_date?: string;
  end_date?: string;
  location?: string;
  remote_allowed?: boolean;
  status?: TenderStatus;
  budget_min?: number;
  budget_max?: number;
  skills?: {
    skill_id: number;
    is_required?: boolean;
    minimum_years?: number;
    importance?: number;
  }[];
}

export interface TenderFilters {
  search?: string;
  status?: TenderStatus;
  company_id?: number;
  skills?: number[];
  start_date_after?: string;
  end_date_before?: string;
  budget_min?: number;
  budget_max?: number;
  location?: string;
  remote_allowed?: boolean;
}

export interface TenderDisplay {
  id: number;
  title: string;
  company: string;
  duration: string;
  location: string;
  status: string;
  budget: string;
  keySkills: string[];
  remote: boolean;
  startDate: string;
  endDate: string;
}