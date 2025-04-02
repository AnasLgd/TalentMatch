from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime, date
from enum import Enum

class TenderStatus(str, Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    CLOSED = "closed"
    CANCELLED = "cancelled"

class TenderBase(BaseModel):
    title: str
    company_id: int
    client_name: str
    description: str
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    status: TenderStatus = TenderStatus.OPEN
    location: Optional[str] = None
    remote_work: Optional[bool] = False
    budget: Optional[float] = None
    required_consultants: Optional[int] = 1

class TenderCreate(TenderBase):
    skills: Optional[List[Dict[str, Any]]] = None

class TenderUpdate(BaseModel):
    title: Optional[str] = None
    client_name: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    status: Optional[TenderStatus] = None
    location: Optional[str] = None
    remote_work: Optional[bool] = None
    budget: Optional[float] = None
    required_consultants: Optional[int] = None
    skills: Optional[List[Dict[str, Any]]] = None

class Tender(TenderBase):
    id: int
    skills: List[Dict[str, Any]] = []
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True

class TenderSkillBase(BaseModel):
    tender_id: int
    skill_id: int
    importance: str  # "required", "preferred", "nice_to_have"
    details: Optional[str] = None

class TenderSkillCreate(TenderSkillBase):
    pass

class TenderSkillUpdate(BaseModel):
    importance: Optional[str] = None
    details: Optional[str] = None

class TenderSkill(TenderSkillBase):
    id: int
    skill: Dict[str, Any]
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True

# Create a TenderResponse alias for API responses
TenderResponse = Tender
