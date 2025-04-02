from typing import Dict, Any, List, Optional
import os
import json
import tempfile
from pathlib import Path
import requests
import logging

from app.core.interfaces.cv_analysis_service import CVAnalysisService
from app.core.interfaces.n8n_integration_service import N8nIntegrationService
from app.core.interfaces.rag_service import RAGService
from app.core.config import settings

class N8nCVAnalysisService(CVAnalysisService):
    """
    Implémentation du service d'analyse de CV utilisant n8n et des agents IA maison
    """
    
    def __init__(self, n8n_service: N8nIntegrationService, rag_service: Optional[RAGService] = None):
        """
        Initialisation du service d'analyse de CV avec n8n
        
        Args:
            n8n_service: Service d'intégration avec n8n
            rag_service: Service RAG pour l'enrichissement des analyses (optionnel)
        """
        self.n8n_service = n8n_service
        self.rag_service = rag_service
        self.logger = logging.getLogger(__name__)
        
        # Identifiants des workflows n8n
        self.workflow_ids = {
            "pdf_analysis": settings.N8N_PDF_ANALYSIS_WORKFLOW_ID,
            "docx_analysis": settings.N8N_DOCX_ANALYSIS_WORKFLOW_ID,
            "skill_extraction": settings.N8N_SKILL_EXTRACTION_WORKFLOW_ID,
            "matching": settings.N8N_MATCHING_WORKFLOW_ID,
            "portfolio_generation": settings.N8N_PORTFOLIO_WORKFLOW_ID
        }
    
    async def analyze_pdf(self, content: bytes) -> Dict[str, Any]:
        """
        Analyse un CV au format PDF en utilisant n8n et des agents IA maison
        
        Args:
            content: Contenu du fichier PDF
            
        Returns:
            Résultat de l'analyse
        """
        self.logger.info("Début de l'analyse d'un CV PDF avec n8n")
        
        try:
            # Créer un fichier temporaire pour le contenu
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
                temp_file.write(content)
                temp_path = temp_file.name
            
            # Préparer les données pour n8n
            workflow_data = {
                "file_path": temp_path,
                "file_type": "pdf",
                "metadata": {
                    "source": "TalentMatch",
                    "timestamp": self._get_current_timestamp(),
                    "version": "1.0"
                }
            }
            
            # Exécuter le workflow n8n pour l'analyse PDF
            if self.workflow_ids["pdf_analysis"]:
                result = await self.n8n_service.execute_workflow(
                    self.workflow_ids["pdf_analysis"], 
                    workflow_data
                )
                
                # Enrichir les résultats avec RAG si disponible
                if self.rag_service and result.get("extracted_text"):
                    rag_results = await self._enrich_with_rag(result["extracted_text"])
                    result["rag_enrichment"] = rag_results
                
                return result
            else:
                self.logger.warning("Workflow d'analyse PDF non configuré, utilisation de l'analyse basique")
                return self._basic_pdf_analysis()
                
        except Exception as e:
            self.logger.error(f"Erreur lors de l'analyse du CV PDF: {str(e)}")
            # En cas d'erreur, retourner une analyse basique
            return self._basic_pdf_analysis()
        finally:
            # Supprimer le fichier temporaire
            if 'temp_path' in locals() and os.path.exists(temp_path):
                os.remove(temp_path)
    
    async def analyze_docx(self, content: bytes) -> Dict[str, Any]:
        """
        Analyse un CV au format DOCX en utilisant n8n et des agents IA maison
        
        Args:
            content: Contenu du fichier DOCX
            
        Returns:
            Résultat de l'analyse
        """
        self.logger.info("Début de l'analyse d'un CV DOCX avec n8n")
        
        try:
            # Créer un fichier temporaire pour le contenu
            with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as temp_file:
                temp_file.write(content)
                temp_path = temp_file.name
            
            # Préparer les données pour n8n
            workflow_data = {
                "file_path": temp_path,
                "file_type": "docx",
                "metadata": {
                    "source": "TalentMatch",
                    "timestamp": self._get_current_timestamp(),
                    "version": "1.0"
                }
            }
            
            # Exécuter le workflow n8n pour l'analyse DOCX
            if self.workflow_ids["docx_analysis"]:
                result = await self.n8n_service.execute_workflow(
                    self.workflow_ids["docx_analysis"], 
                    workflow_data
                )
                
                # Enrichir les résultats avec RAG si disponible
                if self.rag_service and result.get("extracted_text"):
                    rag_results = await self._enrich_with_rag(result["extracted_text"])
                    result["rag_enrichment"] = rag_results
                
                return result
            else:
                self.logger.warning("Workflow d'analyse DOCX non configuré, utilisation de l'analyse basique")
                return self._basic_docx_analysis()
                
        except Exception as e:
            self.logger.error(f"Erreur lors de l'analyse du CV DOCX: {str(e)}")
            # En cas d'erreur, retourner une analyse basique
            return self._basic_docx_analysis()
        finally:
            # Supprimer le fichier temporaire
            if 'temp_path' in locals() and os.path.exists(temp_path):
                os.remove(temp_path)
    
    async def extract_skills(self, cv_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Extrait les compétences d'un CV en utilisant n8n et des agents IA maison
        
        Args:
            cv_data: Données du CV
            
        Returns:
            Liste des compétences
        """
        self.logger.info("Début de l'extraction des compétences avec n8n")
        
        try:
            # Préparer les données pour n8n
            workflow_data = {
                "cv_data": cv_data,
                "metadata": {
                    "source": "TalentMatch",
                    "timestamp": self._get_current_timestamp(),
                    "version": "1.0"
                }
            }
            
            # Exécuter le workflow n8n pour l'extraction des compétences
            if self.workflow_ids["skill_extraction"]:
                result = await self.n8n_service.execute_workflow(
                    self.workflow_ids["skill_extraction"], 
                    workflow_data
                )
                
                if "skills" in result and isinstance(result["skills"], list):
                    return result["skills"]
                else:
                    self.logger.warning("Format de retour inattendu pour l'extraction des compétences")
                    return cv_data.get("skills", [])
            else:
                self.logger.warning("Workflow d'extraction des compétences non configuré, utilisation de l'extraction basique")
                return cv_data.get("skills", [])
                
        except Exception as e:
            self.logger.error(f"Erreur lors de l'extraction des compétences: {str(e)}")
            # En cas d'erreur, retourner les compétences déjà extraites
            return cv_data.get("skills", [])
    
    async def match_with_tender(self, cv_data: Dict[str, Any], tender_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Compare un CV avec un appel d'offres en utilisant n8n et des agents IA maison
        
        Args:
            cv_data: Données du CV
            tender_data: Données de l'appel d'offres
            
        Returns:
            Résultat du matching
        """
        self.logger.info("Début du matching CV/appel d'offres avec n8n")
        
        try:
            # Préparer les données pour n8n
            workflow_data = {
                "cv_data": cv_data,
                "tender_data": tender_data,
                "metadata": {
                    "source": "TalentMatch",
                    "timestamp": self._get_current_timestamp(),
                    "version": "1.0"
                }
            }
            
            # Exécuter le workflow n8n pour le matching
            if self.workflow_ids["matching"]:
                result = await self.n8n_service.execute_workflow(
                    self.workflow_ids["matching"], 
                    workflow_data
                )
                
                return result
            else:
                self.logger.warning("Workflow de matching non configuré, utilisation du matching basique")
                return self._basic_matching(cv_data, tender_data)
                
        except Exception as e:
            self.logger.error(f"Erreur lors du matching CV/appel d'offres: {str(e)}")
            # En cas d'erreur, effectuer un matching basique
            return self._basic_matching(cv_data, tender_data)
    
    async def generate_portfolio(self, consultant_data: Dict[str, Any], tender_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Génère un dossier de compétences pour un consultant en fonction d'un appel d'offres
        en utilisant n8n et des agents IA maison
        
        Args:
            consultant_data: Données du consultant
            tender_data: Données de l'appel d'offres
            
        Returns:
            Dossier de compétences généré
        """
        self.logger.info("Début de la génération du portfolio avec n8n")
        
        try:
            # Préparer les données pour n8n
            workflow_data = {
                "consultant_data": consultant_data,
                "tender_data": tender_data,
                "metadata": {
                    "source": "TalentMatch",
                    "timestamp": self._get_current_timestamp(),
                    "version": "1.0"
                }
            }
            
            # Exécuter le workflow n8n pour la génération du portfolio
            if self.workflow_ids["portfolio_generation"]:
                result = await self.n8n_service.execute_workflow(
                    self.workflow_ids["portfolio_generation"], 
                    workflow_data
                )
                
                return result
            else:
                self.logger.warning("Workflow de génération de portfolio non configuré, utilisation de la génération basique")
                return self._basic_portfolio_generation(consultant_data, tender_data)
                
        except Exception as e:
            self.logger.error(f"Erreur lors de la génération du portfolio: {str(e)}")
            # En cas d'erreur, générer un portfolio basique
            return self._basic_portfolio_generation(consultant_data, tender_data)
    
    async def prepare_n8n_workflow_data(self, cv_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Prépare les données pour un workflow n8n
        
        Args:
            cv_data: Données du CV
            
        Returns:
            Données formatées pour n8n
        """
        return {
            "cv": cv_data,
            "metadata": {
                "source": "TalentMatch",
                "timestamp": self._get_current_timestamp(),
                "version": "1.0"
            }
        }
    
    async def _enrich_with_rag(self, text: str) -> Dict[str, Any]:
        """
        Enrichit l'analyse avec le service RAG
        
        Args:
            text: Texte à enrichir
            
        Returns:
            Résultats de l'enrichissement
        """
        if not self.rag_service:
            return {}
        
        try:
            # Interroger le service RAG
            query_results = await self.rag_service.query(
                text=text,
                filters={"document_type": "cv_template"},
                top_k=3
            )
            
            # Générer une réponse avec RAG
            generation_params = {
                "temperature": 0.2,
                "top_k": 3
            }
            
            generation_result = await self.rag_service.generate(
                text="Extraire et analyser les compétences, l'expérience et la formation à partir de ce CV.",
                filters={"document_type": "cv_template"},
                generation_params=generation_params
            )
            
            return {
                "query_results": query_results,
                "generation": generation_result
            }
        except Exception as e:
            self.logger.error(f"Erreur lors de l'enrichissement RAG: {str(e)}")
            return {}
    
    def _get_current_timestamp(self) -> str:
        """
        Retourne le timestamp actuel au format ISO
        
        Returns:
            Timestamp au format ISO
        """
        from datetime import datetime
        return datetime.now().isoformat()
    
    def _basic_pdf_analysis(self) -> Dict[str, Any]:
        """
        Analyse basique d'un CV PDF (fallback)
        
        Returns:
            Résultat de l'analyse
        """
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
            },
            "analysis_method": "basic_fallback"
        }
    
    def _basic_docx_analysis(self) -> Dict[str, Any]:
        """
        Analyse basique d'un CV DOCX (fallback)
        
        Returns:
            Résultat de l'analyse
        """
        return self._basic_pdf_analysis()
    
    def _basic_matching(self, cv_data: Dict[str, Any], tender_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Matching basique entre un CV et un appel d'offres (fallback)
        
        Args:
            cv_data: Données du CV
            tender_data: Données de l'appel d'offres
            
        Returns:
            Résultat du matching
        """
        # Extraire les compétences du CV
        cv_skills = {skill["name"].lower(): skill for skill in cv_data.get("skills", [])}
        
        # Extraire les compétences requises et préférées de l'appel d'offres
        required_skills = []
        preferred_skills = []
        
        for skill in tender_data.get("skills", []):
            if skill.get("importance") == "required":
                required_skills.append(skill)
            else:
                preferred_skills.append(skill)
        
        # Calculer le score pour les compétences requises
        required_matches = []
        required_misses = []
        for skill in required_skills:
            skill_name = skill["name"].lower()
            if skill_name in cv_skills:
                cv_skill = cv_skills[skill_name]
                required_matches.append({
                    "name": skill["name"],
                    "required_level": skill.get("level", "any"),
                    "candidate_level": cv_skill.get("level", "unknown"),
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
                    "preferred_level": skill.get("level", "any"),
                    "candidate_level": cv_skill.get("level", "unknown"),
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
            "recommendation": "strong_match" if final_score >= 0.8 else "partial_match" if final_score >= 0.5 else "weak_match",
            "matching_method": "basic_fallback"
        }
    
    def _basic_portfolio_generation(self, consultant_data: Dict[str, Any], tender_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Génération basique d'un portfolio (fallback)
        
        Args:
            consultant_data: Données du consultant
            tender_data: Données de l'appel d'offres
            
        Returns:
            Portfolio généré
        """
        # Extraire les compétences requises par l'appel d'offres
        tender_skills = [skill["name"].lower() for skill in tender_data.get("skills", [])]
        
        # Filtrer les compétences pertinentes
        relevant_skills = []
        for skill in consultant_data.get("skills", []):
            if skill["name"].lower() in tender_skills:
                relevant_skills.append(skill)
        
        # Générer le portfolio
        portfolio = {
            "consultant_name": f"{consultant_data.get('first_name', '')} {consultant_data.get('last_name', '')}",
            "consultant_title": consultant_data.get("title", ""),
            "consultant_summary": consultant_data.get("bio", ""),
            "tender_title": tender_data.get("title", ""),
            "relevant_skills": relevant_skills,
            "relevant_experiences": consultant_data.get("experiences", []),
            "education": consultant_data.get("education", []),
            "match_score": 0,  # Sera calculé par le service de matching
            "generated_at": self._get_current_timestamp(),
            "generation_method": "basic_fallback"
        }
        
        return portfolio
