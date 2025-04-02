from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum

class UserRole(str, Enum):
    ADMIN = "admin"
    MANAGER = "manager"
    RECRUITER = "recruiter"
    SALES = "sales"
    CONSULTANT = "consultant"

class UserBase(BaseModel):
    email: str
    first_name: str
    last_name: str
    role: UserRole
    company_id: int

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    email: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role: Optional[UserRole] = None
    company_id: Optional[int] = None
    password: Optional[str] = None

class User(UserBase):
    id: int
    is_active: bool = True
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True
