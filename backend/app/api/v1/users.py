from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.entities.user import User
from app.adapters.repositories.user_repository import SQLAlchemyUserRepository
from app.infrastructure.database.session import get_db

router = APIRouter(
    tags=["users"],
    responses={404: {"description": "Utilisateur non trouvé"}},
)

@router.get("/available", response_model=List[User])
async def get_available_users(
    db: Session = Depends(get_db),
):
    """
    Récupère les utilisateurs qui ne sont pas déjà consultants.
    Cette API est utilisée pour la création d'un consultant.
    """
    try:
        user_repository = SQLAlchemyUserRepository(db)
        users = await user_repository.get_available_users()
        # Debug logging pour vérifier le format des données
        print(f"Available users: {users}")
        return users
    except Exception as e:
        print(f"Error getting available users: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la récupération des utilisateurs disponibles: {str(e)}",
        )