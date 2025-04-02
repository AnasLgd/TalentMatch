from typing import Dict, Any, Optional, List
import requests
import json
import os
from fastapi import HTTPException, status

from app.core.interfaces.n8n_integration_service import N8nIntegrationService
from app.core.config import settings

class N8nWorkflowService(N8nIntegrationService):
    """
    Service d'intégration avec n8n pour l'exécution de workflows
    """
    
    def __init__(self):
        self.n8n_base_url = f"http://{settings.N8N_HOST}:{settings.N8N_PORT}"
        self.api_key = settings.N8N_API_KEY
        self.headers = {
            "Content-Type": "application/json"
        }
        
        # Ajouter l'API key si elle est configurée
        if self.api_key:
            self.headers["X-N8N-API-KEY"] = self.api_key
    
    async def execute_workflow(self, workflow_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Exécute un workflow n8n avec les données fournies
        
        Args:
            workflow_id: Identifiant du workflow à exécuter
            data: Données à passer au workflow
            
        Returns:
            Résultat de l'exécution du workflow
        """
        url = f"{self.n8n_base_url}/api/v1/workflows/{workflow_id}/execute"
        
        try:
            response = requests.post(
                url,
                headers=self.headers,
                json={"data": data}
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Erreur lors de l'exécution du workflow n8n: {response.text}"
                )
        except requests.RequestException as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erreur de connexion à n8n: {str(e)}"
            )
    
    async def trigger_webhook(self, webhook_url: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Déclenche un webhook n8n avec les données fournies
        
        Args:
            webhook_url: URL du webhook à déclencher
            data: Données à passer au webhook
            
        Returns:
            Résultat du déclenchement du webhook
        """
        try:
            response = requests.post(
                webhook_url,
                headers=self.headers,
                json=data
            )
            
            if response.status_code in [200, 201]:
                return response.json()
            else:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Erreur lors du déclenchement du webhook n8n: {response.text}"
                )
        except requests.RequestException as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erreur de connexion au webhook n8n: {str(e)}"
            )
    
    async def get_workflows(self) -> List[Dict[str, Any]]:
        """
        Récupère la liste des workflows n8n disponibles
        
        Returns:
            Liste des workflows n8n
        """
        url = f"{self.n8n_base_url}/api/v1/workflows"
        
        try:
            response = requests.get(
                url,
                headers=self.headers
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Erreur lors de la récupération des workflows n8n: {response.text}"
                )
        except requests.RequestException as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erreur de connexion à n8n: {str(e)}"
            )
    
    async def get_workflow(self, workflow_id: str) -> Dict[str, Any]:
        """
        Récupère les détails d'un workflow n8n
        
        Args:
            workflow_id: Identifiant du workflow à récupérer
            
        Returns:
            Détails du workflow n8n
        """
        url = f"{self.n8n_base_url}/api/v1/workflows/{workflow_id}"
        
        try:
            response = requests.get(
                url,
                headers=self.headers
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Erreur lors de la récupération du workflow n8n: {response.text}"
                )
        except requests.RequestException as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erreur de connexion à n8n: {str(e)}"
            )
    
    async def create_workflow(self, workflow_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Crée un nouveau workflow n8n
        
        Args:
            workflow_data: Données du workflow à créer
            
        Returns:
            Détails du workflow n8n créé
        """
        url = f"{self.n8n_base_url}/api/v1/workflows"
        
        try:
            response = requests.post(
                url,
                headers=self.headers,
                json=workflow_data
            )
            
            if response.status_code in [200, 201]:
                return response.json()
            else:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Erreur lors de la création du workflow n8n: {response.text}"
                )
        except requests.RequestException as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erreur de connexion à n8n: {str(e)}"
            )
    
    async def update_workflow(self, workflow_id: str, workflow_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Met à jour un workflow n8n existant
        
        Args:
            workflow_id: Identifiant du workflow à mettre à jour
            workflow_data: Nouvelles données du workflow
            
        Returns:
            Détails du workflow n8n mis à jour
        """
        url = f"{self.n8n_base_url}/api/v1/workflows/{workflow_id}"
        
        try:
            response = requests.put(
                url,
                headers=self.headers,
                json=workflow_data
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Erreur lors de la mise à jour du workflow n8n: {response.text}"
                )
        except requests.RequestException as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erreur de connexion à n8n: {str(e)}"
            )
    
    async def delete_workflow(self, workflow_id: str) -> bool:
        """
        Supprime un workflow n8n
        
        Args:
            workflow_id: Identifiant du workflow à supprimer
            
        Returns:
            True si la suppression a réussi, False sinon
        """
        url = f"{self.n8n_base_url}/api/v1/workflows/{workflow_id}"
        
        try:
            response = requests.delete(
                url,
                headers=self.headers
            )
            
            if response.status_code in [200, 204]:
                return True
            else:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Erreur lors de la suppression du workflow n8n: {response.text}"
                )
        except requests.RequestException as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erreur de connexion à n8n: {str(e)}"
            )
    
    async def get_workflow_executions(self, workflow_id: str) -> List[Dict[str, Any]]:
        """
        Récupère les exécutions d'un workflow n8n
        
        Args:
            workflow_id: Identifiant du workflow
            
        Returns:
            Liste des exécutions du workflow
        """
        url = f"{self.n8n_base_url}/api/v1/executions"
        
        try:
            response = requests.get(
                url,
                headers=self.headers,
                params={"workflowId": workflow_id}
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Erreur lors de la récupération des exécutions du workflow n8n: {response.text}"
                )
        except requests.RequestException as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erreur de connexion à n8n: {str(e)}"
            )
    
    async def get_execution(self, execution_id: str) -> Dict[str, Any]:
        """
        Récupère les détails d'une exécution de workflow n8n
        
        Args:
            execution_id: Identifiant de l'exécution
            
        Returns:
            Détails de l'exécution
        """
        url = f"{self.n8n_base_url}/api/v1/executions/{execution_id}"
        
        try:
            response = requests.get(
                url,
                headers=self.headers
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Erreur lors de la récupération de l'exécution du workflow n8n: {response.text}"
                )
        except requests.RequestException as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erreur de connexion à n8n: {str(e)}"
            )
    
    async def process_cv(self, cv_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Traite un CV via un workflow n8n
        
        Args:
            cv_data: Données du CV à traiter
            
        Returns:
            Résultat du traitement du CV
        """
        # Identifiant du workflow d'analyse de CV (à configurer dans n8n)
        workflow_id = os.getenv("N8N_CV_ANALYSIS_WORKFLOW_ID", "1")
        
        return await self.execute_workflow(workflow_id, cv_data)
    
    async def match_consultant_with_tenders(self, consultant_id: int) -> List[Dict[str, Any]]:
        """
        Trouve les appels d'offres qui correspondent à un consultant via un workflow n8n
        
        Args:
            consultant_id: Identifiant du consultant
            
        Returns:
            Liste des appels d'offres correspondants
        """
        # Identifiant du workflow de matching (à configurer dans n8n)
        workflow_id = os.getenv("N8N_MATCHING_WORKFLOW_ID", "2")
        
        result = await self.execute_workflow(workflow_id, {"consultant_id": consultant_id})
        return result.get("matches", [])
    
    async def find_consultants_for_tender(self, tender_id: int) -> List[Dict[str, Any]]:
        """
        Trouve les consultants qui correspondent à un appel d'offres via un workflow n8n
        
        Args:
            tender_id: Identifiant de l'appel d'offres
            
        Returns:
            Liste des consultants correspondants
        """
        # Identifiant du workflow de matching (à configurer dans n8n)
        workflow_id = os.getenv("N8N_MATCHING_WORKFLOW_ID", "2")
        
        result = await self.execute_workflow(workflow_id, {"tender_id": tender_id})
        return result.get("matches", [])
    
    async def initiate_collaboration(self, initiator_company_id: int, partner_company_id: int, 
                                   terms: Dict[str, Any]) -> Dict[str, Any]:
        """
        Initie une collaboration entre deux entreprises via un workflow n8n
        
        Args:
            initiator_company_id: Identifiant de l'entreprise initiatrice
            partner_company_id: Identifiant de l'entreprise partenaire
            terms: Termes de la collaboration
            
        Returns:
            Détails de la collaboration initiée
        """
        # Identifiant du workflow de collaboration (à configurer dans n8n)
        workflow_id = os.getenv("N8N_COLLABORATION_WORKFLOW_ID", "3")
        
        data = {
            "initiator_company_id": initiator_company_id,
            "partner_company_id": partner_company_id,
            "terms": terms
        }
        
        return await self.execute_workflow(workflow_id, data)
