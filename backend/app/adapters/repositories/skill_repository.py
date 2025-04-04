from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

from app.core.interfaces.skill_repository import SkillRepository
from app.core.entities.skill import (
    Skill as SkillEntity,
    SkillCreate,
    SkillUpdate,
    ProficiencyLevel
)
from app.infrastructure.database.models import Skill as SkillModel


class SQLAlchemySkillRepository(SkillRepository):
    """
    Implémentation de SkillRepository avec SQLAlchemy
    """
    
    def __init__(self, db: Session):
        self.db = db

    async def get_all(self) -> List[SkillEntity]:
        db_skills = self.db.query(SkillModel).all()
        return [self._map_to_entity(db_skill) for db_skill in db_skills]

    async def get_by_id(self, skill_id: int) -> Optional[SkillEntity]:
        db_skill = self.db.query(SkillModel).filter(SkillModel.id == skill_id).first()
        if not db_skill:
            return None
        return self._map_to_entity(db_skill)

    async def get_by_name(self, name: str) -> Optional[SkillEntity]:
        db_skill = self.db.query(SkillModel).filter(SkillModel.name == name).first()
        if not db_skill:
            return None
        return self._map_to_entity(db_skill)

    async def get_by_category(self, category: str) -> List[SkillEntity]:
        db_skills = self.db.query(SkillModel).filter(SkillModel.category == category).all()
        return [self._map_to_entity(db_skill) for db_skill in db_skills]

    async def create(self, skill: SkillCreate) -> SkillEntity:
        # skill: SkillCreate => (name, category, description)
        try:
            db_skill = SkillModel(
                name=skill.name,
                category=skill.category.value,  # si c'est un Enum, .value
                description=skill.description
            )
            self.db.add(db_skill)
            self.db.commit()
            self.db.refresh(db_skill)
            return self._map_to_entity(db_skill)
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Skill with name '{skill.name}' already exists."
            )

    async def update(self, skill_id: int, skill_data: SkillUpdate) -> Optional[SkillEntity]:
        db_skill = self.db.query(SkillModel).filter(SkillModel.id == skill_id).first()
        if not db_skill:
            return None
        
        # skill_data = SkillUpdate => (name=?, category=?, description=?)
        updates = skill_data.dict(exclude_unset=True)
        
        # On parcourt chaque champ et on l'assigne au modèle
        for field_name, field_value in updates.items():
            if field_name == "category" and field_value is not None:
                setattr(db_skill, field_name, field_value.value)
            else:
                setattr(db_skill, field_name, field_value)
        
        try:
            self.db.commit()
            self.db.refresh(db_skill)
            return self._map_to_entity(db_skill)
        except IntegrityError as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Erreur lors de la mise à jour de la skill: {str(e)}"
            )

    async def delete(self, skill_id: int) -> bool:
        db_skill = self.db.query(SkillModel).filter(SkillModel.id == skill_id).first()
        if not db_skill:
            return False
        try:
            self.db.delete(db_skill)
            self.db.commit()
            return True
        except IntegrityError as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Erreur lors de la suppression de la skill: {str(e)}"
            )

    async def search_skills(self, query: str) -> List[SkillEntity]:
        # On cherche par name ou description
        search_pattern = f"%{query}%"
        db_skills = self.db.query(SkillModel).filter(
            (SkillModel.name.ilike(search_pattern)) | (SkillModel.description.ilike(search_pattern))
        ).all()
        return [self._map_to_entity(db_skill) for db_skill in db_skills]

    async def get_popular_skills(self, limit: int = 10) -> List[SkillEntity]:
        # Exemple d'implémentation simple (à adapter) :
        # On pourrait compter le nombre de consultants associées à chaque skill ou le nombre de Tenders, etc.
        # Pour l'instant, on va juste renvoyer les X premiers skills ordonnés par ID, par exemple
        db_skills = self.db.query(SkillModel).order_by(SkillModel.id).limit(limit).all()
        return [self._map_to_entity(db_skill) for db_skill in db_skills]

    async def get_consultant_skills(self, consultant_id: int) -> List[Dict[str, Any]]:
        # Dans consultant_repository, on fait un join sur consultant_skills => 
        # On peut faire la même chose ici ou déléguer la logique.
        # Ex d'implémentation minimaliste (non optimisée) :

        # Récupération brute :
        # SELECT * FROM consultant_skills cs JOIN skills s ON cs.skill_id = s.id WHERE consultant_id = ?

        from app.infrastructure.database.models import ConsultantSkill as CSModel

        results = (
            self.db.query(CSModel, SkillModel)
            .join(SkillModel, CSModel.skill_id == SkillModel.id)
            .filter(CSModel.consultant_id == consultant_id)
            .all()
        )

        # On reconstruit un tableau
        data = []
        for cs, sk in results:
            data.append({
                "consultant_id": cs.consultant_id,
                "proficiency_level": cs.proficiency_level.value,
                "years_experience": cs.years_experience,
                "details": cs.details,
                "skill": {
                    "id": sk.id,
                    "name": sk.name,
                    "category": sk.category,
                    "description": sk.description
                }
            })
        return data

    async def get_tender_skills(self, tender_id: int) -> List[Dict[str, Any]]:
        from app.infrastructure.database.models import TenderSkill as TSModel

        results = (
            self.db.query(TSModel, SkillModel)
            .join(SkillModel, TSModel.skill_id == SkillModel.id)
            .filter(TSModel.tender_id == tender_id)
            .all()
        )

        data = []
        for ts, sk in results:
            data.append({
                "tender_id": ts.tender_id,
                "importance": ts.importance,
                "details": ts.details,
                "skill": {
                    "id": sk.id,
                    "name": sk.name,
                    "category": sk.category,
                    "description": sk.description
                }
            })
        return data

    def _map_to_entity(self, db_skill: SkillModel) -> SkillEntity:
        return SkillEntity(
            id=db_skill.id,
            name=db_skill.name,
            category=db_skill.category,  # c'est une string
            description=db_skill.description,
            created_at=db_skill.created_at,
            updated_at=db_skill.updated_at,
        )