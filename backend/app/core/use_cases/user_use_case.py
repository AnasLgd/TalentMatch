from typing import List, Optional, Dict, Any
from fastapi import Depends

from app.core.entities.user import User, UserCreate, UserUpdate
from app.core.interfaces.user_repository import UserRepository
from app.core.interfaces.company_repository import CompanyRepository

class UserUseCase:
    """
    Cas d'utilisation pour la gestion des utilisateurs
    """
    
    def __init__(
        self,
        user_repository: UserRepository,
        company_repository: CompanyRepository
    ):
        self.user_repository = user_repository
        self.company_repository = company_repository
    
    async def get_all_users(self) -> List[User]:
        """Récupère tous les utilisateurs"""
        return await self.user_repository.get_all()
    
    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Récupère un utilisateur par son ID"""
        return await self.user_repository.get_by_id(user_id)
    
    async def get_user_by_email(self, email: str) -> Optional[User]:
        """Récupère un utilisateur par son email"""
        return await self.user_repository.get_by_email(email)
    
    async def get_users_by_company(self, company_id: int) -> List[User]:
        """Récupère tous les utilisateurs d'une entreprise"""
        return await self.user_repository.get_by_company_id(company_id)
    
    async def create_user(self, user_data: UserCreate) -> User:
        """Crée un nouvel utilisateur"""
        # Vérifier que l'email n'est pas déjà utilisé
        existing_user = await self.user_repository.get_by_email(user_data.email)
        if existing_user:
            raise ValueError("Cet email est déjà utilisé")
        
        # Vérifier que l'entreprise existe si spécifiée
        if user_data.company_id:
            company = await self.company_repository.get_by_id(user_data.company_id)
            if not company:
                raise ValueError("L'entreprise n'existe pas")
        
        return await self.user_repository.create(user_data)
    
    async def update_user(self, user_id: int, user_data: UserUpdate) -> Optional[User]:
        """Met à jour un utilisateur existant"""
        existing_user = await self.user_repository.get_by_id(user_id)
        if not existing_user:
            return None
        
        # Vérifier que l'email n'est pas déjà utilisé par un autre utilisateur
        if user_data.email:
            user_with_email = await self.user_repository.get_by_email(user_data.email)
            if user_with_email and user_with_email.id != user_id:
                raise ValueError("Cet email est déjà utilisé par un autre utilisateur")
        
        # Vérifier que l'entreprise existe si spécifiée
        if user_data.company_id:
            company = await self.company_repository.get_by_id(user_data.company_id)
            if not company:
                raise ValueError("L'entreprise n'existe pas")
        
        return await self.user_repository.update(user_id, user_data)
    
    async def delete_user(self, user_id: int) -> bool:
        """Supprime un utilisateur"""
        return await self.user_repository.delete(user_id)
    
    async def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """Authentifie un utilisateur"""
        return await self.user_repository.authenticate(email, password)
    
    async def change_user_password(self, user_id: int, new_password: str) -> bool:
        """Change le mot de passe d'un utilisateur"""
        return await self.user_repository.change_password(user_id, new_password)
    
    async def get_active_users(self) -> List[User]:
        """Récupère les utilisateurs actifs"""
        return await self.user_repository.get_active_users()
    
    async def search_users(self, query: str, company_id: Optional[int] = None) -> List[User]:
        """Recherche des utilisateurs par critères"""
        return await self.user_repository.search_users(query, company_id)
