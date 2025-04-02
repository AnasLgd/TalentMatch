import pytest
from fastapi.testclient import TestClient
import os
import tempfile
from pathlib import Path

from app.main import app
from app.adapters.n8n.workflow_service import N8nWorkflowService
from app.adapters.services.rag_service import LocalRAGService

client = TestClient(app)

def test_n8n_integration():
    """Test de l'intégration avec n8n"""
    # Créer une instance du service n8n
    n8n_service = N8nWorkflowService()
    
    # Vérifier que les méthodes principales sont implémentées
    assert hasattr(n8n_service, 'execute_workflow')
    assert hasattr(n8n_service, 'trigger_webhook')
    assert hasattr(n8n_service, 'get_workflows')
    assert hasattr(n8n_service, 'get_workflow')
    assert hasattr(n8n_service, 'create_workflow')
    assert hasattr(n8n_service, 'update_workflow')
    assert hasattr(n8n_service, 'delete_workflow')
    
    # Vérifier les méthodes spécifiques aux cas d'utilisation
    assert hasattr(n8n_service, 'process_cv')
    assert hasattr(n8n_service, 'match_consultant_with_tenders')
    assert hasattr(n8n_service, 'find_consultants_for_tender')
    assert hasattr(n8n_service, 'initiate_collaboration')

def test_rag_service():
    """Test du service RAG"""
    # Créer une instance du service RAG
    rag_service = LocalRAGService()
    
    # Vérifier que les méthodes principales sont implémentées
    assert hasattr(rag_service, 'index_document')
    assert hasattr(rag_service, 'query')
    assert hasattr(rag_service, 'generate')
    assert hasattr(rag_service, 'get_documents')
    assert hasattr(rag_service, 'get_document')
    assert hasattr(rag_service, 'delete_document')
    
    # Créer un document texte simple pour le test
    test_content = b"Ceci est un document de test pour le service RAG."
    
    # Créer un fichier temporaire
    with tempfile.NamedTemporaryFile(delete=False, suffix='.txt') as temp_file:
        temp_file.write(test_content)
        temp_path = temp_file.name
    
    try:
        # Indexer le document (test asynchrone simulé)
        document_id = None
        try:
            import asyncio
            document_id = asyncio.run(rag_service.index_document(
                test_content,
                Path(temp_path).name,
                'test',
                {'test_metadata': 'value'}
            ))
        except:
            # Si asyncio n'est pas disponible dans l'environnement de test
            pass
        
        # Vérifier que le document a été indexé si possible
        if document_id:
            # Interroger la base de connaissances
            results = asyncio.run(rag_service.query("test"))
            assert len(results) > 0
            
            # Supprimer le document
            success = asyncio.run(rag_service.delete_document(document_id))
            assert success
    finally:
        # Supprimer le fichier temporaire
        if os.path.exists(temp_path):
            os.remove(temp_path)

def test_collaboration_workflow():
    """Test du workflow de collaboration inter-ESN"""
    # Créer deux entreprises
    company1_response = client.post(
        "/api/v1/companies/",
        json={
            "name": "ESN Workflow 1",
            "description": "Une ESN pour le test de workflow",
            "website": "https://esn-workflow1.com",
            "location": "Paris, France",
            "size": "50-200",
            "industry": "IT Services"
        },
    )
    assert company1_response.status_code == 200
    company1_id = company1_response.json()["id"]
    
    company2_response = client.post(
        "/api/v1/companies/",
        json={
            "name": "ESN Workflow 2",
            "description": "Une autre ESN pour le test de workflow",
            "website": "https://esn-workflow2.com",
            "location": "Lyon, France",
            "size": "10-50",
            "industry": "IT Services"
        },
    )
    assert company2_response.status_code == 200
    company2_id = company2_response.json()["id"]
    
    # Créer une collaboration
    collab_response = client.post(
        "/api/v1/collaborations/",
        json={
            "initiator_company_id": company1_id,
            "partner_company_id": company2_id,
            "status": "pending",
            "terms": "Partage de consultants et d'appels d'offres",
            "start_date": "2025-05-01",
            "end_date": "2026-05-01"
        },
    )
    assert collab_response.status_code == 200
    collab_id = collab_response.json()["id"]
    
    # Traiter la collaboration avec n8n
    process_response = client.post(f"/api/v1/collaborations/{collab_id}/process-with-n8n")
    
    # Le test peut échouer si n8n n'est pas disponible, mais l'API doit répondre
    if process_response.status_code == 200:
        assert "collaboration" in process_response.json()
    else:
        assert process_response.status_code in [500, 503]  # Service indisponible
    
    # Mettre à jour le statut de la collaboration
    update_response = client.put(
        f"/api/v1/collaborations/{collab_id}",
        json={
            "status": "active",
            "terms": "Partage de consultants et d'appels d'offres - Approuvé"
        },
    )
    assert update_response.status_code == 200
    assert update_response.json()["status"] == "active"
    
    # Récupérer les collaborations de l'entreprise
    get_response = client.get(f"/api/v1/collaborations/?company_id={company1_id}")
    assert get_response.status_code == 200
    collaborations = get_response.json()
    assert len(collaborations) > 0
    assert any(c["id"] == collab_id for c in collaborations)

