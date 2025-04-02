from typing import Dict, Any, List, Optional
import os
import json
import tempfile
from pathlib import Path

from app.core.interfaces.cv_analysis_service import CVAnalysisService

class BasicCVAnalysisService(CVAnalysisService):
    """
    Implémentation basique du service d'analyse de CV sans IA pour le MVP
    """
    
    def __init__(self):
        """Initialisation du service d'analyse de CV"""
        pass
    
    async def analyze_pdf(self, content: bytes) -> Dict[str, Any]:
        """
        Analyse un CV au format PDF
        
        Args:
            content: Contenu du fichier PDF
            
        Returns:
            Résultat de l'analyse
        """
        # Dans le MVP, nous utilisons une analyse basique sans IA
        # Cette méthode serait remplacée par une analyse plus sophistiquée dans les versions futures
        
        # Simuler une extraction basique des informations
        # Dans une implémentation réelle, nous utiliserions PyPDF2 ou pdfplumber
        return {
            "skills": [
                {"name": "JavaScript", "level": "expert", "years_experience": 5},
                {"name": "Python", "level": "intermediate", "years_experience": 3},
                {"name": "React", "level": "expert", "years_experience": 4}
            ],
            "experience": [
                {
                    "title": "Développeur Full Stack",
                    "company": "Tech Solutions",
                    "start_date": "Janvier 2020",
                    "end_date": "Présent",
                    "description": "Développement d'applications web avec React et Node.js."
                }
            ],
            "education": [
                {
                    "degree": "Master en Informatique",
                    "institution": "Université de Paris",
                    "year": 2019
                }
            ],
            "languages": [
                {"name": "Français", "level": "native"},
                {"name": "Anglais", "level": "fluent"}
            ],
            "personal_info": {
                "name": "John Doe",
                "email": "john.doe@example.com",
                "phone": "+33123456789",
                "location": "Paris, France"
            }
        }
    
    async def analyze_docx(self, content: bytes) -> Dict[str, Any]:
        """
        Analyse un CV au format DOCX
        
        Args:
            content: Contenu du fichier DOCX
            
        Returns:
            Résultat de l'analyse
        """
        # Dans le MVP, nous utilisons une analyse basique sans IA
        # Cette méthode serait remplacée par une analyse plus sophistiquée dans les versions futures
        
        # Simuler une extraction basique des informations
        # Dans une implémentation réelle, nous utiliserions python-docx
        return {
            "skills": [
                {"name": "JavaScript", "level": "expert", "years_experience": 5},
                {"name": "Python", "level": "intermediate", "years_experience": 3},
                {"name": "React", "level": "expert", "years_experience": 4}
            ],
            "experience": [
                {
                    "title": "Développeur Full Stack",
                    "company": "Tech Solutions",
                    "start_date": "Janvier 2020",
                    "end_date": "Présent",
                    "description": "Développement d'applications web avec React et Node.js."
                }
            ],
            "education": [
                {
                    "degree": "Master en Informatique",
                    "institution": "Université de Paris",
                    "year": 2019
                }
            ],
            "languages": [
                {"name": "Français", "level": "native"},
                {"name": "Anglais", "level": "fluent"}
            ],
            "personal_info": {
                "name": "John Doe",
                "email": "john.doe@example.com",
                "phone": "+33123456789",
                "location": "Paris, France"
            }
        }
    
    async def extract_skills(self, cv_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Extrait les compétences d'un CV
        
        Args:
            cv_data: Données du CV
            
        Returns:
            Liste des compétences
        """
        # Dans le MVP, nous retournons simplement les compétences déjà extraites
        return cv_data.get("skills", [])
    
    async def match_with_tender(self, cv_data: Dict[str, Any], tender_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Compare un CV avec un appel d'offres
        
        Args:
            cv_data: Données du CV
            tender_data: Données de l'appel d'offres
            
        Returns:
            Résultat du matching
        """
        # Dans le MVP, nous utilisons un algorithme de matching simple
        cv_skills = {skill["name"].lower(): skill for skill in cv_data.get("skills", [])}
        required_skills = tender_data.get("required_skills", [])
        preferred_skills = tender_data.get("preferred_skills", [])
        
        # Calculer le score pour les compétences requises
        required_matches = []
        required_misses = []
        for skill in required_skills:
            skill_name = skill["name"].lower()
            if skill_name in cv_skills:
                cv_skill = cv_skills[skill_name]
                required_matches.append({
                    "name": skill["name"],
                    "required_level": skill["level"],
                    "candidate_level": cv_skill["level"],
                    "required_years": skill.get("years_experience", 0),
                    "candidate_years": cv_skill.get("years_experience", 0)
                })
            else:
                required_misses.append(skill["name"])
        
        # Calculer le score pour les compétences préférées
        preferred_matches = []
        for skill in preferred_skills:
            skill_name = skill["name"].lower()
            if skill_name in cv_skills:
                cv_skill = cv_skills[skill_name]
                preferred_matches.append({
                    "name": skill["name"],
                    "preferred_level": skill["level"],
                    "candidate_level": cv_skill["level"],
                    "preferred_years": skill.get("years_experience", 0),
                    "candidate_years": cv_skill.get("years_experience", 0)
                })
        
        # Calculer le score global
        required_score = len(required_matches) / len(required_skills) if required_skills else 1.0
        preferred_score = len(preferred_matches) / len(preferred_skills) if preferred_skills else 1.0
        
        # Le score final est pondéré : 80% pour les compétences requises, 20% pour les préférées
        final_score = required_score * 0.8 + preferred_score * 0.2
        
        return {
            "score": round(final_score * 100),  # Score sur 100
            "required_matches": required_matches,
            "required_misses": required_misses,
            "preferred_matches": preferred_matches,
            "recommendation": "strong_match" if final_score >= 0.8 else "partial_match" if final_score >= 0.5 else "weak_match"
        }
    
    async def generate_portfolio(self, consultant_data: Dict[str, Any], tender_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Génère un dossier de compétences pour un consultant en fonction d'un appel d'offres
        
        Args:
            consultant_data: Données du consultant
            tender_data: Données de l'appel d'offres
            
        Returns:
            Dossier de compétences généré
        """
        # Dans le MVP, nous générons un dossier de compétences simple
        # Extraire les compétences requises par l'appel d'offres
        required_skills = [skill["name"].lower() for skill in tender_data.get("required_skills", [])]
        preferred_skills = [skill["name"].lower() for skill in tender_data.get("preferred_skills", [])]
        all_tender_skills = required_skills + preferred_skills
        
        # Filtrer les expériences pertinentes
        relevant_experiences = []
        for exp in consultant_data.get("experiences", []):
            # Dans une implémentation réelle, nous analyserions le texte de l'expérience
            # pour déterminer sa pertinence par rapport aux compétences demandées
            relevant_experiences.append(exp)
        
        # Filtrer les compétences pertinentes
        relevant_skills = []
        for skill in consultant_data.get("skills", []):
            if skill["name"].lower() in all_tender_skills:
                relevant_skills.append(skill)
        
        # Générer le dossier de compétences
        portfolio = {
            "consultant_name": f"{consultant_data.get('first_name', '')} {consultant_data.get('last_name', '')}",
            "consultant_title": consultant_data.get("title", ""),
            "consultant_summary": consultant_data.get("bio", ""),
            "tender_title": tender_data.get("title", ""),
            "relevant_skills": relevant_skills,
            "relevant_experiences": relevant_experiences,
            "education": consultant_data.get("education", []),
            "match_score": 0,  # Sera calculé par le service de matching
            "generated_at": "2025-04-01T09:34:00Z"  # Dans une implémentation réelle, nous utiliserions datetime.now().isoformat()
        }
        
        return portfolio
    
    async def prepare_n8n_workflow_data(self, cv_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Prépare les données pour un workflow n8n
        
        Args:
            cv_data: Données du CV
            
        Returns:
            Données formatées pour n8n
        """
        # Formater les données pour n8n
        return {
            "cv": cv_data,
            "metadata": {
                "source": "TalentMatch",
                "timestamp": "2025-04-01T09:34:00Z",  # Dans une implémentation réelle, nous utiliserions datetime.now().isoformat()
                "version": "1.0"
            }
        }
