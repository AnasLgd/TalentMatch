from typing import Protocol, List, Optional, Dict, Any

from app.core.entities.user import User, UserCreate, UserUpdate

class UserRepository(Protocol):
    async def get_all(self) -> List[User]:
        ...
    
    async def get_by_id(self, user_id: int) -> Optional[User]:
        ...
    
    async def get_by_email(self, email: str) -> Optional[User]:
        ...
    
    async def get_by_company_id(self, company_id: int) -> List[User]:
        ...
    
    async def create(self, user: UserCreate) -> User:
        ...
    
    async def update(self, user_id: int, user: UserUpdate) -> Optional[User]:
        ...
    
    async def delete(self, user_id: int) -> bool:
        ...
    
    async def authenticate(self, email: str, password: str) -> Optional[User]:
        ...
    
    async def change_password(self, user_id: int, new_password: str) -> bool:
        ...
    
    async def get_active_users(self) -> List[User]:
        ...
    
    async def search_users(self, query: str, company_id: Optional[int] = None) -> List[User]:
        ...
