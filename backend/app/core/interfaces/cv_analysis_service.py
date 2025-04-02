from typing import Dict, Any, List, Optional, Protocol
from abc import ABC, abstractmethod

class CVAnalysisService(ABC):
    """
    Interface pour le service d'analyse de CV
    """
    
    @abstractmethod
    async def analyze_pdf(self, content: bytes) -> Dict[str, Any]:
        """
        Analyse un CV au format PDF
        
        Args:
            content: Contenu du fichier PDF
            
        Returns:
            Résultat de l'analyse
        """
        pass
    
    @abstractmethod
    async def analyze_docx(self, content: bytes) -> Dict[str, Any]:
        """
        Analyse un CV au format DOCX
        
        Args:
            content: Contenu du fichier DOCX
            
        Returns:
            Résultat de l'analyse
        """
        pass
    
    @abstractmethod
    async def extract_skills(self, cv_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Extrait les compétences d'un CV
        
        Args:
            cv_data: Données du CV
            
        Returns:
            Liste des compétences
        """
        pass
    
    @abstractmethod
    async def match_with_tender(self, cv_data: Dict[str, Any], tender_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Compare un CV avec un appel d'offres
        
        Args:
            cv_data: Données du CV
            tender_data: Données de l'appel d'offres
            
        Returns:
            Résultat du matching
        """
        pass
    
    @abstractmethod
    async def generate_portfolio(self, consultant_data: Dict[str, Any], tender_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Génère un dossier de compétences pour un consultant en fonction d'un appel d'offres
        
        Args:
            consultant_data: Données du consultant
            tender_data: Données de l'appel d'offres
            
        Returns:
            Dossier de compétences généré
        """
        pass
    
    @abstractmethod
    async def prepare_n8n_workflow_data(self, cv_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Prépare les données pour un workflow n8n
        
        Args:
            cv_data: Données du CV
            
        Returns:
            Données formatées pour n8n
        """
        pass
