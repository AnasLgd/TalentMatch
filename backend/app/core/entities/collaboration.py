from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime, date
from enum import Enum

class CollaborationStatus(str, Enum):
    PENDING = "pending"
    ACTIVE = "active"
    INACTIVE = "inactive"

class CollaborationBase(BaseModel):
    initiator_company_id: int
    partner_company_id: int
    status: CollaborationStatus = CollaborationStatus.PENDING
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    terms: Optional[str] = None

class CollaborationCreate(CollaborationBase):
    pass

class CollaborationUpdate(BaseModel):
    status: Optional[CollaborationStatus] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    terms: Optional[str] = None

class Collaboration(CollaborationBase):
    id: int
    initiator_company: Dict[str, Any]
    partner_company: Dict[str, Any]
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True
