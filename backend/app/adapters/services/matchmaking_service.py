from typing import List, Optional, Dict, Any
import logging
from datetime import date

from app.core.interfaces.matchmaking_service import MatchmakingService
from app.core.interfaces.consultant_repository import ConsultantRepository
from app.core.interfaces.tender_repository import TenderRepository
from app.core.interfaces.match_repository import MatchRepository
from app.core.entities.match import MatchCreate, MatchStatus

class DefaultMatchmakingService:
    """
    Implémentation par défaut du service de matchmaking entre consultants et appels d'offres
    """
    
    def __init__(
        self,
        consultant_repository: ConsultantRepository,
        tender_repository: TenderRepository,
        match_repository: MatchRepository
    ):
        self.consultant_repository = consultant_repository
        self.tender_repository = tender_repository
        self.match_repository = match_repository
        self.logger = logging.getLogger(__name__)
    
    async def calculate_match_score(self, consultant_id: int, tender_id: int) -> float:
        """
        Calcule le score de correspondance entre un consultant et un appel d'offres
        basé sur les compétences, l'expérience, la localisation et la disponibilité
        """
        consultant = await self.consultant_repository.get_by_id(consultant_id)
        tender = await self.tender_repository.get_by_id(tender_id)
        
        if not consultant or not tender:
            return 0.0
        
        # Facteurs de pondération pour chaque critère
        weights = {
            "skills": 0.5,          # 50% pour les compétences
            "experience": 0.2,       # 20% pour l'expérience
            "location": 0.15,        # 15% pour la localisation
            "availability": 0.15     # 15% pour la disponibilité
        }
        
        # Score basé sur les compétences
        skills_score = self._calculate_skills_match(consultant, tender)
        
        # Score basé sur l'expérience
        experience_score = self._calculate_experience_match(consultant, tender)
        
        # Score basé sur la localisation
        location_score = self._calculate_location_match(consultant, tender)
        
        # Score basé sur la disponibilité
        availability_score = self._calculate_availability_match(consultant, tender)
        
        # Score final pondéré
        final_score = (
            skills_score * weights["skills"] +
            experience_score * weights["experience"] +
            location_score * weights["location"] +
            availability_score * weights["availability"]
        )
        
        # Arrondir à 2 décimales
        return round(final_score, 2)
    
    def _calculate_skills_match(self, consultant: Any, tender: Any) -> float:
        """Calcule le score de correspondance des compétences"""
        if not tender.skills or not consultant.skills:
            return 0.0
        
        tender_skills = {skill["skill_id"]: skill for skill in tender.skills}
        consultant_skills = {skill["skill_id"]: skill for skill in consultant.skills}
        
        # Poids selon l'importance des compétences dans l'appel d'offres
        importance_weights = {
            "required": 1.0,
            "preferred": 0.7,
            "nice_to_have": 0.3
        }
        
        total_weight = 0
        matched_weight = 0
        
        for skill_id, tender_skill in tender_skills.items():
            importance = tender_skill.get("importance", "required")
            weight = importance_weights.get(importance, 1.0)
            total_weight += weight
            
            if skill_id in consultant_skills:
                # Vérifier le niveau de compétence du consultant
                consultant_level = consultant_skills[skill_id].get("level", 1)
                # Normaliser le niveau (supposons entre 1 et 5)
                level_factor = min(consultant_level / 5.0, 1.0)
                
                matched_weight += weight * level_factor
        
        if total_weight == 0:
            return 0.0
            
        return matched_weight / total_weight
    
    def _calculate_experience_match(self, consultant: Any, tender: Any) -> float:
        """Calcule le score de correspondance de l'expérience"""
        # Si l'expérience n'est pas spécifiée, on considère un match moyen
        if not consultant.experience_years:
            return 0.5
            
        # On suppose qu'un appel d'offres requiert en moyenne 3 ans d'expérience
        # et qu'un consultant avec 5+ ans est parfaitement qualifié
        required_exp = 3
        ideal_exp = 5
        
        if consultant.experience_years >= ideal_exp:
            return 1.0
        elif consultant.experience_years >= required_exp:
            # Score proportionnel entre le minimum et l'idéal
            return 0.7 + 0.3 * ((consultant.experience_years - required_exp) / (ideal_exp - required_exp))
        else:
            # En dessous du minimum mais peut-être encore considérable
            return max(0.3, 0.7 * (consultant.experience_years / required_exp))
    
    def _calculate_location_match(self, consultant: Any, tender: Any) -> float:
        """Calcule le score de correspondance de la localisation"""
        # Si le travail est à distance, la localisation est moins importante
        if tender.remote_work:
            # Si le consultant accepte le travail à distance, match parfait
            if consultant.remote_work:
                return 1.0
            # Sinon, match partiel
            return 0.3
            
        # Si les localisations sont identiques
        if consultant.location and tender.location and consultant.location.lower() == tender.location.lower():
            return 1.0
            
        # Si le consultant a une distance de déplacement maximum
        if consultant.max_travel_distance:
            # TODO: implémentation plus sophistiquée avec calcul de distance géographique
            # Pour l'instant, on retourne une valeur moyenne
            return 0.5
            
        # Par défaut, match partiel
        return 0.3
    
    def _calculate_availability_match(self, consultant: Any, tender: Any) -> float:
        """Calcule le score de correspondance de la disponibilité"""
        # Si le consultant est indisponible, score nul
        if consultant.availability_status == "unavailable" or consultant.availability_status == "on_mission":
            return 0.0
            
        # Si le consultant est partiellement disponible, vérifier les dates
        if consultant.availability_status == "partially_available" and consultant.availability_date:
            if tender.start_date and consultant.availability_date > tender.start_date:
                # Le consultant sera disponible après le début du projet
                return 0.3
        
        # Si le consultant est disponible, score parfait
        if consultant.availability_status == "available":
            return 1.0
            
        # Par défaut, match moyen
        return 0.7
    
    async def find_matches_for_tender(self, tender_id: int, 
                                     min_score: float = 0.6,
                                     include_partner_consultants: bool = True) -> List[Dict[str, Any]]:
        """
        Trouve les consultants qui correspondent à un appel d'offres
        Inclut les consultants des ESN partenaires si include_partner_consultants est True
        """
        tender = await self.tender_repository.get_by_id(tender_id)
        if not tender:
            return []
            
        # Récupérer tous les consultants (avec filtre selon les partenaires)
        if include_partner_consultants:
            consultants = await self.consultant_repository.get_all()
        else:
            # Seulement les consultants de la même entreprise
            consultants = await self.consultant_repository.get_by_company_id(tender.company_id)
            
        matches = []
        for consultant in consultants:
            # Calculer le score de match
            score = await self.calculate_match_score(consultant.id, tender_id)
            
            # Filtrer selon le score minimum
            if score >= min_score:
                matches.append({
                    "consultant": consultant,
                    "tender": tender,
                    "score": score
                })
                
        # Trier par score décroissant
        matches.sort(key=lambda x: x["score"], reverse=True)
        return matches
    
    async def find_matches_for_consultant(self, consultant_id: int,
                                         min_score: float = 0.6,
                                         include_partner_tenders: bool = True) -> List[Dict[str, Any]]:
        """
        Trouve les appels d'offres qui correspondent à un consultant
        Inclut les appels d'offres des ESN partenaires si include_partner_tenders est True
        """
        consultant = await self.consultant_repository.get_by_id(consultant_id)
        if not consultant:
            return []
            
        # Récupérer tous les appels d'offres (avec filtre selon les partenaires)
        if include_partner_tenders:
            tenders = await self.tender_repository.get_all()
        else:
            # Seulement les appels d'offres de la même entreprise
            tenders = await self.tender_repository.get_by_company_id(consultant.company_id)
            
        matches = []
        for tender in tenders:
            # Calculer le score de match
            score = await self.calculate_match_score(consultant_id, tender.id)
            
            # Filtrer selon le score minimum
            if score >= min_score:
                matches.append({
                    "consultant": consultant,
                    "tender": tender,
                    "score": score
                })
                
        # Trier par score décroissant
        matches.sort(key=lambda x: x["score"], reverse=True)
        return matches
    
    async def suggest_top_matches(self, company_id: int, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Suggère les meilleures correspondances pour une ESN
        """
        # Récupérer les consultants et appels d'offres de l'entreprise
        consultants = await self.consultant_repository.get_by_company_id(company_id)
        tenders = await self.tender_repository.get_by_company_id(company_id)
        
        all_matches = []
        
        # Pour chaque consultant, trouver les meilleurs appels d'offres
        for consultant in consultants:
            matches = await self.find_matches_for_consultant(
                consultant.id, min_score=0.7, include_partner_tenders=True
            )
            all_matches.extend(matches)
            
        # Pour chaque appel d'offres, trouver les meilleurs consultants
        for tender in tenders:
            matches = await self.find_matches_for_tender(
                tender.id, min_score=0.7, include_partner_consultants=True
            )
            # On vérifie qu'on n'ajoute pas de doublons
            for match in matches:
                # Vérifier si cette paire consultant/tender existe déjà
                exists = any(
                    m["consultant"].id == match["consultant"].id and 
                    m["tender"].id == match["tender"].id 
                    for m in all_matches
                )
                if not exists:
                    all_matches.append(match)
                    
        # Trier par score décroissant et limiter le nombre de résultats
        all_matches.sort(key=lambda x: x["score"], reverse=True)
        return all_matches[:limit]
    
    async def update_match_status(self, match_id: int, new_status: str) -> bool:
        """
        Met à jour le statut d'une correspondance
        """
        match = await self.match_repository.get_by_id(match_id)
        if not match:
            return False
            
        # Vérifier que le statut est valide
        try:
            valid_status = MatchStatus(new_status)
        except ValueError:
            return False
            
        # Mettre à jour le statut
        updated = await self.match_repository.update(
            match_id, {"status": valid_status}
        )
        
        return updated is not None