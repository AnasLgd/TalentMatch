from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum

class CompanyBase(BaseModel):
    name: str
    description: Optional[str] = None
    website: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    postal_code: Optional[str] = None
    country: Optional[str] = None

class CompanyCreate(CompanyBase):
    pass

class CompanyUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    website: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    postal_code: Optional[str] = None
    country: Optional[str] = None
    is_active: Optional[bool] = None

class Company(CompanyBase):
    id: int
    is_active: bool = True
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True
        
class CompanyResponse(Company):
    """
    Model for company responses in the API
    Includes all fields from Company plus any additional fields needed for API responses
    """
    # Additional fields can be added here if needed for API responses
    
    class Config:
        orm_mode = True
        from_attributes = True  # Updated for newer Pydantic versions
