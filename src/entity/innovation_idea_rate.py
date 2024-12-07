from datetime import datetime

from pydantic import BaseModel, validator

from entity import Employee, InnovationIdea


class InnovationIdeaRate(BaseModel):
    id: int | None = None
    manager_id: int | None = None
    manager: Employee | None = None
    innovation_idea_id: int | None = None
    innovation_idea: InnovationIdea | None = None
    rate: int
    created_at: datetime | None = None
    updated_at: datetime | None = None

    @validator("innovation_idea_id", pre=True, always=True)
    @classmethod
    def set_innovation_idea_id(cls, i, values):
        if "innovation_idea" in values and values["innovation_idea"]:
            return values["innovation_idea"].id
        return i

    @validator("manager_id", pre=True, always=True)
    @classmethod
    def set_manager_id(cls, i, values):
        if "manager" in values and values["manager"]:
            return values["manager"].id
        return i
