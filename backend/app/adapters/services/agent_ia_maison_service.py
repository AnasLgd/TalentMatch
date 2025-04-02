from typing import Dict, Any, List, Optional
import os
import json
import logging
import uuid
from datetime import datetime
import tempfile
from pathlib import Path

from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain_core.retrievers import BaseRetriever
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_community.llms import LlamaCpp

from app.core.interfaces.rag_service import RAGService
from app.core.interfaces.n8n_integration_service import N8nIntegrationService
from app.core.config import settings

class AgentIAMaisonService:
    """
    Service pour les agents IA maison intégrés avec n8n et RAG
    """
    
    def __init__(self, n8n_service: N8nIntegrationService, rag_service: Optional[RAGService] = None):
        """
        Initialisation du service d'agents IA maison
        
        Args:
            n8n_service: Service d'intégration avec n8n
            rag_service: Service RAG pour l'enrichissement des analyses (optionnel)
        """
        self.n8n_service = n8n_service
        self.rag_service = rag_service
        self.logger = logging.getLogger(__name__)
        
        # Initialiser le modèle d'embeddings si RAG n'est pas fourni
        if not self.rag_service:
            self.embeddings = HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2",
                model_kwargs={"device": "cpu"}
            )
            
            # Initialiser le text splitter
            self.text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200
            )
            
            # Initialiser le modèle de langage
            model_path = os.getenv("LLM_MODEL_PATH", "/opt/models/llama-3-8b-instruct.Q4_K_M.gguf")
            if os.path.exists(model_path):
                self.llm = LlamaCpp(
                    model_path=model_path,
                    temperature=0.1,
                    max_tokens=2048,
                    n_ctx=4096,
                    verbose=False
                )
            else:
                self.llm = None
                self.logger.warning(f"Modèle LLM non trouvé à {model_path}. La génération de réponses ne sera pas disponible.")
        
        # Initialiser les workflows n8n
        self.workflow_ids = {
            "cv_extraction": settings.N8N_CV_EXTRACTION_WORKFLOW_ID,
            "skill_analysis": settings.N8N_SKILL_ANALYSIS_WORKFLOW_ID,
            "consultant_matching": settings.N8N_CONSULTANT_MATCHING_WORKFLOW_ID,
            "portfolio_generation": settings.N8N_PORTFOLIO_GENERATION_WORKFLOW_ID,
            "rag_query": settings.N8N_RAG_QUERY_WORKFLOW_ID
        }
    
    async def initialize_workflows(self) -> Dict[str, str]:
        """
        Initialise les workflows n8n nécessaires pour les agents IA maison
        
        Returns:
            Dictionnaire des IDs de workflows créés
        """
        self.logger.info("Initialisation des workflows n8n pour les agents IA maison")
        
        created_workflows = {}
        
        try:
            # Créer le workflow d'extraction de CV s'il n'existe pas
            if not self.workflow_ids.get("cv_extraction"):
                workflow_id = await self.n8n_service.create_cv_analysis_workflow()
                self.workflow_ids["cv_extraction"] = workflow_id
                created_workflows["cv_extraction"] = workflow_id
                self.logger.info(f"Workflow d'extraction de CV créé avec l'ID: {workflow_id}")
            
            # Créer le workflow de matchmaking s'il n'existe pas
            if not self.workflow_ids.get("consultant_matching"):
                workflow_id = await self.n8n_service.create_matchmaking_workflow()
                self.workflow_ids["consultant_matching"] = workflow_id
                created_workflows["consultant_matching"] = workflow_id
                self.logger.info(f"Workflow de matchmaking créé avec l'ID: {workflow_id}")
            
            # Créer les autres workflows nécessaires
            # Ces méthodes devraient être implémentées dans le service n8n
            
            return created_workflows
        except Exception as e:
            self.logger.error(f"Erreur lors de l'initialisation des workflows: {str(e)}")
            return created_workflows
    
    async def extract_cv_data(self, file_content: bytes, file_name: str) -> Dict[str, Any]:
        """
        Extrait les données d'un CV en utilisant l'agent IA maison
        
        Args:
            file_content: Contenu du fichier CV
            file_name: Nom du fichier
            
        Returns:
            Données extraites du CV
        """
        self.logger.info(f"Extraction des données du CV: {file_name}")
        
        try:
            # Déterminer le type de fichier
            file_type = Path(file_name).suffix.lower().replace(".", "")
            
            # Créer un fichier temporaire
            with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file_type}") as temp_file:
                temp_file.write(file_content)
                temp_path = temp_file.name
            
            # Préparer les données pour le workflow
            workflow_data = {
                "file_path": temp_path,
                "file_type": file_type,
                "file_name": file_name,
                "metadata": {
                    "source": "TalentMatch",
                    "timestamp": datetime.now().isoformat(),
                    "process_id": str(uuid.uuid4())
                }
            }
            
            # Exécuter le workflow d'extraction de CV
            if self.workflow_ids.get("cv_extraction"):
                result = await self.n8n_service.execute_workflow(
                    self.workflow_ids["cv_extraction"],
                    workflow_data
                )
                
                # Enrichir avec RAG si disponible
                if self.rag_service and "extracted_text" in result:
                    rag_enrichment = await self._enrich_with_rag(
                        result["extracted_text"],
                        "Extraire les compétences, l'expérience et la formation de ce CV."
                    )
                    result["rag_enrichment"] = rag_enrichment
                
                return result
            else:
                self.logger.warning("Workflow d'extraction de CV non configuré")
                return self._fallback_cv_extraction(file_type)
        
        except Exception as e:
            self.logger.error(f"Erreur lors de l'extraction des données du CV: {str(e)}")
            return self._fallback_cv_extraction(file_type)
        
        finally:
            # Supprimer le fichier temporaire
            if 'temp_path' in locals() and os.path.exists(temp_path):
                os.remove(temp_path)
    
    async def analyze_skills(self, cv_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyse les compétences extraites d'un CV
        
        Args:
            cv_data: Données du CV
            
        Returns:
            Analyse des compétences
        """
        self.logger.info("Analyse des compétences")
        
        try:
            # Préparer les données pour le workflow
            workflow_data = {
                "cv_data": cv_data,
                "metadata": {
                    "source": "TalentMatch",
                    "timestamp": datetime.now().isoformat(),
                    "process_id": str(uuid.uuid4())
                }
            }
            
            # Exécuter le workflow d'analyse des compétences
            if self.workflow_ids.get("skill_analysis"):
                result = await self.n8n_service.execute_workflow(
                    self.workflow_ids["skill_analysis"],
                    workflow_data
                )
                
                return result
            else:
                self.logger.warning("Workflow d'analyse des compétences non configuré")
                return self._fallback_skill_analysis(cv_data)
        
        except Exception as e:
            self.logger.error(f"Erreur lors de l'analyse des compétences: {str(e)}")
            return self._fallback_skill_analysis(cv_data)
    
    async def match_consultant_with_tender(self, consultant_data: Dict[str, Any], tender_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Effectue le matching entre un consultant et un appel d'offres
        
        Args:
            consultant_data: Données du consultant
            tender_data: Données de l'appel d'offres
            
        Returns:
            Résultat du matching
        """
        self.logger.info("Matching consultant avec appel d'offres")
        
        try:
            # Préparer les données pour le workflow
            workflow_data = {
                "consultant_data": consultant_data,
                "tender_data": tender_data,
                "metadata": {
                    "source": "TalentMatch",
                    "timestamp": datetime.now().isoformat(),
                    "process_id": str(uuid.uuid4())
                }
            }
            
            # Exécuter le workflow de matching
            if self.workflow_ids.get("consultant_matching"):
                result = await self.n8n_service.execute_workflow(
                    self.workflow_ids["consultant_matching"],
                    workflow_data
                )
                
                # Enrichir avec RAG si disponible
                if self.rag_service:
                    query = f"Évaluer la correspondance entre un consultant avec les compétences {', '.join([s['name'] for s in consultant_data.get('skills', [])])} et un appel d'offres qui demande {', '.join([s['name'] for s in tender_data.get('skills', [])])}."
                    rag_enrichment = await self._enrich_with_rag(query, query)
                    result["rag_enrichment"] = rag_enrichment
                
                return result
            else:
                self.logger.warning("Workflow de matching non configuré")
                return self._fallback_matching(consultant_data, tender_data)
        
        except Exception as e:
            self.logger.error(f"Erreur lors du matching: {str(e)}")
            return self._fallback_matching(consultant_data, tender_data)
    
    async def generate_consultant_portfolio(self, consultant_data: Dict[str, Any], tender_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Génère un portfolio pour un consultant en fonction d'un appel d'offres
        
        Args:
            consultant_data: Données du consultant
            tender_data: Données de l'appel d'offres
            
        Returns:
            Portfolio généré
        """
        self.logger.info("Génération du portfolio consultant")
        
        try:
            # Préparer les données pour le workflow
            workflow_data = {
                "consultant_data": consultant_data,
                "tender_data": tender_data,
                "metadata": {
                    "source": "TalentMatch",
                    "timestamp": datetime.now().isoformat(),
                    "process_id": str(uuid.uuid4())
                }
            }
            
            # Exécuter le workflow de génération de portfolio
            if self.workflow_ids.get("portfolio_generation"):
                result = await self.n8n_service.execute_workflow(
                    self.workflow_ids["portfolio_generation"],
                    workflow_data
                )
                
                # Enrichir avec RAG si disponible
                if self.rag_service:
                    query = f"Générer un portfolio professionnel pour un consultant avec les compétences {', '.join([s['name'] for s in consultant_data.get('skills', [])])} pour un appel d'offres qui demande {', '.join([s['name'] for s in tender_data.get('skills', [])])}."
                    rag_enrichment = await self._enrich_with_rag(query, query)
                    result["rag_enrichment"] = rag_enrichment
                
                return result
            else:
                self.logger.warning("Workflow de génération de portfolio non configuré")
                return self._fallback_portfolio_generation(consultant_data, tender_data)
        
        except Exception as e:
            self.logger.error(f"Erreur lors de la génération du portfolio: {str(e)}")
            return self._fallback_portfolio_generation(consultant_data, tender_data)
    
    async def query_knowledge_base(self, query: str, filters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Interroge la base de connaissances avec RAG
        
        Args:
            query: Requête à exécuter
            filters: Filtres à appliquer
            
        Returns:
            Résultats de la requête
        """
        self.logger.info(f"Requête RAG: {query}")
        
        try:
            # Utiliser le service RAG si disponible
            if self.rag_service:
                # Exécuter la requête RAG
                query_results = await self.rag_service.query(
                    text=query,
                    filters=filters,
                    top_k=5
                )
                
                # Générer une réponse
                generation_result = await self.rag_service.generate(
                    text=query,
                    filters=filters,
                    generation_params={"temperature": 0.2, "top_k": 5}
                )
                
                return {
                    "query_results": query_results,
                    "generation": generation_result
                }
            
            # Sinon, utiliser le workflow n8n
            elif self.workflow_ids.get("rag_query"):
                workflow_data = {
                    "query": query,
                    "filters": filters or {},
                    "metadata": {
                        "source": "TalentMatch",
                        "timestamp": datetime.now().isoformat(),
                        "process_id": str(uuid.uuid4())
                    }
                }
                
                result = await self.n8n_service.execute_workflow(
                    self.workflow_ids["rag_query"],
                    workflow_data
                )
                
                return result
            
            else:
                self.logger.warning("Ni le service RAG ni le workflow RAG ne sont configurés")
                return {"error": "Service RAG non disponible"}
        
        except Exception as e:
            self.logger.error(f"Erreur lors de la requête RAG: {str(e)}")
            return {"error": str(e)}
    
    async def _enrich_with_rag(self, context: str, query: str) -> Dict[str, Any]:
        """
        Enrichit les données avec le service RAG
        
        Args:
            context: Contexte pour la requête
            query: Requête à exécuter
            
        Returns:
            Résultats de l'enrichissement
        """
        if not self.rag_service:
            return {}
        
        try:
            # Interroger le service RAG
            query_results = await self.rag_service.query(
                text=query,
                top_k=3
            )
            
            # Générer une réponse avec RAG
            generation_params = {
                "temperature": 0.2,
                "top_k": 3
            }
            
            generation_result = await self.rag_service.generate(
                text=query,
                generation_params=generation_params
            )
            
            return {
                "query_results": query_results,
                "generation": generation_result
            }
        except Exception as e:
            self.logger.error(f"Erreur lors de l'enrichissement RAG: {str(e)}")
            return {}
    
    def _fallback_cv_extraction(self, file_type: str) -> Dict[str, Any]:
        """
        Méthode de secours pour l'extraction de CV
        
        Args:
            file_type: Type de fichier
            
        Returns:
            Données extraites par défaut
        """
        return {
            "personal_info": {
                "name": "John Doe",
                "email": "john.doe@example.com",
                "phone": "+33123456789",
                "location": "Paris, France"
            },
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
            "extraction_method": "fallback",
            "file_type": file_type
        }
    
    def _fallback_skill_analysis(self, cv_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Méthode de secours pour l'analyse des compétences
        
        Args:
            cv_data: Données du CV
            
        Returns:
            Analyse des compétences par défaut
        """
        skills = cv_data.get("skills", [])
        
        # Catégoriser les compétences
        technical_skills = []
        soft_skills = []
        
        for skill in skills:
            if skill.get("name", "").lower() in ["communication", "leadership", "travail d'équipe", "gestion de projet"]:
                soft_skills.append(skill)
            else:
                technical_skills.append(skill)
        
        return {
            "skills": skills,
            "technical_skills": technical_skills,
            "soft_skills": soft_skills,
            "skill_count": len(skills),
            "top_skills": skills[:3] if len(skills) >= 3 else skills,
            "analysis_method": "fallback"
        }
    
    def _fallback_matching(self, consultant_data: Dict[str, Any], tender_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Méthode de secours pour le matching
        
        Args:
            consultant_data: Données du consultant
            tender_data: Données de l'appel d'offres
            
        Returns:
            Résultat du matching par défaut
        """
        # Extraire les compétences du consultant
        consultant_skills = {skill["name"].lower(): skill for skill in consultant_data.get("skills", [])}
        
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
            if skill_name in consultant_skills:
                consultant_skill = consultant_skills[skill_name]
                required_matches.append({
                    "name": skill["name"],
                    "required_level": skill.get("level", "any"),
                    "consultant_level": consultant_skill.get("level", "unknown"),
                    "required_years": skill.get("years_experience", 0),
                    "consultant_years": consultant_skill.get("years_experience", 0)
                })
            else:
                required_misses.append(skill["name"])
        
        # Calculer le score pour les compétences préférées
        preferred_matches = []
        for skill in preferred_skills:
            skill_name = skill["name"].lower()
            if skill_name in consultant_skills:
                consultant_skill = consultant_skills[skill_name]
                preferred_matches.append({
                    "name": skill["name"],
                    "preferred_level": skill.get("level", "any"),
                    "consultant_level": consultant_skill.get("level", "unknown"),
                    "preferred_years": skill.get("years_experience", 0),
                    "consultant_years": consultant_skill.get("years_experience", 0)
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
            "matching_method": "fallback"
        }
    
    def _fallback_portfolio_generation(self, consultant_data: Dict[str, Any], tender_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Méthode de secours pour la génération de portfolio
        
        Args:
            consultant_data: Données du consultant
            tender_data: Données de l'appel d'offres
            
        Returns:
            Portfolio par défaut
        """
        # Extraire les compétences requises par l'appel d'offres
        tender_skills = [skill["name"].lower() for skill in tender_data.get("skills", [])]
        
        # Filtrer les compétences pertinentes
        relevant_skills = []
        for skill in consultant_data.get("skills", []):
            if skill["name"].lower() in tender_skills:
                relevant_skills.append(skill)
        
        # Générer le portfolio
        return {
            "consultant_name": f"{consultant_data.get('first_name', '')} {consultant_data.get('last_name', '')}",
            "consultant_title": consultant_data.get("title", ""),
            "consultant_summary": consultant_data.get("bio", ""),
            "tender_title": tender_data.get("title", ""),
            "relevant_skills": relevant_skills,
            "relevant_experiences": consultant_data.get("experiences", []),
            "education": consultant_data.get("education", []),
            "match_score": 0,  # Sera calculé par le service de matching
            "generated_at": datetime.now().isoformat(),
            "generation_method": "fallback"
        }
