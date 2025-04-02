from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

from app.core.interfaces.user_repository import UserRepository
from app.core.entities.user import User, UserCreate, UserUpdate
from app.infrastructure.database.models import User as UserModel
from app.infrastructure.security.password import get_password_hash, verify_password

class SQLAlchemyUserRepository(UserRepository):
    """
    Implémentation SQLAlchemy du repository pour les utilisateurs
    """
    
    def __init__(self, db: Session):
        self.db = db
    
    async def get_all(self) -> List[User]:
        """Récupère tous les utilisateurs"""
        users = self.db.query(UserModel).all()
        return [self._map_to_entity(user) for user in users]
    
    async def get_by_id(self, user_id: int) -> Optional[User]:
        """Récupère un utilisateur par son ID"""
        user = self.db.query(UserModel).filter(UserModel.id == user_id).first()
        if not user:
            return None
        return self._map_to_entity(user)
    
    async def get_by_email(self, email: str) -> Optional[User]:
        """Récupère un utilisateur par son email"""
        user = self.db.query(UserModel).filter(UserModel.email == email).first()
        if not user:
            return None
        return self._map_to_entity(user)
    
    async def get_by_company_id(self, company_id: int) -> List[User]:
        """Récupère tous les utilisateurs d'une entreprise"""
        users = self.db.query(UserModel).filter(UserModel.company_id == company_id).all()
        return [self._map_to_entity(user) for user in users]
    
    async def create(self, user: UserCreate) -> User:
        """Crée un nouvel utilisateur"""
        try:
            # Hacher le mot de passe
            hashed_password = get_password_hash(user.password)
            
            # Créer l'utilisateur
            db_user = UserModel(
                email=user.email,
                hashed_password=hashed_password,
                first_name=user.first_name,
                last_name=user.last_name,
                role=user.role,
                company_id=user.company_id,
                is_active=user.is_active if hasattr(user, "is_active") else True
            )
            
            self.db.add(db_user)
            self.db.commit()
            self.db.refresh(db_user)
            
            return self._map_to_entity(db_user)
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="L'utilisateur avec cet email existe déjà"
            )
    
    async def update(self, user_id: int, user: UserUpdate) -> Optional[User]:
        """Met à jour un utilisateur existant"""
        db_user = self.db.query(UserModel).filter(UserModel.id == user_id).first()
        if not db_user:
            return None
        
        # Mettre à jour les champs
        update_data = user.dict(exclude_unset=True)
        
        # Hacher le mot de passe si fourni
        if "password" in update_data:
            update_data["hashed_password"] = get_password_hash(update_data.pop("password"))
        
        for key, value in update_data.items():
            setattr(db_user, key, value)
        
        try:
            self.db.commit()
            self.db.refresh(db_user)
            return self._map_to_entity(db_user)
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Erreur lors de la mise à jour de l'utilisateur"
            )
    
    async def delete(self, user_id: int) -> bool:
        """Supprime un utilisateur"""
        db_user = self.db.query(UserModel).filter(UserModel.id == user_id).first()
        if not db_user:
            return False
        
        self.db.delete(db_user)
        self.db.commit()
        return True
    
    async def authenticate(self, email: str, password: str) -> Optional[User]:
        """Authentifie un utilisateur"""
        user = self.db.query(UserModel).filter(UserModel.email == email).first()
        if not user:
            return None
        
        if not verify_password(password, user.hashed_password):
            return None
        
        return self._map_to_entity(user)
    
    async def change_password(self, user_id: int, new_password: str) -> bool:
        """Change le mot de passe d'un utilisateur"""
        db_user = self.db.query(UserModel).filter(UserModel.id == user_id).first()
        if not db_user:
            return False
        
        db_user.hashed_password = get_password_hash(new_password)
        self.db.commit()
        return True
    
    async def get_active_users(self) -> List[User]:
        """Récupère les utilisateurs actifs"""
        users = self.db.query(UserModel).filter(UserModel.is_active == True).all()
        return [self._map_to_entity(user) for user in users]
    
    async def search_users(self, query: str, company_id: Optional[int] = None) -> List[User]:
        """Recherche des utilisateurs par critères"""
        search = f"%{query}%"
        users_query = self.db.query(UserModel).filter(
            (UserModel.first_name.ilike(search)) |
            (UserModel.last_name.ilike(search)) |
            (UserModel.email.ilike(search))
        )
        
        if company_id:
            users_query = users_query.filter(UserModel.company_id == company_id)
        
        users = users_query.all()
        return [self._map_to_entity(user) for user in users]
    
    def _map_to_entity(self, db_user: UserModel) -> User:
        """Convertit un modèle SQLAlchemy en entité"""
        return User(
            id=db_user.id,
            email=db_user.email,
            first_name=db_user.first_name,
            last_name=db_user.last_name,
            role=db_user.role.value,
            company_id=db_user.company_id,
            is_active=db_user.is_active,
            created_at=db_user.created_at,
            updated_at=db_user.updated_at
        )
