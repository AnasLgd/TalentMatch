from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime, date
from app.core.entities.enums import AvailabilityStatus

class ConsultantBase(BaseModel):
    company_id: int
    title: str
    user_id: Optional[int] = None  # Rendu optionnel pour permettre la création de consultants sans utilisateur associé
    first_name: Optional[str] = None  # Prénom du consultant
    last_name: Optional[str] = None  # Nom du consultant
    experience_years: Optional[int] = None
    availability_status: AvailabilityStatus = AvailabilityStatus.AVAILABLE
    availability_date: Optional[date] = None
    hourly_rate: Optional[float] = None
    daily_rate: Optional[float] = None
    bio: Optional[str] = None
    location: Optional[str] = None
    remote_work: Optional[bool] = False
    max_travel_distance: Optional[int] = None
    photo_url: Optional[str] = None
class ConsultantCreate(ConsultantBase):
    skills: Optional[List[Dict[str, Any]]] = None
    # Note: first_name et last_name sont déjà définis dans ConsultantBase

class ConsultantUpdate(BaseModel):
    title: Optional[str] = None
    experience_years: Optional[int] = None
    availability_status: Optional[AvailabilityStatus] = None
    availability_date: Optional[date] = None
    hourly_rate: Optional[float] = None
    daily_rate: Optional[float] = None
    bio: Optional[str] = None
    location: Optional[str] = None
    remote_work: Optional[bool] = None
    max_travel_distance: Optional[int] = None
    skills: Optional[List[Dict[str, Any]]] = None

class Consultant(ConsultantBase):
    id: int
    user: Dict[str, Any]
    skills: List[Dict[str, Any]] = []
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True

# Ajout de la classe ConsultantResponse manquante
class ConsultantResponse(Consultant):
    """
    Modèle de données pour la réponse API d'un consultant.
    Étend le modèle Consultant avec des champs supplémentaires si nécessaire.
    """
    
    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 1,
                "user_id": 2,
                "company_id": 3,
                "first_name": "John",
                "last_name": "Doe",
                "title": "Ingénieur Logiciel Senior",
                "experience_years": 8,
                "availability_status": "available",
                "availability_date": "2025-02-01",
                "hourly_rate": 85.0,
                "daily_rate": 680.0,
                "bio": "Plus de 8 ans d'expérience en développement backend et cloud.",
                "location": "Paris, France",
                "remote_work": True,
                "max_travel_distance": 50,
                "user": {
                    "id": 2,
                    "email": "john.doe@example.com",
                    "full_name": "John Doe"
                },
                "skills": [
                    {"id": 1, "name": "Python", "level": "expert"},
                    {"id": 2, "name": "FastAPI", "level": "advanced"}
                ],
                "created_at": "2024-01-01T00:00:00",
                "updated_at": "2024-01-15T14:30:00"
            }
        }
