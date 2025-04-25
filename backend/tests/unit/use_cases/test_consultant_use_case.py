import pytest
from unittest.mock import Mock, AsyncMock, MagicMock
from fastapi import HTTPException

from app.core.entities.consultant import ConsultantCreate, ConsultantUpdate, Consultant
from app.core.entities.enums import AvailabilityStatus
from app.core.use_cases.consultant_use_case import ConsultantUseCase

@pytest.fixture
def mock_repositories():
    """Crée des repositories mockés pour les tests."""
    return {
        "consultant_repository": AsyncMock(),
        "skill_repository": AsyncMock(),
        "user_repository": AsyncMock(),
        "company_repository": AsyncMock()
    }

@pytest.fixture
def consultant_use_case(mock_repositories):
    """Crée un use case de consultant avec des repositories mockés."""
    return ConsultantUseCase(
        consultant_repository=mock_repositories["consultant_repository"],
        skill_repository=mock_repositories["skill_repository"],
        user_repository=mock_repositories["user_repository"],
        company_repository=mock_repositories["company_repository"]
    )

@pytest.mark.asyncio
async def test_create_consultant_success(consultant_use_case, mock_repositories):
    """
    Test de création d'un consultant avec succès.
    Vérifie que le use case appelle le repository avec les bonnes données.
    """
    # Arrange
    consultant_data = ConsultantCreate(
        company_id=1,
        title="Test Consultant",
        user_id=1,
        photo_url="https://minio.example.com/profiles/photo.jpg",
        availability_status=AvailabilityStatus.QUALIFIED
    )
    
    # Simuler un utilisateur existant
    mock_repositories["user_repository"].get_by_id.return_value = {"id": 1, "name": "Test User"}
    
    # Simuler une entreprise existante
    mock_repositories["company_repository"].get_by_id.return_value = {"id": 1, "name": "Test Company"}
    
    # Simuler la création réussie
    mock_consultant = MagicMock()
    mock_consultant.id = 99
    mock_consultant.company_id = 1
    mock_consultant.title = "Test Consultant"
    mock_consultant.user_id = 1
    mock_consultant.photo_url = "https://minio.example.com/profiles/photo.jpg"
    mock_consultant.availability_status = AvailabilityStatus.QUALIFIED
    mock_repositories["consultant_repository"].create.return_value = mock_consultant
    
    # Act
    result = await consultant_use_case.create_consultant(consultant_data)
    
    # Assert
    mock_repositories["user_repository"].get_by_id.assert_called_once_with(1)
    mock_repositories["company_repository"].get_by_id.assert_called_once_with(1)
    mock_repositories["consultant_repository"].create.assert_called_once_with(consultant_data)
    assert result == mock_consultant

@pytest.mark.asyncio
async def test_create_consultant_with_invalid_company(consultant_use_case, mock_repositories):
    """
    Test de création d'un consultant avec une entreprise invalide.
    Vérifie que le use case lève une exception HTTPException.
    """
    # Arrange
    consultant_data = ConsultantCreate(
        company_id=999,  # ID d'entreprise invalide
        title="Test Consultant",
        user_id=1,
        availability_status=AvailabilityStatus.QUALIFIED
    )
    
    # Simuler un utilisateur existant
    mock_repositories["user_repository"].get_by_id.return_value = {"id": 1, "name": "Test User"}
    
    # Simuler une entreprise inexistante
    mock_repositories["company_repository"].get_by_id.return_value = None
    
    # Act & Assert
    with pytest.raises(HTTPException) as excinfo:
        await consultant_use_case.create_consultant(consultant_data)
    
    # Vérifier que l'exception contient le bon message et code
    assert "L'entreprise n'existe pas" in str(excinfo.value.detail)
    assert excinfo.value.status_code == 400

@pytest.mark.asyncio
async def test_create_consultant_with_invalid_user(consultant_use_case, mock_repositories):
    """
    Test de création d'un consultant avec un utilisateur invalide.
    Vérifie que le use case lève une exception HTTPException.
    """
    # Arrange
    consultant_data = ConsultantCreate(
        company_id=1,
        title="Test Consultant",
        user_id=999,  # ID utilisateur invalide
        availability_status=AvailabilityStatus.AVAILABLE
    )
    
    # Simuler une entreprise existante
    mock_repositories["company_repository"].get_by_id.return_value = {"id": 1, "name": "Test Company"}
    
    # Simuler un utilisateur inexistant
    mock_repositories["user_repository"].get_by_id.return_value = None
    
    # Act & Assert
    with pytest.raises(HTTPException) as excinfo:
        await consultant_use_case.create_consultant(consultant_data)
    
    # Vérifier que l'exception contient le bon message et code
    assert "L'utilisateur n'existe pas" in str(excinfo.value.detail)
    assert excinfo.value.status_code == 400

@pytest.mark.asyncio
async def test_create_consultant_with_photo_url(consultant_use_case, mock_repositories):
    """
    Test de création d'un consultant avec une photo de profil.
    Vérifie que le use case traite correctement le champ photo_url.
    """
    # Arrange
    photo_url = "https://minio.example.com/profiles/photo.jpg"
    consultant_data = ConsultantCreate(
        company_id=1,
        title="Test Consultant",
        user_id=1,
        photo_url=photo_url,
        availability_status=AvailabilityStatus.AVAILABLE
    )
    
    # Simuler un utilisateur existant
    mock_repositories["user_repository"].get_by_id.return_value = {"id": 1, "name": "Test User"}
    
    # Simuler une entreprise existante
    mock_repositories["company_repository"].get_by_id.return_value = {"id": 1, "name": "Test Company"}
    
    # Simuler la création réussie
    mock_consultant = MagicMock()
    mock_consultant.id = 99
    mock_consultant.photo_url = photo_url
    mock_repositories["consultant_repository"].create.return_value = mock_consultant
    
    # Act
    result = await consultant_use_case.create_consultant(consultant_data)
    
    # Assert
    mock_repositories["consultant_repository"].create.assert_called_once_with(consultant_data)
    assert result.photo_url == photo_url

@pytest.mark.asyncio
async def test_update_consultant_photo_url(consultant_use_case, mock_repositories):
    """
    Test de mise à jour de la photo de profil d'un consultant.
    """
    # Arrange
    consultant_id = 1
    new_photo_url = "https://minio.example.com/profiles/new_photo.jpg"
    update_data = ConsultantUpdate(
        photo_url=new_photo_url
    )
    
    # Simuler un consultant existant
    mock_consultant = MagicMock()
    mock_consultant.id = consultant_id
    mock_consultant.photo_url = new_photo_url
    mock_repositories["consultant_repository"].get_by_id.return_value = mock_consultant
    mock_repositories["consultant_repository"].update.return_value = mock_consultant
    
    # Act
    result = await consultant_use_case.update_consultant(consultant_id, update_data)
    
    # Assert
    mock_repositories["consultant_repository"].update.assert_called_once_with(consultant_id, update_data)
    assert result.photo_url == new_photo_url