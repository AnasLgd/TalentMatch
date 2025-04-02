from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class MatchStatus(str, Enum):
    SUGGESTED = "suggested"
    SUBMITTED = "submitted"
    ACCEPTED = "accepted"
    REJECTED = "rejected"

class MatchBase(BaseModel):
    consultant_id: int
    tender_id: int
    match_score: float
    status: MatchStatus = MatchStatus.SUGGESTED
    notes: Optional[str] = None

class MatchCreate(MatchBase):
    pass

class MatchUpdate(BaseModel):
    match_score: Optional[float] = None
    status: Optional[MatchStatus] = None
    notes: Optional[str] = None

class Match(MatchBase):
    id: int
    consultant: Dict[str, Any]
    tender: Dict[str, Any]
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True
