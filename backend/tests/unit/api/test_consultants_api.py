import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from fastapi import HTTPException, status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.main import app
from app.api.v1.consultants import router, get_consultant_use_case
from app.core.entities.consultant import ConsultantCreate, ConsultantResponse
from app.core.entities.enums import AvailabilityStatus

# Mock pour get_db
async def override_get_db():
    return MagicMock(spec=Session)

# Mock pour get_consultant_use_case
async def override_get_consultant_use_case():
    return AsyncMock()

@pytest.fixture
def test_client():
    """Crée un client de test pour l'API FastAPI."""
    # Remplacer les dépendances
    app.dependency_overrides[get_consultant_use_case] = override_get_consultant_use_case
    client = TestClient(app)
    yield client
    app.dependency_overrides = {}

@pytest.mark.asyncio
async def test_create_consultant_api_success():
    """
    Test de création d'un consultant via l'API avec succès.
    """
    # Arrange
    consultant_data = {
        "company_id": 1,
        "title": "Développeur Java",
        "user_id": 1,
        "photo_url": "https://minio.example.com/profiles/photo.jpg",
        "availability_status": "available"
    }
    
    # Simuler la réponse du use case
    mock_response = MagicMock()
    mock_response.id = 99
    mock_response.company_id = 1
    mock_response.title = "Développeur Java"
    mock_response.user_id = 1
    mock_response.photo_url = "https://minio.example.com/profiles/photo.jpg"
    mock_response.availability_status = AvailabilityStatus.AVAILABLE
    
    # Créer un client de test avec des mocks
    client = TestClient(app)
    
    with patch('app.api.v1.consultants.get_consultant_use_case') as mock_get_use_case:
        # Configuration du mock
        mock_use_case = AsyncMock()
        mock_use_case.create_consultant.return_value = mock_response
        mock_get_use_case.return_value = mock_use_case
        
        # Act
        response = client.post("/api/consultants", json=consultant_data)
        
        # Assert
        assert response.status_code == 201
        mock_use_case.create_consultant.assert_called_once()

@pytest.mark.asyncio
async def test_create_consultant_api_validation_error():
    """
    Test de création d'un consultant via l'API avec des données invalides.
    """
    # Arrange - données manquantes
    invalid_data = {
        "company_id": 1,
        # Titre manquant
        "user_id": 1
    }
    
    # Créer un client de test
    client = TestClient(app)
    
    # Act
    response = client.post("/api/consultants", json=invalid_data)
    
    # Assert
    assert response.status_code == 422  # Validation error

@pytest.mark.asyncio
async def test_create_consultant_api_server_error():
    """
    Test de création d'un consultant via l'API avec une erreur serveur.
    """
    # Arrange
    consultant_data = {
        "company_id": 1,
        "title": "Développeur Java",
        "user_id": 1,
        "photo_url": "https://minio.example.com/profiles/photo.jpg",
        "availability_status": "available"
    }
    
    # Créer un client de test avec des mocks
    client = TestClient(app)
    
    with patch('app.api.v1.consultants.get_consultant_use_case') as mock_get_use_case:
        # Configuration du mock pour lever une exception
        mock_use_case = AsyncMock()
        mock_use_case.create_consultant.side_effect = Exception("Erreur interne du serveur")
        mock_get_use_case.return_value = mock_use_case
        
        # Act
        response = client.post("/api/consultants", json=consultant_data)
        
        # Assert
        assert response.status_code == 500
        mock_use_case.create_consultant.assert_called_once()

@pytest.mark.asyncio
async def test_get_consultant_by_id_success():
    """
    Test de récupération d'un consultant par son ID avec succès.
    """
    # Arrange
    consultant_id = 1
    
    # Simuler la réponse du use case
    mock_response = MagicMock()
    mock_response.id = consultant_id
    mock_response.title = "Développeur Java"
    mock_response.photo_url = "https://minio.example.com/profiles/photo.jpg"
    
    # Créer un client de test avec des mocks
    client = TestClient(app)
    
    with patch('app.api.v1.consultants.get_consultant_use_case') as mock_get_use_case:
        # Configuration du mock
        mock_use_case = AsyncMock()
        mock_use_case.get_consultant_by_id.return_value = mock_response
        mock_get_use_case.return_value = mock_use_case
        
        # Act
        response = client.get(f"/api/consultants/{consultant_id}")
        
        # Assert
        assert response.status_code == 200
        mock_use_case.get_consultant_by_id.assert_called_once_with(consultant_id)

@pytest.mark.asyncio
async def test_get_consultant_not_found():
    """
    Test de récupération d'un consultant qui n'existe pas.
    """
    # Arrange
    consultant_id = 999
    
    # Créer un client de test avec des mocks
    client = TestClient(app)
    
    with patch('app.api.v1.consultants.get_consultant_use_case') as mock_get_use_case:
        # Configuration du mock pour retourner None
        mock_use_case = AsyncMock()
        mock_use_case.get_consultant_by_id.return_value = None
        mock_get_use_case.return_value = mock_use_case
        
        # Act
        response = client.get(f"/api/consultants/{consultant_id}")
        
        # Assert
        assert response.status_code == 404
        mock_use_case.get_consultant_by_id.assert_called_once_with(consultant_id)

@pytest.mark.asyncio
async def test_update_consultant_photo_url():
    """
    Test de mise à jour de la photo de profil d'un consultant.
    """
    # Arrange
    consultant_id = 1
    update_data = {
        "photo_url": "https://minio.example.com/profiles/new_photo.jpg"
    }
    
    # Simuler la réponse du use case
    mock_response = MagicMock()
    mock_response.id = consultant_id
    mock_response.photo_url = update_data["photo_url"]
    
    # Créer un client de test avec des mocks
    client = TestClient(app)
    
    with patch('app.api.v1.consultants.get_consultant_use_case') as mock_get_use_case:
        # Configuration du mock
        mock_use_case = AsyncMock()
        mock_use_case.update_consultant.return_value = mock_response
        mock_get_use_case.return_value = mock_use_case
        
        # Act
        response = client.put(f"/api/consultants/{consultant_id}", json=update_data)
        
        # Assert
        assert response.status_code == 200
        assert response.json()["photo_url"] == update_data["photo_url"]
        mock_use_case.update_consultant.assert_called_once()