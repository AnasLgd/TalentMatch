from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class ProficiencyLevel(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"

class SkillCategory(str, Enum):
    PROGRAMMING_LANGUAGE = "programming_language"
    FRAMEWORK = "framework"
    DATABASE = "database"
    CLOUD = "cloud"
    DEVOPS = "devops"
    METHODOLOGY = "methodology"
    SOFT_SKILL = "soft_skill"
    OTHER = "other"

class SkillBase(BaseModel):
    name: str
    category: SkillCategory
    description: Optional[str] = None

class SkillCreate(SkillBase):
    pass

class SkillUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[SkillCategory] = None
    description: Optional[str] = None

class Skill(SkillBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True

class ConsultantSkillBase(BaseModel):
    consultant_id: int
    skill_id: int
    proficiency_level: ProficiencyLevel
    years_experience: Optional[int] = None
    details: Optional[str] = None

class ConsultantSkillCreate(ConsultantSkillBase):
    pass

class ConsultantSkillUpdate(BaseModel):
    proficiency_level: Optional[ProficiencyLevel] = None
    years_experience: Optional[int] = None
    details: Optional[str] = None

class ConsultantSkill(ConsultantSkillBase):
    id: int
    skill: Dict[str, Any]
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True
