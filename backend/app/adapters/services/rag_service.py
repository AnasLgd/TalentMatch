from typing import Dict, Any, List, Optional
import logging
import os
import tempfile
import uuid
from datetime import datetime

from app.core.interfaces.rag_service import RAGService
from app.core.config import settings

class VectorRAGService(RAGService):
    """
    Implémentation du service RAG (Retrieval Augmented Generation) pour enrichir l'analyse de CV
    et les matchings avec une recherche vectorielle
    """
    
    def __init__(self, vector_db_client=None, llm_service=None):
        """
        Initialise le service RAG avec un client de base de données vectorielle et un service LLM
        
        Args:
            vector_db_client: Client pour la base de données vectorielle
            llm_service: Service pour l'inférence du modèle de langage
        """
        self.logger = logging.getLogger(__name__)
        self.vector_db_client = vector_db_client
        self.llm_service = llm_service
        
        # Configuration par défaut
        self.embedding_dim = 768  # Dimension des embeddings (dépend du modèle utilisé)
        self.default_top_k = 5    # Nombre de résultats par défaut
        self.collection_names = {
            "cv": "cv_embeddings",
            "skills": "skill_embeddings",
            "tender": "tender_embeddings",
            "cv_template": "cv_template_embeddings"
        }
        
        self.logger.info("Service RAG initialisé")
    
    async def query(self, text: str, filters: Optional[Dict[str, Any]] = None, 
                   top_k: int = None) -> List[Dict[str, Any]]:
        """
        Effectue une requête de récupération sur la base de connaissances
        
        Args:
            text: Texte de la requête
            filters: Filtres optionnels à appliquer à la recherche
            top_k: Nombre de résultats à retourner
        
        Returns:
            Liste des résultats les plus pertinents
        """
        self.logger.info(f"Exécution d'une requête RAG: '{text[:50]}...'")
        
        if not self.vector_db_client:
            self.logger.warning("Client de base de données vectorielle non configuré")
            return []
        
        try:
            # Déterminer la collection à utiliser
            collection_name = self._get_collection_name(filters)
            
            # Obtenir l'embedding pour le texte de la requête
            embedding = await self._get_embedding(text)
            
            # Définir le nombre de résultats à retourner
            top_k = top_k or self.default_top_k
            
            # Effectuer la recherche vectorielle
            results = await self.vector_db_client.search(
                collection_name=collection_name,
                embedding=embedding,
                filters=filters,
                limit=top_k
            )
            
            # Traiter et formater les résultats
            formatted_results = []
            for result in results:
                formatted_results.append({
                    "document_id": result.get("id"),
                    "score": result.get("score"),
                    "metadata": result.get("metadata", {}),
                    "content": result.get("content", ""),
                    "source": result.get("source", "unknown")
                })
            
            return formatted_results
            
        except Exception as e:
            self.logger.error(f"Erreur lors de la requête RAG: {str(e)}")
            return []
    
    async def generate(self, text: str, filters: Optional[Dict[str, Any]] = None,
                      generation_params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Génère une réponse basée sur la récupération de contexte
        
        Args:
            text: Texte de la requête
            filters: Filtres optionnels à appliquer à la recherche
            generation_params: Paramètres pour la génération
        
        Returns:
            Réponse générée et informations contextuelles
        """
        self.logger.info(f"Génération RAG pour: '{text[:50]}...'")
        
        if not self.llm_service:
            self.logger.warning("Service LLM non configuré")
            return {"error": "Service LLM non disponible"}
        
        try:
            # Récupérer le contexte pertinent
            context_docs = await self.query(text, filters, top_k=3)
            
            # Préparer le contexte pour l'envoi au LLM
            context_text = "\n\n".join([doc["content"] for doc in context_docs])
            
            # Préparer les paramètres de génération
            params = generation_params or {}
            default_params = {
                "temperature": 0.3,
                "max_tokens": 500,
                "top_p": 0.95,
                "frequency_penalty": 0.0,
                "presence_penalty": 0.0
            }
            
            # Fusionner les paramètres par défaut avec ceux fournis
            generation_config = {**default_params, **params}
            
            # Construire le prompt pour le LLM
            prompt = f"""Tu es un assistant spécialisé dans l'analyse de CV et le matching pour le recrutement.
Utilise le contexte suivant pour répondre à la question:

CONTEXTE:
{context_text}

QUESTION:
{text}

Réponds de manière précise et basée uniquement sur le contexte fourni. 
Si le contexte ne contient pas l'information nécessaire, indique-le clairement.
"""
            
            # Générer la réponse avec le LLM
            llm_response = await self.llm_service.generate(
                prompt=prompt,
                **generation_config
            )
            
            # Formater la réponse finale
            return {
                "generated_text": llm_response.get("text", ""),
                "context_documents": [{"id": doc["document_id"], "score": doc["score"]} for doc in context_docs],
                "generation_config": generation_config
            }
            
        except Exception as e:
            self.logger.error(f"Erreur lors de la génération RAG: {str(e)}")
            return {"error": str(e)}
    
    async def index_document(self, content: bytes, filename: str, document_type: str, metadata: Dict[str, Any]) -> str:
        """
        Indexe un document dans la base de connaissances
        
        Args:
            content: Contenu du document
            filename: Nom du fichier
            document_type: Type de document
            metadata: Métadonnées du document
            
        Returns:
            Identifiant du document
        """
        self.logger.info(f"Indexation d'un document de type: {document_type}, fichier: {filename}")
        
        if not self.vector_db_client:
            self.logger.warning("Client de base de données vectorielle non configuré")
            return ""
        
        try:
            # Déterminer la collection
            collection_name = self.collection_names.get(document_type, "general")
            
            # Extraire le texte du contenu du document
            document_text = self._extract_text_from_content(content, filename)
            
            # Obtenir l'embedding
            embedding = await self._get_embedding(document_text)
            
            # Générer un ID de document
            document_id = self._generate_id()
            
            # Enrichir les métadonnées
            enhanced_metadata = {
                "document_type": document_type,
                "filename": filename,
                "file_extension": os.path.splitext(filename)[1].lower(),
                "indexed_at": self._get_current_timestamp(),
                **metadata
            }
            
            # Indexer le document
            result = await self.vector_db_client.insert(
                collection_name=collection_name,
                documents=[{
                    "id": document_id,
                    "embedding": embedding,
                    "metadata": enhanced_metadata,
                    "content": document_text
                }]
            )
            
            return document_id
            
        except Exception as e:
            self.logger.error(f"Erreur lors de l'indexation du document: {str(e)}")
            return {"error": str(e)}
    
    async def _get_embedding(self, text: str) -> List[float]:
        """
        Obtient l'embedding pour un texte donné
        
        Args:
            text: Texte à encoder
        
        Returns:
            Vecteur d'embedding
        """
        # Dans une implémentation réelle, nous utiliserions un service d'embedding
        # comme sentence-transformers, HuggingFace ou OpenAI
        # Pour le MVP, nous retournons un vecteur factice
        
        # Simuler un embedding de la dimension configurée
        import numpy as np
        embedding = np.random.normal(0, 1, self.embedding_dim).tolist()
        
        return embedding
    def _extract_text_from_content(self, content: bytes, filename: str) -> str:
        """
        Extrait le texte du contenu brut d'un document
        
        Args:
            content: Contenu binaire du document
            filename: Nom du fichier
        
        Returns:
            Texte extrait
        """
        file_ext = os.path.splitext(filename)[1].lower()
        
        # Créer un fichier temporaire pour le contenu
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as temp_file:
            temp_file.write(content)
            temp_path = temp_file.name
        
        try:
            extracted_text = ""
            
            # Extraire le texte selon le type de fichier
            if file_ext == '.pdf':
                from langchain_community.document_loaders import PyPDFLoader
                loader = PyPDFLoader(temp_path)
                documents = loader.load()
                extracted_text = "\n".join([doc.page_content for doc in documents])
            elif file_ext in ['.docx', '.doc']:
                from langchain_community.document_loaders import Docx2txtLoader
                loader = Docx2txtLoader(temp_path)
                documents = loader.load()
                extracted_text = "\n".join([doc.page_content for doc in documents])
            elif file_ext == '.txt':
                from langchain_community.document_loaders import TextLoader
                loader = TextLoader(temp_path)
                documents = loader.load()
                extracted_text = "\n".join([doc.page_content for doc in documents])
            else:
                # Pour les autres types de fichiers, tenter une extraction basique
                extracted_text = content.decode('utf-8', errors='ignore')
            
            return extracted_text
        
        except Exception as e:
            self.logger.error(f"Erreur lors de l'extraction du texte: {str(e)}")
            return ""
        
        finally:
            # Supprimer le fichier temporaire
            if os.path.exists(temp_path):
                os.remove(temp_path)
    
    def _extract_text_from_document(self, document: Dict[str, Any]) -> str:
        """
        Extrait le texte d'un document structuré
        
        Args:
            document: Document structuré
        
        Returns:
            Texte extrait
        """
        # Extraire le texte selon le type de document
        doc_type = document.get("document_type", "unknown")
        
        if doc_type == "cv":
            # Extraire le texte du CV
            parts = []
            
            # Informations personnelles
            personal_info = document.get("personal_info", {})
            if personal_info:
                parts.append(f"Nom: {personal_info.get('name', '')}")
                parts.append(f"Email: {personal_info.get('email', '')}")
                parts.append(f"Téléphone: {personal_info.get('phone', '')}")
                parts.append(f"Localisation: {personal_info.get('location', '')}")
            
            # Compétences
            skills = document.get("skills", [])
            if skills:
                parts.append("\nCompétences:")
                for skill in skills:
                    years = skill.get("years_experience", "")
                    level = skill.get("level", "")
                    parts.append(f"- {skill.get('name', '')}: {level} ({years} ans)")
            
            # Expériences
            experiences = document.get("experience", [])
            if experiences:
                parts.append("\nExpériences professionnelles:")
                for exp in experiences:
                    parts.append(f"- {exp.get('title', '')} chez {exp.get('company', '')}")
                    parts.append(f"  {exp.get('start_date', '')} - {exp.get('end_date', '')}")
                    parts.append(f"  {exp.get('description', '')}")
            
            # Formation
            education = document.get("education", [])
            if education:
                parts.append("\nFormation:")
                for edu in education:
                    parts.append(f"- {edu.get('degree', '')} - {edu.get('institution', '')} ({edu.get('year', '')})")
            
            return "\n".join(parts)
            
        elif doc_type == "tender":
            # Extraire le texte de l'appel d'offres
            parts = []
            
            parts.append(f"Titre: {document.get('title', '')}")
            parts.append(f"Client: {document.get('client', '')}")
            parts.append(f"Description: {document.get('description', '')}")
            
            # Compétences requises
            required_skills = document.get("required_skills", [])
            if required_skills:
                parts.append("\nCompétences requises:")
                for skill in required_skills:
                    parts.append(f"- {skill.get('name', '')}: {skill.get('level', '')} ({skill.get('years_experience', '')} ans)")
            
            # Compétences préférées
            preferred_skills = document.get("preferred_skills", [])
            if preferred_skills:
                parts.append("\nCompétences préférées:")
                for skill in preferred_skills:
                    parts.append(f"- {skill.get('name', '')}: {skill.get('level', '')} ({skill.get('years_experience', '')} ans)")
            
            return "\n".join(parts)
        
        else:
            # Pour les autres types de documents, retourner le contenu brut si disponible
            return document.get("content", str(document))
    
    def _get_collection_name(self, filters: Optional[Dict[str, Any]]) -> str:
        """
        Détermine la collection à utiliser en fonction des filtres
        
        Args:
            filters: Filtres de la requête
            
        Returns:
            Nom de la collection à utiliser
        """
        if not filters:
            return self.collection_names.get("cv", "general")
        
        doc_type = filters.get("document_type")
        if doc_type and doc_type in self.collection_names:
            return self.collection_names[doc_type]
        
        return self.collection_names.get("cv", "general")  # Collection par défaut
    
    def _get_current_timestamp(self) -> str:
        """
        Retourne le timestamp actuel au format ISO
        
        Returns:
            Timestamp au format ISO
        """
        from datetime import datetime
        return datetime.now().isoformat()
    
    def _generate_id(self) -> str:
        """
        Génère un identifiant unique
        
        Returns:
            Identifiant unique
        """
        import uuid
        return str(uuid.uuid4())
    
    async def get_documents(self, document_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Récupère la liste des documents indexés
        
        Args:
            document_type: Type de document à filtrer (optionnel)
            
        Returns:
            Liste des documents
        """
        self.logger.info(f"Récupération de la liste des documents de type: {document_type}")
        
        if not self.vector_db_client:
            self.logger.warning("Client de base de données vectorielle non configuré")
            return []
        
        try:
            # Déterminer la collection
            collection_name = self.collection_names.get(document_type, "general") if document_type else "general"
            
            # Créer les filtres si un type de document est spécifié
            filters = {"document_type": document_type} if document_type else None
            
            # Récupérer les documents
            documents = await self.vector_db_client.list_documents(
                collection_name=collection_name,
                filters=filters
            )
            
            # Formater les résultats
            return [
                {
                    "id": doc.get("id", ""),
                    "metadata": doc.get("metadata", {}),
                    "content_preview": doc.get("content", "")[:200] + "..." if len(doc.get("content", "")) > 200 else doc.get("content", "")
                }
                for doc in documents
            ]
            
        except Exception as e:
            self.logger.error(f"Erreur lors de la récupération des documents: {str(e)}")
            return []
    
    async def get_document(self, document_id: str) -> Optional[Dict[str, Any]]:
        """
        Récupère un document indexé
        
        Args:
            document_id: Identifiant du document
            
        Returns:
            Document ou None si non trouvé
        """
        self.logger.info(f"Récupération du document avec l'ID: {document_id}")
        
        if not self.vector_db_client:
            self.logger.warning("Client de base de données vectorielle non configuré")
            return None
        
        try:
            # Rechercher dans toutes les collections
            for collection_name in self.collection_names.values():
                # Récupérer le document
                document = await self.vector_db_client.get_document(
                    collection_name=collection_name,
                    document_id=document_id
                )
                
                if document:
                    return {
                        "id": document.get("id", ""),
                        "metadata": document.get("metadata", {}),
                        "content": document.get("content", ""),
                        "collection": collection_name
                    }
            
            # Document non trouvé
            return None
            
        except Exception as e:
            self.logger.error(f"Erreur lors de la récupération du document: {str(e)}")
            return None
    
    async def delete_document(self, document_id: str) -> bool:
        """
        Supprime un document indexé
        
        Args:
            document_id: Identifiant du document
            
        Returns:
            True si supprimé, False sinon
        """
        self.logger.info(f"Suppression du document avec l'ID: {document_id}")
        
        if not self.vector_db_client:
            self.logger.warning("Client de base de données vectorielle non configuré")
            return False
        
        try:
            # Rechercher dans toutes les collections
            for collection_name in self.collection_names.values():
                # Tenter de supprimer le document
                success = await self.vector_db_client.delete_document(
                    collection_name=collection_name,
                    document_id=document_id
                )
                
                if success:
                    return True
            
            # Document non trouvé ou non supprimé
            return False
            
        except Exception as e:
            self.logger.error(f"Erreur lors de la suppression du document: {str(e)}")
            return False
