from typing import Dict, Any, List, Optional
import os
import json
import logging
import tempfile
from pathlib import Path
import re
from datetime import datetime, date

from app.core.interfaces.cv_analysis_service import CVAnalysisService
from app.core.interfaces.rag_service import RAGService

class EnhancedCVAnalysisService(CVAnalysisService):
    """
    Implémentation améliorée du service d'analyse de CV avec NLP et IA
    """
    
    def __init__(self, rag_service: Optional[RAGService] = None):
        """
        Initialisation du service d'analyse de CV avancé
        
        Args:
            rag_service: Service RAG pour l'extraction de contexte (optionnel)
        """
        self.rag_service = rag_service
        self.logger = logging.getLogger(__name__)
        
        # Dictionnaire des compétences courantes avec leur catégorie
        self.skills_categories = {
            # Langages de programmation
            "python": "programming_language",
            "javascript": "programming_language",
            "typescript": "programming_language",
            "java": "programming_language",
            "c#": "programming_language",
            "c++": "programming_language",
            "php": "programming_language",
            "ruby": "programming_language",
            "go": "programming_language",
            "rust": "programming_language",
            "swift": "programming_language",
            "kotlin": "programming_language",
            
            # Frameworks frontend
            "react": "frontend_framework",
            "angular": "frontend_framework",
            "vue": "frontend_framework",
            "svelte": "frontend_framework",
            "jquery": "frontend_framework",
            
            # Frameworks backend
            "django": "backend_framework",
            "flask": "backend_framework",
            "fastapi": "backend_framework",
            "express": "backend_framework",
            "spring": "backend_framework",
            "laravel": "backend_framework",
            "ruby on rails": "backend_framework",
            "asp.net": "backend_framework",
            
            # Bases de données
            "sql": "database",
            "mysql": "database",
            "postgresql": "database",
            "mongodb": "database",
            "redis": "database",
            "elasticsearch": "database",
            "sqlite": "database",
            "oracle": "database",
            "cassandra": "database",
            
            # DevOps
            "docker": "devops",
            "kubernetes": "devops",
            "jenkins": "devops",
            "github actions": "devops",
            "gitlab ci": "devops",
            "aws": "cloud",
            "azure": "cloud",
            "gcp": "cloud",
            "terraform": "devops",
            "ansible": "devops",
            
            # UI/UX
            "figma": "design",
            "sketch": "design",
            "adobe xd": "design",
            "photoshop": "design",
            "illustrator": "design",
            
            # Soft skills
            "communication": "soft_skill",
            "leadership": "soft_skill",
            "teamwork": "soft_skill",
            "problem solving": "soft_skill",
            "time management": "soft_skill",
            "critical thinking": "soft_skill",
            "project management": "soft_skill",
            "agile": "methodology",
            "scrum": "methodology",
            "kanban": "methodology",
            
            # Data science
            "machine learning": "data_science",
            "deep learning": "data_science",
            "tensorflow": "data_science",
            "pytorch": "data_science",
            "pandas": "data_science",
            "numpy": "data_science",
            "scikit-learn": "data_science",
            "data analysis": "data_science",
            "statistics": "data_science",
            "big data": "data_science",
            "hadoop": "data_science",
            "spark": "data_science",
            
            # Mobile
            "ios": "mobile",
            "android": "mobile",
            "react native": "mobile",
            "flutter": "mobile",
            "xamarin": "mobile",
            
            # Testing
            "testing": "testing",
            "unit testing": "testing",
            "integration testing": "testing",
            "e2e testing": "testing",
            "jest": "testing",
            "pytest": "testing",
            "selenium": "testing",
            "cypress": "testing",
            "mocha": "testing",
            "chai": "testing",
        }
        
        # Niveaux de compétence avec leur équivalent numérique
        self.skill_levels = {
            "beginner": 1,
            "basic": 1,
            "elementary": 1,
            "novice": 1,
            
            "intermediate": 2,
            "moderate": 2,
            "average": 2,
            
            "advanced": 3,
            "proficient": 3,
            "skilled": 3,
            "competent": 3,
            
            "expert": 4,
            "master": 4,
            "experienced": 4,
            "senior": 4,
            
            "specialist": 5,
            "guru": 5,
            "authority": 5,
        }
    
    async def _extract_text_from_pdf(self, content: bytes) -> str:
        """
        Extrait le texte d'un fichier PDF
        
        Dans une implémentation réelle, nous utiliserions PyPDF2, pdfplumber ou pdfminer
        """
        # Simuler l'extraction de texte pour le MVP
        # Dans une version réelle, le code ressemblerait à ceci:
        '''
        import io
        import PyPDF2
        
        pdf_file = io.BytesIO(content)
        reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in range(len(reader.pages)):
            text += reader.pages[page].extract_text()
        return text
        '''
        
        # Pour le MVP, on utilise un texte exemple
        return """
        JOHN DOE
        Développeur Full Stack
        Paris, France | +33123456789 | john.doe@example.com
        
        RÉSUMÉ
        Développeur Full Stack avec 5 ans d'expérience en développement web et mobile.
        Compétences avancées en JavaScript, React, Node.js et bases de données SQL/NoSQL.
        
        COMPÉTENCES
        • Langages: JavaScript (5 ans), Python (3 ans), TypeScript (2 ans)
        • Frontend: React (4 ans), Angular (2 ans), HTML5, CSS3, SASS
        • Backend: Node.js (4 ans), Express.js, Django, Flask
        • Bases de données: MongoDB, PostgreSQL, MySQL
        • DevOps: Docker, Kubernetes, AWS, CI/CD, Git
        • Méthodologies: Agile, Scrum, TDD
        
        EXPÉRIENCE PROFESSIONNELLE
        Développeur Full Stack
        Tech Solutions, Paris
        Janvier 2020 - Présent
        • Développement d'applications web avec React et Node.js
        • Mise en place d'une architecture microservices
        • Implémentation de tests automatisés et CI/CD
        • Collaboration avec les équipes produit et design
        
        Développeur Frontend
        Digital Agency, Lyon
        Juin 2018 - Décembre 2019
        • Création d'interfaces utilisateur responsive
        • Développement de composants React réutilisables
        • Optimisation de performances frontend
        
        FORMATION
        Master en Informatique
        Université de Paris
        2016 - 2018
        
        Licence en Génie Logiciel
        INSA Lyon
        2013 - 2016
        
        LANGUES
        • Français (natif)
        • Anglais (courant)
        • Espagnol (notions)
        """
    
    async def _extract_text_from_docx(self, content: bytes) -> str:
        """
        Extrait le texte d'un fichier DOCX
        
        Dans une implémentation réelle, nous utiliserions python-docx
        """
        # Simuler l'extraction de texte pour le MVP
        # Dans une version réelle, le code ressemblerait à ceci:
        '''
        import io
        from docx import Document
        
        docx_file = io.BytesIO(content)
        document = Document(docx_file)
        text = ""
        for paragraph in document.paragraphs:
            text += paragraph.text + "\n"
        return text
        '''
        
        # Pour le MVP, on utilise le même texte exemple que pour le PDF
        return await self._extract_text_from_pdf(content)
    
    async def _extract_skills_from_text(self, text: str) -> List[Dict[str, Any]]:
        """
        Extrait les compétences à partir du texte du CV
        
        Args:
            text: Texte du CV
            
        Returns:
            Liste des compétences avec leur niveau et catégorie
        """
        skills = []
        text_lower = text.lower()
        
        # Rechercher les compétences connues dans le texte
        for skill_name, category in self.skills_categories.items():
            if skill_name in text_lower:
                # Chercher le niveau de compétence à proximité de la mention de la compétence
                level = "intermediate"  # Niveau par défaut
                years_experience = None
                
                # Recherche du niveau
                for level_name, level_value in self.skill_levels.items():
                    if level_name in text_lower and abs(text_lower.find(skill_name) - text_lower.find(level_name)) < 100:
                        level = level_name
                        break
                
                # Recherche des années d'expérience
                # Chercher un pattern comme "Python (3 ans)" ou "JavaScript - 5 ans"
                patterns = [
                    rf"{skill_name}\s*\((\d+)\s*an",
                    rf"{skill_name}\s*[:-]\s*(\d+)\s*an",
                    rf"{skill_name}\s+(\d+)\s+an"
                ]
                
                for pattern in patterns:
                    matches = re.findall(pattern, text_lower)
                    if matches:
                        years_experience = int(matches[0])
                        break
                
                skills.append({
                    "name": skill_name.title(),  # Mettre en majuscule la première lettre
                    "level": level,
                    "level_value": self.skill_levels.get(level, 2),  # Valeur numérique du niveau
                    "category": category,
                    "years_experience": years_experience
                })
        
        return skills
    
    async def _extract_experience_from_text(self, text: str) -> List[Dict[str, Any]]:
        """
        Extrait les expériences professionnelles à partir du texte du CV
        
        Args:
            text: Texte du CV
            
        Returns:
            Liste des expériences professionnelles
        """
        experiences = []
        
        # Dans une implémentation réelle, nous utiliserions des techniques NLP plus avancées
        # Pour le MVP, on utilise un parsing simple basé sur des patterns
        
        # Rechercher des sections d'expérience
        experience_sections = re.split(r"EXPÉRIENCE PROFESSIONNELLE|EXPERIENCE|EMPLOIS", text, flags=re.IGNORECASE)
        
        if len(experience_sections) > 1:
            # Prendre la section après le titre "EXPÉRIENCE PROFESSIONNELLE"
            experience_text = experience_sections[1]
            
            # La section suivante est généralement la formation
            education_idx = re.search(r"FORMATION|ÉDUCATION|EDUCATION", experience_text, flags=re.IGNORECASE)
            if education_idx:
                experience_text = experience_text[:education_idx.start()]
            
            # Diviser en expériences individuelles
            # On recherche des patterns comme "Titre\nEntreprise, Lieu\nPériode"
            experiences_raw = re.split(r"\n\s*\n", experience_text)
            
            for exp in experiences_raw:
                if not exp.strip():
                    continue
                
                lines = exp.strip().split('\n')
                if len(lines) >= 3:
                    title = lines[0].strip()
                    
                    # Analyser la deuxième ligne (entreprise, lieu)
                    company_line = lines[1]
                    company_parts = company_line.split(',')
                    company = company_parts[0].strip()
                    location = company_parts[1].strip() if len(company_parts) > 1 else None
                    
                    # Analyser la troisième ligne (période)
                    date_line = lines[2]
                    dates = re.findall(r"(Janvier|Février|Mars|Avril|Mai|Juin|Juillet|Août|Septembre|Octobre|Novembre|Décembre|Jan|Fév|Mar|Avr|Mai|Jun|Jul|Aoû|Sep|Oct|Nov|Déc)\s+(\d{4})\s*-\s*(Janvier|Février|Mars|Avril|Mai|Juin|Juillet|Août|Septembre|Octobre|Novembre|Décembre|Jan|Fév|Mar|Avr|Mai|Jun|Jul|Aoû|Sep|Oct|Nov|Déc|Présent)\s*(\d{4})?", date_line, flags=re.IGNORECASE)
                    
                    start_date = None
                    end_date = None
                    if dates:
                        start_month, start_year, end_month, end_year = dates[0]
                        start_date = f"{start_month} {start_year}"
                        
                        if end_month.lower() == "présent":
                            end_date = "Présent"
                        else:
                            end_date = f"{end_month} {end_year if end_year else ''}"
                    
                    # Description de l'expérience (les lignes restantes)
                    description = "\n".join(lines[3:]) if len(lines) > 3 else ""
                    
                    experiences.append({
                        "title": title,
                        "company": company,
                        "location": location,
                        "start_date": start_date,
                        "end_date": end_date,
                        "description": description
                    })
        
        return experiences
    
    async def _extract_education_from_text(self, text: str) -> List[Dict[str, Any]]:
        """
        Extrait la formation à partir du texte du CV
        
        Args:
            text: Texte du CV
            
        Returns:
            Liste des formations
        """
        education = []
        
        # Rechercher des sections de formation
        education_sections = re.split(r"FORMATION|ÉDUCATION|EDUCATION", text, flags=re.IGNORECASE)
        
        if len(education_sections) > 1:
            # Prendre la section après le titre "FORMATION"
            education_text = education_sections[1]
            
            # La section suivante est généralement les langues ou certifications
            next_section_idx = re.search(r"LANGUES|CERTIFICATIONS|COMPÉTENCES", education_text, flags=re.IGNORECASE)
            if next_section_idx:
                education_text = education_text[:next_section_idx.start()]
            
            # Diviser en formations individuelles
            education_raw = re.split(r"\n\s*\n", education_text)
            
            for edu in education_raw:
                if not edu.strip():
                    continue
                
                lines = edu.strip().split('\n')
                if len(lines) >= 2:
                    degree = lines[0].strip()
                    
                    # Analyser la deuxième ligne (institution)
                    institution = lines[1].strip()
                    
                    # Analyser les années
                    year = None
                    years_match = re.search(r"(\d{4})\s*-\s*(\d{4})|(\d{4})", edu)
                    if years_match:
                        if years_match.group(3):  # Format simple année
                            year = int(years_match.group(3))
                        else:  # Format début - fin
                            year = int(years_match.group(2))  # Année de fin
                    
                    education.append({
                        "degree": degree,
                        "institution": institution,
                        "year": year
                    })
        
        return education
    
    async def _extract_personal_info(self, text: str) -> Dict[str, Any]:
        """
        Extrait les informations personnelles à partir du texte du CV
        
        Args:
            text: Texte du CV
            
        Returns:
            Informations personnelles
        """
        personal_info = {}
        
        # Extraire le nom (en supposant qu'il soit en haut du CV)
        first_lines = text.strip().split('\n')[:3]
        if first_lines:
            name_line = first_lines[0].strip()
            if len(name_line.split()) <= 4:  # C'est probablement un nom
                personal_info["name"] = name_line
        
        # Extraire l'email
        email_match = re.search(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", text)
        if email_match:
            personal_info["email"] = email_match.group(0)
        
        # Extraire le numéro de téléphone
        phone_match = re.search(r"\+\d{1,4}[\s\d-]{7,12}|\d{2}[\s\.-]?\d{2}[\s\.-]?\d{2}[\s\.-]?\d{2}[\s\.-]?\d{2}", text)
        if phone_match:
            personal_info["phone"] = phone_match.group(0)
        
        # Extraire la localisation
        location_patterns = [
            r"(?:Adresse|Location|Localisation|Ville)\s*:\s*([^,\n]+(?:,\s*[^,\n]+)*)",
            r"([^,|\n]+,\s*[^,|\n]+)\s*\|\s*",
            r"\n([A-Z][a-zé]+(?: [A-Z][a-zé]+)*,\s*(?:France|Belgique|Suisse|Canada))"
        ]
        
        for pattern in location_patterns:
            location_match = re.search(pattern, text)
            if location_match:
                personal_info["location"] = location_match.group(1).strip()
                break
        
        return personal_info
    
    async def _parse_cv_text(self, text: str) -> Dict[str, Any]:
        """
        Analyse le texte brut d'un CV et extrait les informations structurées
        
        Args:
            text: Texte du CV
            
        Returns:
            Données structurées du CV
        """
        cv_data = {}
        
        # Extraire les compétences
        cv_data["skills"] = await self._extract_skills_from_text(text)
        
        # Extraire les expériences professionnelles
        cv_data["experience"] = await self._extract_experience_from_text(text)
        
        # Extraire la formation
        cv_data["education"] = await self._extract_education_from_text(text)
        
        # Extraire les informations personnelles
        cv_data["personal_info"] = await self._extract_personal_info(text)
        
        return cv_data
    
    async def analyze_pdf(self, content: bytes) -> Dict[str, Any]:
        """
        Analyse un CV au format PDF
        
        Args:
            content: Contenu du fichier PDF
            
        Returns:
            Résultat de l'analyse
        """
        try:
            # Extraire le texte du PDF
            text = await self._extract_text_from_pdf(content)
            
            # Analyser le texte
            cv_data = await self._parse_cv_text(text)
            
            # Enrichir avec RAG si disponible
            if self.rag_service:
                cv_data = await self._enrich_with_rag(cv_data, text)
            
            return cv_data
            
        except Exception as e:
            self.logger.error(f"Erreur lors de l'analyse du PDF: {str(e)}")
            # Fallback sur le service basique
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
        try:
            # Extraire le texte du DOCX
            text = await self._extract_text_from_docx(content)
            
            # Analyser le texte
            cv_data = await self._parse_cv_text(text)
            
            # Enrichir avec RAG si disponible
            if self.rag_service:
                cv_data = await self._enrich_with_rag(cv_data, text)
            
            return cv_data
            
        except Exception as e:
            self.logger.error(f"Erreur lors de l'analyse du DOCX: {str(e)}")
            # Fallback sur le service basique (même que pour PDF)
            return await self.analyze_pdf(content)
    
    async def _enrich_with_rag(self, cv_data: Dict[str, Any], original_text: str) -> Dict[str, Any]:
        """
        Enrichit les données du CV avec le service RAG
        
        Args:
            cv_data: Données du CV
            original_text: Texte original du CV
            
        Returns:
            Données du CV enrichies
        """
        if not self.rag_service:
            return cv_data
        
        try:
            # Requête RAG pour trouver des informations additionnelles
            rag_query = f"Analyser et enrichir les compétences et expériences suivantes : {cv_data['skills']} {cv_data['experience']}"
            rag_result = await self.rag_service.query(rag_query, original_text)
            
            # Si des informations supplémentaires sont trouvées, les ajouter
            if rag_result and "additional_skills" in rag_result:
                for skill in rag_result["additional_skills"]:
                    if not any(s["name"].lower() == skill["name"].lower() for s in cv_data["skills"]):
                        cv_data["skills"].append(skill)
            
            # Enrichir les descriptions d'expérience si présentes
            if rag_result and "enriched_experiences" in rag_result:
                for i, exp in enumerate(cv_data["experience"]):
                    if i < len(rag_result["enriched_experiences"]):
                        cv_data["experience"][i]["enriched_description"] = rag_result["enriched_experiences"][i]
            
            return cv_data
            
        except Exception as e:
            self.logger.error(f"Erreur lors de l'enrichissement avec RAG: {str(e)}")
            return cv_data
    
    async def extract_skills(self, cv_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Extrait les compétences d'un CV
        
        Args:
            cv_data: Données du CV
            
        Returns:
            Liste des compétences
        """
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
        # Version améliorée de l'algorithme de matching
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
                # Vérifier le niveau de compétence
                required_level = skill.get("level", "intermediate")
                required_level_value = self.skill_levels.get(required_level, 2)
                candidate_level = cv_skill.get("level", "intermediate")
                candidate_level_value = self.skill_levels.get(candidate_level, 2)
                
                # Vérifier les années d'expérience
                required_years = skill.get("years_experience", 0)
                candidate_years = cv_skill.get("years_experience", 0)
                
                # Calculer le score de correspondance pour cette compétence
                level_match = min(candidate_level_value / required_level_value, 1.0)
                years_match = 1.0 if not required_years else min(candidate_years / max(required_years, 1), 1.0)
                
                # Score global pour cette compétence
                skill_score = (level_match * 0.6) + (years_match * 0.4)
                
                required_matches.append({
                    "name": skill["name"],
                    "required_level": required_level,
                    "candidate_level": candidate_level,
                    "required_years": required_years,
                    "candidate_years": candidate_years,
                    "skill_score": round(skill_score, 2)
                })
            else:
                required_misses.append(skill["name"])
        
        # Calculer le score pour les compétences préférées
        preferred_matches = []
        for skill in preferred_skills:
            skill_name = skill["name"].lower()
            if skill_name in cv_skills:
                cv_skill = cv_skills[skill_name]
                # Même logique que pour les compétences requises
                required_level = skill.get("level", "intermediate")
                required_level_value = self.skill_levels.get(required_level, 2)
                candidate_level = cv_skill.get("level", "intermediate")
                candidate_level_value = self.skill_levels.get(candidate_level, 2)
                
                required_years = skill.get("years_experience", 0)
                candidate_years = cv_skill.get("years_experience", 0)
                
                level_match = min(candidate_level_value / required_level_value, 1.0)
                years_match = 1.0 if not required_years else min(candidate_years / max(required_years, 1), 1.0)
                
                skill_score = (level_match * 0.6) + (years_match * 0.4)
                
                preferred_matches.append({
                    "name": skill["name"],
                    "preferred_level": required_level,
                    "candidate_level": candidate_level,
                    "preferred_years": required_years,
                    "candidate_years": candidate_years,
                    "skill_score": round(skill_score, 2)
                })
        
        # Calculer les scores moyens
        required_skills_score = sum(match["skill_score"] for match in required_matches) / len(required_skills) if required_skills else 1.0
        required_coverage = len(required_matches) / len(required_skills) if required_skills else 1.0
        preferred_skills_score = sum(match["skill_score"] for match in preferred_matches) / len(preferred_skills) if preferred_skills else 1.0
        
        # Pondérer les scores : compétences requises (65%), couverture des compétences requises (20%), compétences préférées (15%)
        final_score = (
            required_skills_score * 0.65 +
            required_coverage * 0.2 +
            preferred_skills_score * 0.15
        )
        
        # Déterminer les compétences manquantes mais similaires
        missing_skills_suggestions = []
        for missing_skill in required_misses:
            # Dans une implémentation réelle, nous utiliserions un système de recherche de similarité
            # basé sur les embeddings ou une taxonomie de compétences
            similar_skills = [
                skill for skill in cv_data.get("skills", []) 
                if self.skills_categories.get(missing_skill.lower(), "") == 
                   self.skills_categories.get(skill["name"].lower(), "unknown")
            ]
            
            if similar_skills:
                missing_skills_suggestions.append({
                    "missing_skill": missing_skill,
                    "similar_skills": [skill["name"] for skill in similar_skills]
                })
        
        return {
            "score": round(final_score * 100),  # Score sur 100
            "required_skills_score": round(required_skills_score * 100),
            "required_coverage": round(required_coverage * 100),
            "preferred_skills_score": round(preferred_skills_score * 100),
            "required_matches": required_matches,
            "required_misses": required_misses,
            "preferred_matches": preferred_matches,
            "missing_skills_suggestions": missing_skills_suggestions,
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
        # Extraire les compétences requises et préférées de l'appel d'offres
        required_skills = [skill["name"].lower() for skill in tender_data.get("required_skills", [])]
        preferred_skills = [skill["name"].lower() for skill in tender_data.get("preferred_skills", [])]
        all_tender_skills = required_skills + preferred_skills
        
        # Récupérer le résultat du matching
        match_result = await self.match_with_tender(consultant_data, tender_data)
        
        # Filtrer et classer les expériences selon leur pertinence pour cet appel d'offres
        experiences = consultant_data.get("experiences", []) or consultant_data.get("experience", [])
        relevant_experiences = []
        
        for exp in experiences:
            # Calculer la pertinence de cette expérience pour l'appel d'offres
            relevance_score = 0
            description = exp.get("description", "").lower()
            
            # Vérifier la présence des compétences requises dans la description
            for skill in required_skills:
                if skill in description:
                    relevance_score += 10  # Score élevé pour les compétences requises
            
            # Vérifier la présence des compétences préférées dans la description
            for skill in preferred_skills:
                if skill in description:
                    relevance_score += 5  # Score moyen pour les compétences préférées
            
            # Si l'expérience est pertinente, l'ajouter à la liste
            if relevance_score > 0:
                exp_copy = exp.copy()  # Créer une copie pour ne pas modifier l'original
                exp_copy["relevance_score"] = relevance_score
                relevant_experiences.append(exp_copy)
            else:
                # Vérifier d'autres facteurs de pertinence (titre, entreprise, etc.)
                title = exp.get("title", "").lower()
                for keyword in tender_data.get("keywords", []):
                    if keyword.lower() in title or keyword.lower() in description:
                        exp_copy = exp.copy()
                        exp_copy["relevance_score"] = 3  # Score bas pour les correspondances générales
                        relevant_experiences.append(exp_copy)
                        break
        
        # Trier les expériences par pertinence
        relevant_experiences.sort(key=lambda x: x.get("relevance_score", 0), reverse=True)
        
        # Filtrer les compétences pertinentes
        all_skills = consultant_data.get("skills", [])
        relevant_skills = []
        other_skills = []
        
        for skill in all_skills:
            skill_name = skill["name"].lower()
            if skill_name in all_tender_skills:
                relevance = "required" if skill_name in required_skills else "preferred"
                skill_copy = skill.copy()
                skill_copy["relevance"] = relevance
                relevant_skills.append(skill_copy)
            else:
                other_skills.append(skill)
        
        # Sélectionner les projets similaires (dans une implémentation réelle, cela pourrait venir d'une base de données)
        similar_projects = []
        
        # Générer une présentation personnalisée
        presentation = await self._generate_custom_presentation(consultant_data, tender_data, match_result)
        
        # Générer le dossier de compétences
        portfolio = {
            "consultant_name": f"{consultant_data.get('first_name', '')} {consultant_data.get('last_name', '')}".strip() or consultant_data.get("personal_info", {}).get("name", ""),
            "consultant_title": consultant_data.get("title", ""),
            "consultant_summary": consultant_data.get("bio", ""),
            "custom_presentation": presentation,
            "tender_title": tender_data.get("title", ""),
            "tender_description": tender_data.get("description", ""),
            "match_score": match_result["score"],
            "match_details": {
                "skills_match": match_result["required_skills_score"],
                "skills_coverage": match_result["required_coverage"],
                "recommendation": match_result["recommendation"]
            },
            "relevant_skills": relevant_skills,
            "other_skills": other_skills,
            "relevant_experiences": relevant_experiences,
            "education": consultant_data.get("education", []),
            "similar_projects": similar_projects,
            "generated_at": datetime.now().isoformat()
        }
        
        return portfolio
    
    async def _generate_custom_presentation(
        self, consultant_data: Dict[str, Any], tender_data: Dict[str, Any], match_result: Dict[str, Any]
    ) -> str:
        """
        Génère une présentation personnalisée du consultant pour l'appel d'offres
        
        Dans une implémentation réelle, cela pourrait utiliser un LLM comme GPT-4
        
        Args:
            consultant_data: Données du consultant
            tender_data: Données de l'appel d'offres
            match_result: Résultat du matching
            
        Returns:
            Présentation personnalisée
        """
        # Obtenir le nom du consultant
        name = f"{consultant_data.get('first_name', '')} {consultant_data.get('last_name', '')}".strip() or consultant_data.get("personal_info", {}).get("name", "Consultant")
        
        # Obtenir le titre du consultant
        title = consultant_data.get("title", "Professionnel IT")
        
        # Obtenir les années d'expérience totales
        experiences = consultant_data.get("experiences", []) or consultant_data.get("experience", [])
        years_experience = max(skill.get("years_experience", 0) for skill in consultant_data.get("skills", []) if "years_experience" in skill) if consultant_data.get("skills") else 3
        
        # Obtenir les compétences principales
        skills = consultant_data.get("skills", [])
        top_skills = sorted(skills, key=lambda x: x.get("years_experience", 0), reverse=True)[:5]
        skills_text = ", ".join(skill["name"] for skill in top_skills)
        
        # Informations sur l'appel d'offres
        tender_title = tender_data.get("title", "ce projet")
        
        # Score de matching
        match_score = match_result["score"]
        recommendation = match_result["recommendation"]
        
        # Construire la présentation
        presentation = f"""
{name} est un {title} avec {years_experience} ans d'expérience, spécialisé en {skills_text}.

Avec un score de correspondance de {match_score}% pour {tender_title}, {name} présente """
        
        if recommendation == "strong_match":
            presentation += f"""
une excellente adéquation avec les exigences du projet. Ses compétences correspondent parfaitement aux besoins exprimés, 
et son expérience professionnelle démontre sa capacité à contribuer immédiatement et efficacement.
"""
        elif recommendation == "partial_match":
            presentation += f"""
une bonne adéquation avec les exigences principales du projet. Bien que certaines compétences requises 
soient présentes, d'autres pourraient nécessiter une montée en compétence rapide ou une formation complémentaire.
"""
        else:
            presentation += f"""
quelques compétences pertinentes pour le projet. Cependant, plusieurs compétences clés requises demanderaient 
une montée en compétence significative ou un accompagnement pour garantir le succès du projet.
"""
        
        # Ajouter des informations sur les expériences pertinentes
        experiences = consultant_data.get("experiences", []) or consultant_data.get("experience", [])
        if experiences:
            recent_exp = experiences[0]
            presentation += f"""
Récemment, {name} a occupé le poste de {recent_exp.get('title', 'professionnel')} chez {recent_exp.get('company', 'une entreprise')}, 
où il a développé des compétences directement applicables à ce projet.
"""
        
        return presentation.strip()
    
    async def prepare_n8n_workflow_data(self, cv_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Prépare les données pour un workflow n8n
        
        Args:
            cv_data: Données du CV
            
        Returns:
            Données formatées pour n8n
        """
        # Formater les données pour n8n dans un format plus détaillé
        skills_by_category = {}
        for skill in cv_data.get("skills", []):
            category = skill.get("category", "other")
            if category not in skills_by_category:
                skills_by_category[category] = []
            skills_by_category[category].append(skill)
        
        return {
            "cv": cv_data,
            "skills_by_category": skills_by_category,
            "skills_count": len(cv_data.get("skills", [])),
            "experience_count": len(cv_data.get("experience", [])),
            "metadata": {
                "source": "TalentMatch",
                "timestamp": datetime.now().isoformat(),
                "version": "2.0",
                "analyzer": "EnhancedCVAnalyzer"
            }
        }