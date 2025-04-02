from typing import Dict, Any, List, Optional, Protocol
from abc import ABC, abstractmethod

class RAGService(ABC):
    """
    Interface pour le service RAG (Retrieval-Augmented Generation)
    """
    
    @abstractmethod
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
        pass
    
    @abstractmethod
    async def query(self, text: str, filters: Dict[str, Any] = None, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Interroge la base de connaissances
        
        Args:
            text: Texte de la requête
            filters: Filtres à appliquer
            top_k: Nombre de résultats à retourner
            
        Returns:
            Liste des résultats
        """
        pass
    
    @abstractmethod
    async def generate(self, text: str, filters: Dict[str, Any] = None, generation_params: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Génère une réponse avec l'approche RAG
        
        Args:
            text: Texte de la requête
            filters: Filtres à appliquer
            generation_params: Paramètres de génération
            
        Returns:
            Réponse générée
        """
        pass
    
    @abstractmethod
    async def get_documents(self, document_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Récupère la liste des documents indexés
        
        Args:
            document_type: Type de document à filtrer (optionnel)
            
        Returns:
            Liste des documents
        """
        pass
    
    @abstractmethod
    async def get_document(self, document_id: str) -> Optional[Dict[str, Any]]:
        """
        Récupère un document indexé
        
        Args:
            document_id: Identifiant du document
            
        Returns:
            Document ou None si non trouvé
        """
        pass
    
    @abstractmethod
    async def delete_document(self, document_id: str) -> bool:
        """
        Supprime un document indexé
        
        Args:
            document_id: Identifiant du document
            
        Returns:
            True si supprimé, False sinon
        """
        pass
