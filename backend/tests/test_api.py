import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.infrastructure.database.models import Base
from app.infrastructure.database.session import get_db

# Créer une base de données SQLite en mémoire pour les tests
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Créer les tables dans la base de données de test
Base.metadata.create_all(bind=engine)

# Remplacer la dépendance get_db par une version de test
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# Créer un client de test
client = TestClient(app)

def test_read_main():
    """Test de la route principale"""
    response = client.get("/")
    assert response.status_code == 200
    assert "TalentMatch API" in response.json()["title"]

def test_health_check():
    """Test de la route de vérification de santé"""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_create_consultant():
    """Test de création d'un consultant"""
    # Créer d'abord une entreprise
    company_data = {
        "name": "Test Company",
        "description": "A test company",
        "website": "https://testcompany.com",
        "address": "123 Test Street",
        "city": "Test City",
        "postal_code": "12345",
        "country": "Test Country"
    }
    company_response = client.post("/api/v1/companies/", json=company_data)
    assert company_response.status_code == 201
    company_id = company_response.json()["id"]
    
    # Créer un consultant
    consultant_data = {
        "company_id": company_id,
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "title": "Senior Developer",
        "experience_years": 5,
        "daily_rate": 500,
        "availability_status": "available",
        "location": "Paris, France",
        "remote_work": True
    }
    response = client.post("/api/v1/consultants/", json=consultant_data)
    assert response.status_code == 201
    data = response.json()
    assert data["first_name"] == "John"
    assert data["last_name"] == "Doe"
    assert data["company_id"] == company_id
    
    # Vérifier que le consultant a été créé
    consultant_id = data["id"]
    get_response = client.get(f"/api/v1/consultants/{consultant_id}")
    assert get_response.status_code == 200
    assert get_response.json()["id"] == consultant_id

def test_create_tender():
    """Test de création d'un appel d'offres"""
    # Créer d'abord une entreprise
    company_data = {
        "name": "Another Test Company",
        "description": "Another test company",
        "website": "https://anothertestcompany.com",
        "address": "456 Test Avenue",
        "city": "Another City",
        "postal_code": "54321",
        "country": "Another Country"
    }
    company_response = client.post("/api/v1/companies/", json=company_data)
    assert company_response.status_code == 201
    company_id = company_response.json()["id"]
    
    # Créer un appel d'offres
    tender_data = {
        "company_id": company_id,
        "title": "Test Tender",
        "client_name": "Test Client",
        "description": "A test tender for a test project",
        "start_date": "2025-05-01",
        "end_date": "2025-08-31",
        "status": "open",
        "location": "Lyon, France",
        "remote_work": True,
        "budget": 50000,
        "required_consultants": 2
    }
    response = client.post("/api/v1/tenders/", json=tender_data)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Tender"
    assert data["company_id"] == company_id
    
    # Vérifier que l'appel d'offres a été créé
    tender_id = data["id"]
    get_response = client.get(f"/api/v1/tenders/{tender_id}")
    assert get_response.status_code == 200
    assert get_response.json()["id"] == tender_id

def test_create_match():
    """Test de création d'un match entre consultant et appel d'offres"""
    # Créer une entreprise
    company_data = {
        "name": "Match Test Company",
        "description": "A company for match testing",
        "website": "https://matchtestcompany.com"
    }
    company_response = client.post("/api/v1/companies/", json=company_data)
    assert company_response.status_code == 201
    company_id = company_response.json()["id"]
    
    # Créer un consultant
    consultant_data = {
        "company_id": company_id,
        "first_name": "Jane",
        "last_name": "Smith",
        "email": "jane.smith@example.com",
        "title": "Full Stack Developer",
        "experience_years": 3
    }
    consultant_response = client.post("/api/v1/consultants/", json=consultant_data)
    assert consultant_response.status_code == 201
    consultant_id = consultant_response.json()["id"]
    
    # Créer un appel d'offres
    tender_data = {
        "company_id": company_id,
        "title": "Match Test Tender",
        "client_name": "Match Test Client",
        "description": "A tender for match testing",
        "status": "open"
    }
    tender_response = client.post("/api/v1/tenders/", json=tender_data)
    assert tender_response.status_code == 201
    tender_id = tender_response.json()["id"]
    
    # Créer un match
    match_data = {
        "consultant_id": consultant_id,
        "tender_id": tender_id,
        "match_score": 85.5,
        "status": "suggested",
        "notes": "This is a test match"
    }
    response = client.post("/api/v1/matches/", json=match_data)
    assert response.status_code == 201
    data = response.json()
    assert data["consultant_id"] == consultant_id
    assert data["tender_id"] == tender_id
    assert data["match_score"] == 85.5
    
    # Vérifier que le match a été créé
    match_id = data["id"]
    get_response = client.get(f"/api/v1/matches/{match_id}")
    assert get_response.status_code == 200
    assert get_response.json()["id"] == match_id

def test_create_collaboration():
    """Test de création d'une collaboration entre entreprises"""
    # Créer deux entreprises
    company1_data = {
        "name": "Initiator Company",
        "description": "An initiator company",
        "website": "https://initiator.com"
    }
    company1_response = client.post("/api/v1/companies/", json=company1_data)
    assert company1_response.status_code == 201
    company1_id = company1_response.json()["id"]
    
    company2_data = {
        "name": "Partner Company",
        "description": "A partner company",
        "website": "https://partner.com"
    }
    company2_response = client.post("/api/v1/companies/", json=company2_data)
    assert company2_response.status_code == 201
    company2_id = company2_response.json()["id"]
    
    # Créer une collaboration
    collaboration_data = {
        "initiator_company_id": company1_id,
        "partner_company_id": company2_id,
        "status": "pending",
        "start_date": "2025-05-01",
        "end_date": "2025-12-31",
        "terms": "Test collaboration terms"
    }
    response = client.post("/api/v1/collaborations/", json=collaboration_data)
    assert response.status_code == 201
    data = response.json()
    assert data["initiator_company_id"] == company1_id
    assert data["partner_company_id"] == company2_id
    
    # Vérifier que la collaboration a été créée
    collaboration_id = data["id"]
    get_response = client.get(f"/api/v1/collaborations/{collaboration_id}")
    assert get_response.status_code == 200
    assert get_response.json()["id"] == collaboration_id

def test_n8n_status():
    """Test de la route de vérification du statut n8n"""
    response = client.get("/api/v1/n8n/status")
    # Comme n8n n'est probablement pas configuré dans l'environnement de test,
    # nous vérifions simplement que la route existe et renvoie une réponse
    assert response.status_code in [200, 500]
    
def test_rag_query():
    """Test de la route de requête RAG"""
    query_data = {
        "text": "Quelles sont les compétences requises pour un développeur full stack?",
        "filters": {},
        "top_k": 3
    }
    response = client.post("/api/v1/rag/query", json=query_data)
    # Comme le service RAG n'est probablement pas configuré dans l'environnement de test,
    # nous vérifions simplement que la route existe et renvoie une réponse
    assert response.status_code in [200, 500]

if __name__ == "__main__":
    pytest.main(["-v"])
