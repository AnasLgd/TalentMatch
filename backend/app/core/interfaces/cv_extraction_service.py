from typing import Protocol, List, Optional, Dict, Any, BinaryIO
from datetime import date

class CVExtractionService(Protocol):
    """
    Service pour l'extraction d'informations à partir des CV
    Priorité haute selon le document MVP
    """
    
    async def extract_from_pdf(self, pdf_file: BinaryIO) -> Dict[str, Any]:
        """
        Extrait les informations d'un CV au format PDF
        Utilise GPT-4o Vision pour les CV complexes
        """
        ...
    
    async def extract_from_image(self, image_file: BinaryIO) -> Dict[str, Any]:
        """
        Extrait les informations d'un CV à partir d'une image
        Utilise GPT-4o Vision
        """
        ...
    
    async def convert_pdf_to_images(self, pdf_file: BinaryIO) -> List[bytes]:
        """
        Convertit un PDF en une liste d'images
        Utilisé pour les CV au design complexe
        """
        ...
    
    async def validate_extracted_data(self, extracted_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Valide et nettoie les données extraites du CV
        """
        ...
    
    async def generate_skill_portfolio(self, consultant_data: Dict[str, Any], 
                                      tender_data: Dict[str, Any]) -> str:
        """
        Génère un dossier de compétences pour un consultant en fonction d'un appel d'offres
        """
        ...