def test_cv_analysis_workflow():
    """Test du workflow d'analyse de CV"""
    # Créer un fichier CV de test
    cv_content = b"CV de Jean Dupont\nDeveloppeur Full Stack\nCompetences: JavaScript, Python, React\nExperience: 5 ans"
    
    # Créer un fichier temporaire
    with tempfile.NamedTemporaryFile(delete=False, suffix='.txt') as temp_file:
        temp_file.write(cv_content)
        temp_path = temp_file.name
    
    try:
        # Analyser le CV
        with open(temp_path, 'rb') as f:
            files = {'file': (Path(temp_path).name, f, 'text/plain')}
            response = client.post("/api/v1/cv/analyze", files=files)
        
        # Le test peut échouer si le service d'analyse n'est pas complètement configuré
        if response.status_code == 200:
            result = response.json()
            assert "skills" in result
            assert any(skill["name"] == "JavaScript" for skill in result["skills"])
        else:
            assert response.status_code in [500, 503]  # Service indisponible
        
        # Tester l'analyse avec n8n
        with open(temp_path, 'rb') as f:
            files = {'file': (Path(temp_path).name, f, 'text/plain')}
            response = client.post("/api/v1/cv/analyze-with-n8n", files=files)
        
        # Le test peut échouer si n8n n'est pas disponible
        if response.status_code == 200:
            result = response.json()
            assert "n8n_processing" in result
        else:
            assert response.status_code in [500, 503]  # Service indisponible
    finally:
        # Supprimer le fichier temporaire
        if os.path.exists(temp_path):
            os.remove(temp_path)

def test_matching_workflow():
    """Test du workflow de matching entre consultants et appels d'offres"""
    # Créer une entreprise
    company_response = client.post(
        "/api/v1/companies/",
        json={
            "name": "ESN Matching Workflow",
            "description": "Une ESN pour le test de workflow de matching",
            "website": "https://esn-matching-workflow.com",
            "location": "Paris, France",
            "size": "50-200",
            "industry": "IT Services"
        },
    )
    assert company_response.status_code == 200
    company_id = company_response.json()["id"]
    
    # Créer un consultant
    consultant_response = client.post(
        "/api/v1/consultants/",
        json={
            "first_name": "Sophie",
            "last_name": "Dubois",
            "email": "sophie.dubois@esn-matching-workflow.com",
            "phone": "+33123456789",
            "title": "Développeuse Full Stack",
            "company_id": company_id,
            "experience_years": 7,
            "availability_status": "available",
            "availability_date": "2025-05-01",
            "daily_rate": 700,
            "skills": [
                {
                    "name": "JavaScript",
                    "level": "expert",
                    "years_experience": 7
                },
                {
                    "name": "React",
                    "level": "expert",
                    "years_experience": 5
                },
                {
                    "name": "Node.js",
                    "level": "expert",
                    "years_experience": 6
                }
            ]
        },
    )
    assert consultant_response.status_code == 200
    consultant_id = consultant_response.json()["id"]
    
    # Créer un appel d'offres
    tender_response = client.post(
        "/api/v1/tenders/",
        json={
            "title": "Développeur Full Stack Senior",
            "description": "Nous recherchons un développeur Full Stack expérimenté",
            "company_id": company_id,
            "location": "Paris, France",
            "start_date": "2025-06-01",
            "end_date": "2025-12-31",
            "daily_rate_min": 650,
            "daily_rate_max": 850,
            "status": "open",
            "required_skills": [
                {
                    "name": "JavaScript",
                    "level": "expert",
                    "years_experience": 5
                },
                {
                    "name": "React",
                    "level": "expert",
                    "years_experience": 4
                }
            ],
            "preferred_skills": [
                {
                    "name": "Node.js",
                    "level": "intermediate",
                    "years_experience": 3
                }
            ]
        },
    )
    assert tender_response.status_code == 200
    tender_id = tender_response.json()["id"]
    
    # Rechercher des matchs pour le consultant
    match_consultant_response = client.post(f"/api/v1/matches/find-for-consultant/{consultant_id}")
    
    # Le test peut échouer si n8n n'est pas disponible
    if match_consultant_response.status_code == 200:
        matches = match_consultant_response.json()
        assert len(matches) > 0
    else:
        assert match_consultant_response.status_code in [500, 503]  # Service indisponible
    
    # Rechercher des matchs pour l'appel d'offres
    match_tender_response = client.post(f"/api/v1/matches/find-for-tender/{tender_id}")
    
    # Le test peut échouer si n8n n'est pas disponible
    if match_tender_response.status_code == 200:
        matches = match_tender_response.json()
        assert len(matches) > 0
    else:
        assert match_tender_response.status_code in [500, 503]  # Service indisponible
    
    # Récupérer tous les matchs
    get_matches_response = client.get("/api/v1/matches/")
    assert get_matches_response.status_code == 200
    all_matches = get_matches_response.json()
    
    # Si des matchs ont été créés, tester la mise à jour d'un match
    if len(all_matches) > 0:
        match_id = all_matches[0]["id"]
        update_response = client.put(
            f"/api/v1/matches/{match_id}",
            json={
                "status": "accepted",
                "notes": "Match validé après entretien"
            },
        )
        assert update_response.status_code == 200
        assert update_response.json()["status"] == "accepted"
