from typing import Protocol, List, Optional, Dict, Any

class N8nIntegrationService(Protocol):
    """
    Service pour l'intégration avec n8n
    Préparation pour les agents IA maison cloisonnés en mode premium
    """
    
    async def initialize_workflow_engine(self) -> bool:
        """
        Initialise le moteur de workflow n8n intégré
        """
        ...
    
    async def register_workflow(self, workflow_name: str, workflow_definition: Dict[str, Any]) -> str:
        """
        Enregistre un nouveau workflow dans n8n
        Retourne l'identifiant du workflow
        """
        ...
    
    async def execute_workflow(self, workflow_id: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Exécute un workflow n8n avec les données d'entrée spécifiées
        """
        ...
    
    async def get_workflow_status(self, execution_id: str) -> Dict[str, Any]:
        """
        Récupère le statut d'exécution d'un workflow
        """
        ...
    
    async def create_cv_analysis_workflow(self) -> str:
        """
        Crée un workflow d'analyse de CV dans n8n
        Utilisé pour le mode premium avec agents IA maison
        """
        ...
    
    async def create_matchmaking_workflow(self) -> str:
        """
        Crée un workflow de matchmaking dans n8n
        Utilisé pour le mode premium avec agents IA maison
        """
        ...
