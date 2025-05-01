import sys
import os
from pathlib import Path
import json
from datetime import datetime

# Ajout du répertoire parent au sys.path pour permettre l'import des modules
sys.path.append(str(Path(__file__).parent.parent))

# Import des modules de journalisation et de suivi de développement
from logs.init_logging import setup_logging, log_development_activity
from logs.development_tracker import DevelopmentTracker, TaskStatus, TaskPriority

# Configuration du système de journalisation
loggers = setup_logging()
dev_logger = loggers['dev']
error_logger = loggers['error']
audit_logger = loggers['audit']

# Initialisation du tracker de développement
tracker = DevelopmentTracker()

class UserStoryAnalyzer:
    def __init__(self, analysis_file='/projects/TalentMatch/logs/user_story_analysis.json'):
        self.analysis_file = analysis_file
        self.analyses = self._load_analyses()
        
    def _load_analyses(self):
        if os.path.exists(self.analysis_file):
            with open(self.analysis_file, 'r') as f:
                return json.load(f)
        else:
            # Initialiser avec une structure vide
            initial_data = {
                "user_stories": {},
                "last_updated": datetime.now().isoformat()
            }
            self._save_analyses(initial_data)
            return initial_data
    
    def _save_analyses(self, data):
        data["last_updated"] = datetime.now().isoformat()
        with open(self.analysis_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def add_user_story_analysis(self, user_story_id, title, description, acceptance_criteria, 
                                technical_requirements, dependencies=None, risks=None, notes=None):
        """
        Ajoute une analyse détaillée d'une user story
        
        Args:
            user_story_id (str): Identifiant de la user story (ex: US1.2)
            title (str): Titre de la user story
            description (str): Description de la user story
            acceptance_criteria (list): Liste des critères d'acceptation
            technical_requirements (list): Liste des exigences techniques
            dependencies (list, optional): Liste des IDs des user stories dont celle-ci dépend
            risks (list, optional): Liste des risques identifiés
            notes (str, optional): Notes additionnelles
            
        Returns:
            bool: True si l'ajout a réussi
        """
        analysis = {
            "id": user_story_id,
            "title": title,
            "description": description,
            "acceptance_criteria": acceptance_criteria,
            "technical_requirements": technical_requirements,
            "dependencies": dependencies or [],
            "risks": risks or [],
            "notes": notes,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        
        self.analyses["user_stories"][user_story_id] = analysis
        self._save_analyses(self.analyses)
        
        log_development_activity(
            dev_logger,
            'analysis',
            f'Analyse de la user story {user_story_id}',
            {
                'user_story': user_story_id,
                'technical_requirements_count': len(technical_requirements),
                'risks_count': len(risks or [])
            }
        )
        
        print(f"Analyse de la user story {user_story_id} ajoutée avec succès.")
        return True
    
    def get_user_story_analysis(self, user_story_id):
        """
        Récupère l'analyse d'une user story par son ID
        
        Args:
            user_story_id (str): Identifiant de la user story
            
        Returns:
            dict: Analyse trouvée ou None
        """
        return self.analyses["user_stories"].get(user_story_id)
    
    def get_all_user_story_analyses(self):
        """
        Récupère toutes les analyses de user stories
        
        Returns:
            dict: Dictionnaire des analyses par ID de user story
        """
        return self.analyses["user_stories"]
    
    def update_user_story_analysis(self, user_story_id, updates):
        """
        Met à jour l'analyse d'une user story
        
        Args:
            user_story_id (str): Identifiant de la user story
            updates (dict): Dictionnaire des champs à mettre à jour
            
        Returns:
            bool: True si la mise à jour a réussi, False sinon
        """
        if user_story_id not in self.analyses["user_stories"]:
            print(f"User story {user_story_id} non trouvée")
            return False
        
        for key, value in updates.items():
            if key in self.analyses["user_stories"][user_story_id]:
                self.analyses["user_stories"][user_story_id][key] = value
        
        self.analyses["user_stories"][user_story_id]["updated_at"] = datetime.now().isoformat()
        self._save_analyses(self.analyses)
        
        log_development_activity(
            dev_logger,
            'analysis',
            f'Mise à jour de l\'analyse de la user story {user_story_id}',
            {
                'user_story': user_story_id,
                'updated_fields': list(updates.keys())
            }
        )
        
        print(f"Analyse de la user story {user_story_id} mise à jour avec succès.")
        return True

# Fonction pour initialiser les analyses des user stories prioritaires
def initialize_priority_user_stories():
    analyzer = UserStoryAnalyzer()
    
    # User Story US1.1: Création de profil consultant
    analyzer.add_user_story_analysis(
        user_story_id="US1.1",
        title="Création de profil consultant",
        description="En tant que Recruteur, je veux créer un profil pour un nouveau consultant afin de l'ajouter à notre base de talents",
        acceptance_criteria=[
            "Formulaire avec champs obligatoires (nom, prénom, titre, expérience)",
            "Possibilité d'ajouter une photo de profil",
            "Validation des données saisies",
            "Confirmation de création réussie"
        ],
        technical_requirements=[
            "Endpoint API pour la création de consultant",
            "Validation des données avec Pydantic et Zod",
            "Intégration avec le service de stockage pour les photos",
            "Formulaire React avec gestion d'erreurs",
            "Tests unitaires et d'intégration"
        ],
        dependencies=[],
        risks=[
            "Gestion des permissions et droits d'accès",
            "Performance lors du téléchargement de photos volumineuses"
        ],
        notes="Cette user story est fondamentale pour le MVP et doit être implémentée en priorité."
    )
    
    # User Story US1.2: Téléchargement et analyse de CV
    analyzer.add_user_story_analysis(
        user_story_id="US1.2",
        title="Téléchargement et analyse de CV",
        description="En tant que Recruteur, je veux télécharger le CV d'un consultant et obtenir une analyse automatique afin de gagner du temps sur la qualification",
        acceptance_criteria=[
            "Support des formats PDF, DOCX, DOC",
            "Extraction automatique des informations clés (expérience, formation, compétences)",
            "Interface de validation/correction des données extraites",
            "Intégration des données validées au profil du consultant"
        ],
        technical_requirements=[
            "Service d'extraction de texte des différents formats de CV",
            "Intégration avec l'agent IA maison pour l'analyse",
            "Stockage sécurisé des CV dans MinIO",
            "Interface utilisateur pour la validation et correction",
            "Workflows n8n pour l'orchestration du processus",
            "Tests d'intégration avec jeux de données variés"
        ],
        dependencies=["US1.1"],
        risks=[
            "Précision de l'extraction selon la structure du CV",
            "Performance de l'analyse pour des documents complexes",
            "Sécurité et confidentialité des données extraites",
            "Gestion des langues et formats internationaux"
        ],
        notes="Cette fonctionnalité est critique pour la proposition de valeur de TalentMatch et nécessite une attention particulière à la précision de l'extraction."
    )
    
    # User Story US2.1: Création d'appel d'offres
    analyzer.add_user_story_analysis(
        user_story_id="US2.1",
        title="Création d'appel d'offres",
        description="En tant que Commercial, je veux créer un nouvel appel d'offres afin de centraliser les informations et faciliter la recherche de consultants",
        acceptance_criteria=[
            "Formulaire avec champs obligatoires (titre, client, description, compétences requises)",
            "Possibilité de définir des dates de début/fin",
            "Définition du budget et du nombre de consultants requis",
            "Statut initial (ouvert)"
        ],
        technical_requirements=[
            "Modèle de données pour les appels d'offres",
            "Endpoint API pour la création",
            "Validation des données",
            "Formulaire React avec champs dynamiques pour les compétences",
            "Tests unitaires et fonctionnels"
        ],
        dependencies=[],
        risks=[
            "Confidentialité des informations client",
            "Complexité de la gestion des compétences requises"
        ],
        notes="Cette user story est complémentaire à la gestion des consultants et forme la base du système de matching."
    )
    
    # User Story US3.1: Matching automatique
    analyzer.add_user_story_analysis(
        user_story_id="US3.1",
        title="Matching automatique",
        description="En tant que Commercial, je veux que le système me propose automatiquement des consultants pour un appel d'offres afin de gagner du temps dans la recherche de profils adaptés",
        acceptance_criteria=[
            "Algorithme de matching basé sur les compétences, l'expérience et la disponibilité",
            "Score de correspondance pour chaque consultant",
            "Classement par pertinence",
            "Explication du score de matching"
        ],
        technical_requirements=[
            "Algorithme de scoring configurable",
            "Optimisation des requêtes pour performances",
            "Interface utilisateur pour afficher les résultats avec filtres",
            "Système d'explication du score",
            "API dédiée pour le matching",
            "Tests avec jeux de données variés"
        ],
        dependencies=["US1.1", "US2.1"],
        risks=[
            "Performance avec un grand nombre de consultants",
            "Pertinence des scores de matching",
            "Complexité de l'algorithme et maintenabilité"
        ],
        notes="Cette user story est au cœur de la proposition de valeur de TalentMatch et nécessite une attention particulière à l'algorithme de matching et à son évolutivité."
    )
    
    # User Story US4.1: Création de partenariats
    analyzer.add_user_story_analysis(
        user_story_id="US4.1",
        title="Création de partenariats",
        description="En tant que Directeur, je veux établir des partenariats avec d'autres ESN afin de collaborer sur des opportunités communes",
        acceptance_criteria=[
            "Invitation et validation des partenariats",
            "Définition des règles de collaboration",
            "Gestion des accords (dates de début/fin, termes)",
            "Tableau de bord des partenariats actifs"
        ],
        technical_requirements=[
            "Modèle de données pour les partenariats",
            "Système d'invitation par email",
            "Gestion des statuts de partenariat",
            "Interface utilisateur pour la gestion des partenariats",
            "API pour la création et gestion des partenariats",
            "Tests d'intégration du flux complet"
        ],
        dependencies=[],
        risks=[
            "Sécurité des données partagées entre ESN",
            "Complexité de la gestion des droits d'accès",
            "Conformité légale des partenariats"
        ],
        notes="Cette user story est fondamentale pour l'aspect collaboratif de la plateforme."
    )
    
    print("Analyses des user stories prioritaires initialisées avec succès.")

if __name__ == "__main__":
    print("Initialisation des analyses des user stories prioritaires...")
    initialize_priority_user_stories()
    
    # Afficher un résumé
    analyzer = UserStoryAnalyzer()
    analyses = analyzer.get_all_user_story_analyses()
    
    print("\n=== RÉSUMÉ DES ANALYSES DE USER STORIES ===")
    print(f"Nombre de user stories analysées: {len(analyses)}")
    
    for us_id, analysis in analyses.items():
        print(f"\n{us_id}: {analysis['title']}")
        print(f"  Exigences techniques: {len(analysis['technical_requirements'])}")
        print(f"  Risques identifiés: {len(analysis['risks'])}")
        print(f"  Dépendances: {', '.join(analysis['dependencies']) if analysis['dependencies'] else 'Aucune'}")
    
    print("\n===========================================")
