import pytest
from unittest.mock import Mock, MagicMock
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException

from app.core.entities.consultant import ConsultantCreate, ConsultantUpdate
from app.core.entities.enums import AvailabilityStatus
from app.adapters.repositories.consultant_repository import SQLAlchemyConsultantRepository
from app.infrastructure.database.models import Consultant as ConsultantModel
from app.infrastructure.database.models import User as UserModel

@pytest.fixture
def mock_db_session():
    """Crée une session de base de données simulée pour les tests."""
    mock_session = MagicMock(spec=Session)
    
    # Simuler une requête qui retourne None (utilisateur non trouvé)
    mock_query = MagicMock()
    mock_query.filter.return_value.first.return_value = None
    mock_session.query.return_value = mock_query
    
    # Simuler la méthode add
    mock_session.add = MagicMock()
    
    # Simuler les méthodes commit et refresh
    mock_session.commit = MagicMock()
    mock_session.refresh = MagicMock()
    
    return mock_session

@pytest.fixture
def consultant_repository(mock_db_session):
    """Crée un repository de consultant avec une session de base de données simulée."""
    return SQLAlchemyConsultantRepository(mock_db_session)

@pytest.mark.asyncio
async def test_create_consultant_without_user(consultant_repository, mock_db_session):
    """
    Test de création d'un consultant sans utilisateur associé.
    Vérifie que le repository n'essaie pas de vérifier l'existence d'un utilisateur
    quand user_id est None.
    """
    # Arrange
    consultant_data = ConsultantCreate(
        company_id=1,
        title="Test Consultant",
        user_id=None,  # Aucun utilisateur associé
        availability_status=AvailabilityStatus.AVAILABLE
    )
    
    # Simuler un modèle ConsultantModel et son id après insertion
    mock_db_consultant = MagicMock(spec=ConsultantModel)
    mock_db_consultant.id = 99
    mock_db_consultant.user_id = None
    mock_db_consultant.company_id = 1
    mock_db_consultant.title = "Test Consultant"
    mock_db_consultant.status = AvailabilityStatus.AVAILABLE
    
    # Configurer le comportement du mock pour refresh
    def side_effect_refresh(obj):
        obj.id = 99
        return None
    
    mock_db_session.refresh.side_effect = side_effect_refresh
    
    # Simuler la méthode _map_to_entity pour retourner un objet Consultant valide
    consultant_repository._map_to_entity = MagicMock()
    consultant_repository._map_to_entity.return_value = consultant_data
    
    # Act
    result = await consultant_repository.create(consultant_data)
    
    # Assert
    # Vérifier que add et commit ont été appelés
    mock_db_session.add.assert_called_once()
    mock_db_session.commit.assert_called_once()
    
    # Vérifier que le résultat est celui attendu
    assert result is not None
    
    # Vérifier que la méthode _map_to_entity a été appelée
    consultant_repository._map_to_entity.assert_called_once()

@pytest.mark.asyncio
async def test_create_consultant_with_invalid_user_id(consultant_repository, mock_db_session):
    """
    Test de création d'un consultant avec un ID utilisateur invalide.
    Vérifie que le repository lève une exception HTTPException quand l'utilisateur n'existe pas.
    """
    # Arrange
    consultant_data = ConsultantCreate(
        company_id=1,
        title="Test Consultant",
        user_id=999,  # ID utilisateur inexistant
        availability_status=AvailabilityStatus.AVAILABLE
    )
    
    # Mock retourne None pour simuler qu'aucun utilisateur n'est trouvé
    mock_db_session.query.return_value.filter.return_value.first.return_value = None
    
    # Act & Assert
    with pytest.raises(HTTPException) as excinfo:
        await consultant_repository.create(consultant_data)
    
    # Vérifier que l'exception contient le bon message
    assert "L'utilisateur n'existe pas" in str(excinfo.value.detail)
    # Vérifier que le code d'erreur est 400 (Bad Request)
    assert excinfo.value.status_code == 400
    
    # Vérifier que commit n'a pas été appelé (car une exception a été levée)
    mock_db_session.commit.assert_not_called()

@pytest.mark.asyncio
async def test_create_consultant_with_photo_url(consultant_repository, mock_db_session):
    """
    Test de création d'un consultant avec une photo de profil.
    Vérifie que le repository gère correctement le champ photo_url.
    """
    # Arrange
    consultant_data = ConsultantCreate(
        company_id=1,
        title="Test Consultant",
        user_id=1,
        photo_url="https://minio.example.com/profiles/photo.jpg",
        availability_status=AvailabilityStatus.AVAILABLE
    )
    
    # Simuler un utilisateur existant
    mock_user = MagicMock()
    mock_user.id = 1
    mock_db_session.query.return_value.filter.return_value.first.return_value = mock_user
    
    # Simuler un modèle ConsultantModel et son id après insertion
    mock_db_consultant = MagicMock(spec=ConsultantModel)
    mock_db_consultant.id = 99
    mock_db_consultant.user_id = 1
    mock_db_consultant.company_id = 1
    mock_db_consultant.title = "Test Consultant"
    mock_db_consultant.photo_url = "https://minio.example.com/profiles/photo.jpg"
    mock_db_consultant.status = AvailabilityStatus.AVAILABLE
    
    # Configurer le comportement du mock pour refresh
    def side_effect_refresh(obj):
        obj.id = 99
        return None
    
    mock_db_session.refresh.side_effect = side_effect_refresh
    
    # Simuler la méthode _map_to_entity pour retourner un objet Consultant valide
    consultant_repository._map_to_entity = MagicMock()
    consultant_repository._map_to_entity.return_value = consultant_data
    
    # Act
    result = await consultant_repository.create(consultant_data)
    
    # Assert
    # Vérifier que add et commit ont été appelés
    mock_db_session.add.assert_called_once()
    mock_db_session.commit.assert_called_once()
    
    # Vérifier que le résultat est celui attendu
    assert result is not None
    
    # Vérifier que la méthode _map_to_entity a été appelée
    consultant_repository._map_to_entity.assert_called_once()

@pytest.mark.asyncio
async def test_update_consultant_photo_url(consultant_repository, mock_db_session):
    """
    Test de mise à jour de la photo de profil d'un consultant.
    """
    # Arrange
    consultant_id = 1
    update_data = ConsultantUpdate(
        photo_url="https://minio.example.com/profiles/new_photo.jpg"
    )
    
    # Simuler un consultant existant
    mock_consultant = MagicMock(spec=ConsultantModel)
    mock_consultant.id = consultant_id
    mock_consultant.photo_url = "https://minio.example.com/profiles/old_photo.jpg"
    mock_db_session.query.return_value.filter.return_value.first.return_value = mock_consultant
    
    # Simuler la méthode _map_to_entity
    consultant_repository._map_to_entity = MagicMock()
    consultant_entity = MagicMock()
    consultant_entity.photo_url = update_data.photo_url
    consultant_repository._map_to_entity.return_value = consultant_entity
    
    # Act
    result = await consultant_repository.update(consultant_id, update_data)
    
    # Assert
    # Vérifier que commit a été appelé
    mock_db_session.commit.assert_called_once()
    
    # Vérifier que le champ photo_url a été mis à jour
    assert mock_consultant.photo_url == update_data.photo_url
    
    # Vérifier que _map_to_entity a été appelé
    consultant_repository._map_to_entity.assert_called_once()