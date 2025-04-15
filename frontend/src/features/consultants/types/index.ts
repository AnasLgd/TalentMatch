/**
 * Types pour la fonctionnalité des consultants
 * Organisation selon la structure spécifiée
 */

export enum AvailabilityStatus {
  AVAILABLE = "AVAILABLE",
  PARTIALLY_AVAILABLE = "PARTIALLY_AVAILABLE",
  UNAVAILABLE = "UNAVAILABLE",
  ON_MISSION = "ON_MISSION"
}

export interface Skill {
  id?: number;
  name: string;
  level?: string; // Non présent dans le backend, à stocker dans les métadonnées
  years?: number; // Non présent dans le backend, à stocker dans les métadonnées
  category?: string;
  description?: string;
}

export interface Experience {
  id?: number;
  role: string;
  company: string;
  period: string;
  description?: string;
}

export interface Education {
  id?: number;
  degree: string;
  institution: string;
  period: string;
}

export interface User {
  id: number;
  email: string;
  full_name: string;
  role?: string;
}

export interface Consultant {
  id: number;
  user_id: number;
  company_id: number;
  title: string;
  experience_years?: number;
  availability_status: AvailabilityStatus;
  availability_date?: string;
  hourly_rate?: number;
  daily_rate?: number;
  bio?: string;
  location?: string;
  remote_work?: boolean;
  max_travel_distance?: number;
  user: User;
  skills: Skill[];
  created_at: string;
  updated_at?: string;
}

// Pour la compatibilité avec l'interface existante
export interface ConsultantDisplay {
  id: number;
  name: string;
  role: string;
  experience: string;
  skills: Skill[];
  status: string;
  email?: string;
  phone?: string;
  experiences?: Experience[];
  education?: Education[];
  availabilityDate?: string;
  photo?: string;
}

export interface ConsultantCreate {
  user_id?: number; // Rendu optionnel pour permettre la création de consultants sans utilisateur associé
  company_id: number;
  title: string;
  experience_years?: number;
  availability_status?: AvailabilityStatus;
  availability_date?: string;
  hourly_rate?: number;
  daily_rate?: number;
  bio?: string;
  location?: string;
  remote_work?: boolean;
  max_travel_distance?: number;
  skills?: Skill[];
  photo_url?: string; // URL de la photo de profil
  first_name?: string; // Prénom de l'utilisateur à mettre à jour
  last_name?: string; // Nom de l'utilisateur à mettre à jour
}

export interface ConsultantUpdate {
  title?: string;
  experience_years?: number;
  availability_status?: AvailabilityStatus;
  availability_date?: string;
  hourly_rate?: number;
  daily_rate?: number;
  bio?: string;
  location?: string;
  remote_work?: boolean;
  max_travel_distance?: number;
  skills?: Skill[];
}

export interface ConsultantFilters {
  search?: string;
  status?: AvailabilityStatus;
  skills?: string[];
  experience_years?: number;
}
