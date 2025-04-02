from typing import List, Optional, Dict, Any, BinaryIO
from fastapi import Depends, UploadFile, File

from app.core.interfaces.cv_analysis_service import CVAnalysisService
from app.core.interfaces.consultant_repository import ConsultantRepository
from app.core.interfaces.skill_repository import SkillRepository

class CVAnalysisUseCase:
    """
    Cas d'utilisation pour l'analyse des CV sans IA dans le MVP
    Préparation pour intégration future avec n8n et agents IA maison
    """
    
    def __init__(
        self,
        cv_analysis_service: CVAnalysisService,
        consultant_repository: ConsultantRepository,
        skill_repository: SkillRepository
    ):
        self.cv_analysis_service = cv_analysis_service
        self.consultant_repository = consultant_repository
        self.skill_repository = skill_repository
    
    async def analyze_cv_from_pdf(self, pdf_file: BinaryIO, consultant_id: Optional[int] = None) -> Dict[str, Any]:
        """
        Analyse un CV au format PDF et extrait les informations pertinentes
        Utilise des techniques d'analyse de texte sans IA pour le MVP
        """
        # Extraire les informations du CV
        extracted_data = await self.cv_analysis_service.extract_from_pdf(pdf_file)
        
        # Valider et nettoyer les données extraites
        validated_data = await self.cv_analysis_service.validate_extracted_data(extracted_data)
        
        # Si un consultant est spécifié, mettre à jour ses informations
        if consultant_id:
            consultant = await self.consultant_repository.get_by_id(consultant_id)
            if consultant:
                # Mettre à jour les informations du consultant
                update_data = {
                    "title": validated_data.get("title"),
                    "experience_years": validated_data.get("experience_years"),
                    "bio": validated_data.get("summary")
                }
                
                # Filtrer les valeurs None
                update_data = {k: v for k, v in update_data.items() if v is not None}
                
                if update_data:
                    await self.consultant_repository.update(consultant_id, update_data)
                
                # Ajouter les compétences extraites
                skills = validated_data.get("skills", [])
                for skill in skills:
                    skill_name = skill.get("name")
                    if not skill_name:
                        continue
                    
                    # Rechercher la compétence dans la base de données
                    db_skill = await self.skill_repository.get_by_name(skill_name)
                    
                    # Si la compétence n'existe pas, la créer
                    if not db_skill:
                        db_skill = await self.skill_repository.create({
                            "name": skill_name,
                            "category": skill.get("category", "other"),
                            "description": skill.get("description", "")
                        })
                    
                    # Ajouter la compétence au consultant
                    await self.consultant_repository.add_skill(
                        consultant_id,
                        db_skill.id,
                        skill.get("proficiency_level", "intermediate"),
                        skill.get("years_experience"),
                        skill.get("details")
                    )
        
        return validated_data
    
    async def analyze_cv_from_docx(self, docx_file: BinaryIO, consultant_id: Optional[int] = None) -> Dict[str, Any]:
        """
        Analyse un CV au format DOCX et extrait les informations pertinentes
        Utilise des techniques d'analyse de texte sans IA pour le MVP
        """
        # Extraire les informations du CV
        extracted_data = await self.cv_analysis_service.extract_from_docx(docx_file)
        
        # Valider et nettoyer les données extraites
        validated_data = await self.cv_analysis_service.validate_extracted_data(extracted_data)
        
        # Même logique que pour les PDF pour la mise à jour du consultant
        if consultant_id:
            # Code similaire à analyze_cv_from_pdf
            pass
        
        return validated_data
    
    async def prepare_for_n8n_workflow(self, cv_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Prépare les données extraites du CV pour un futur traitement par n8n
        """
        return await self.cv_analysis_service.prepare_n8n_workflow_data(cv_data)
    
    async def generate_skill_portfolio(self, consultant_id: int, tender_id: int) -> str:
        """
        Génère un dossier de compétences pour un consultant en fonction d'un appel d'offres
        Utilise des templates prédéfinis sans IA dans le MVP
        """
        # Récupérer les données du consultant
        consultant = await self.consultant_repository.get_by_id(consultant_id)
        if not consultant:
            raise ValueError("Le consultant n'existe pas")
        
        # Récupérer les compétences du consultant
        consultant_skills = await self.consultant_repository.get_skills(consultant_id)
        
        # Récupérer les données de l'appel d'offres (à implémenter)
        # tender = await self.tender_repository.get_by_id(tender_id)
        # if not tender:
        #     raise ValueError("L'appel d'offres n'existe pas")
        
        # Récupérer les compétences requises pour l'appel d'offres (à implémenter)
        # tender_skills = await self.tender_repository.get_skills(tender_id)
        
        # Pour le MVP, utiliser des données simulées pour l'appel d'offres
        tender_data = {
            "id": tender_id,
            "title": "Appel d'offres simulé",
            "description": "Description simulée pour le MVP",
            "skills": []
        }
        
        # Générer le dossier de compétences
        consultant_data = {
            "id": consultant.id,
            "name": f"{consultant.user.get('first_name', '')} {consultant.user.get('last_name', '')}",
            "title": consultant.title,
            "experience_years": consultant.experience_years,
            "bio": consultant.bio,
            "skills": consultant_skills
        }
        
        return await self.cv_analysis_service.generate_skill_portfolio(consultant_data, tender_data)
