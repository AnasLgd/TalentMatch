/**
 * Types pour la fonctionnalité des mises en relation
 * Organisation selon la structure spécifiée
 */

import { Consultant } from "../../consultants/types";
import { Tender } from "../../tenders/types";

export enum MatchStatus {
  PENDING = "pending",
  PROPOSED = "proposed",
  ACCEPTED = "accepted",
  REJECTED = "rejected",
  CANCELLED = "cancelled"
}

export interface Match {
  id: number;
  consultant_id: number;
  tender_id: number;
  score: number;
  status: MatchStatus;
  notes?: string;
  created_at: string;
  updated_at?: string;
  consultant?: Consultant;
  tender?: Tender;
}

export interface MatchCreate {
  consultant_id: number;
  tender_id: number;
  score?: number;
  status?: MatchStatus;
  notes?: string;
}

export interface MatchUpdate {
  score?: number;
  status?: MatchStatus;
  notes?: string;
}

export interface MatchDisplay {
  id: number;
  consultant: {
    id: number;
    name: string;
    role: string;
  };
  tender: {
    id: number;
    title: string;
    company: string;
  };
  score: number;
  status: string;
  createdAt: string;
}

export interface MatchFilters {
  consultant_id?: number;
  tender_id?: number;
  status?: MatchStatus;
  min_score?: number;
  created_after?: string;
  created_before?: string;
}