from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class PortfolioStatus(str, Enum):
    DRAFT = "draft"
    FINAL = "final"

class PortfolioBase(BaseModel):
    consultant_id: int
    tender_id: int
    file_path: Optional[str] = None
    version: int = 1
    status: PortfolioStatus = PortfolioStatus.DRAFT
    content: Optional[str] = None

class PortfolioCreate(PortfolioBase):
    pass

class PortfolioUpdate(BaseModel):
    file_path: Optional[str] = None
    version: Optional[int] = None
    status: Optional[PortfolioStatus] = None
    content: Optional[str] = None

class Portfolio(PortfolioBase):
    id: int
    consultant: Dict[str, Any]
    tender: Dict[str, Any]
    generated_date: datetime
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True
