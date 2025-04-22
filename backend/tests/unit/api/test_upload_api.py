import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from fastapi import UploadFile, File, status
from fastapi.testclient import TestClient
import io

from app.main import app
from app.api.v1.upload import router, ALLOWED_IMAGE_TYPES, MAX_IMAGE_SIZE
from app.infrastructure.storage.minio_client import MinioClient

# Mock pour MinioClient
async def override_get_minio_client():
    return AsyncMock(spec=MinioClient)

@pytest.fixture
def test_client():
    """Crée un client de test pour l'API FastAPI."""
    client = TestClient(app)
    yield client

def test_upload_file_success():
    """
    Test d'upload d'un fichier avec succès.
    """
    # Arrange
    file_content = b"test file content"
    file = io.BytesIO(file_content)
    expected_url = "https://minio.example.com/profiles/test.jpg"
    
    # Créer un client de test
    client = TestClient(app)
    
    with patch('app.api.v1.upload.get_minio_client') as mock_get_minio:
        # Configuration du mock
        mock_minio = AsyncMock()
        mock_minio.upload_file.return_value = expected_url
        mock_get_minio.return_value = mock_minio
        
        # Act
        response = client.post(
            "/api/upload",
            files={"file": ("test.jpg", file, "image/jpeg")},
            data={"folder": "profiles"}
        )
        
        # Assert
        assert response.status_code == 201
        assert response.json()["url"] == expected_url
        mock_minio.upload_file.assert_called_once()

def test_upload_file_invalid_format():
    """
    Test d'upload d'un fichier avec un format invalide.
    """
    # Arrange
    file_content = b"test file content"
    file = io.BytesIO(file_content)
    
    # Créer un client de test
    client = TestClient(app)
    
    # Act
    response = client.post(
        "/api/upload",
        files={"file": ("test.txt", file, "text/plain")},
        data={"folder": "profiles"}
    )
    
    # Assert
    assert response.status_code == 400
    assert response.json()["detail"]["code"] == "FORMAT_INVALID"
    assert "Type de fichier non autorisé" in response.json()["detail"]["message"]

def test_upload_file_size_exceeded():
    """
    Test d'upload d'un fichier trop volumineux.
    """
    # Arrange - Fichier de 6MB (supérieur à la limite de 5MB)
    file_size = 6 * 1024 * 1024  # 6 MB
    file_content = b"x" * file_size
    file = io.BytesIO(file_content)
    
    # Créer un client de test
    client = TestClient(app)
    
    # Act
    response = client.post(
        "/api/upload",
        files={"file": ("test.jpg", file, "image/jpeg")},
        data={"folder": "profiles"}
    )
    
    # Assert
    assert response.status_code == 400
    assert response.json()["detail"]["code"] == "SIZE_EXCEEDED"
    assert "Taille de fichier dépassée" in response.json()["detail"]["message"]

def test_upload_file_server_error():
    """
    Test d'upload d'un fichier avec une erreur serveur.
    """
    # Arrange
    file_content = b"test file content"
    file = io.BytesIO(file_content)
    
    # Créer un client de test
    client = TestClient(app)
    
    with patch('app.api.v1.upload.get_minio_client') as mock_get_minio:
        # Configuration du mock pour lever une exception
        mock_minio = AsyncMock()
        mock_minio.upload_file.side_effect = Exception("Erreur de connexion à MinIO")
        mock_get_minio.return_value = mock_minio
        
        # Act
        response = client.post(
            "/api/upload",
            files={"file": ("test.jpg", file, "image/jpeg")},
            data={"folder": "profiles"}
        )
        
        # Assert
        assert response.status_code == 500
        assert response.json()["detail"]["code"] == "UPLOAD_ERROR"
        mock_minio.upload_file.assert_called_once()

def test_upload_file_custom_folder():
    """
    Test d'upload d'un fichier dans un dossier personnalisé.
    """
    # Arrange
    file_content = b"test file content"
    file = io.BytesIO(file_content)
    expected_url = "https://minio.example.com/custom-folder/test.jpg"
    custom_folder = "custom-folder"
    
    # Créer un client de test
    client = TestClient(app)
    
    with patch('app.api.v1.upload.get_minio_client') as mock_get_minio:
        # Configuration du mock
        mock_minio = AsyncMock()
        mock_minio.upload_file.return_value = expected_url
        mock_get_minio.return_value = mock_minio
        
        # Act
        response = client.post(
            "/api/upload",
            files={"file": ("test.jpg", file, "image/jpeg")},
            data={"folder": custom_folder}
        )
        
        # Assert
        assert response.status_code == 201
        assert response.json()["url"] == expected_url
        # Vérifier que le dossier personnalisé a été utilisé dans l'appel
        mock_minio.upload_file.assert_called_once()
        args, kwargs = mock_minio.upload_file.call_args
        assert custom_folder in args[0]  # Le chemin d'objet doit contenir le dossier personnalisé