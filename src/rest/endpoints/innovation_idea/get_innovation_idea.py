from datetime import datetime
from typing import Self

from fastapi import Depends
from pydantic import BaseModel

from entity import User, InnovationIdea, Employee
from services import get_innovation_idea
from settings import configs
from ..dependencies import ManagerRequired
from ...router import router, Tags


class InnovationIdeaResponse(BaseModel):
    id: int
    participation_id: str
    participant_first_name: str
    participant_last_name: str
    participant_email: str
    title: str
    description: str
    feasibility_score: int
    confidence_score: int
    impact_score: int
    created_at: str
    updated_at: str
    rate: int | None

    @classmethod
    def from_entity(cls, entity: InnovationIdea) -> Self:
        assert isinstance(entity.id, int)
        assert isinstance(entity.created_at, datetime)
        assert isinstance(entity.updated_at, datetime)
        assert isinstance(entity.employee, Employee)
        assert isinstance(entity.employee.user, User)
        assert isinstance(entity.employee.user.first_name, str)
        assert isinstance(entity.employee.user.last_name, str)
        assert isinstance(entity.employee.user.email, str)
        return cls(
            id=entity.id,
            participation_id=str(entity.participation_id),
            participant_first_name=entity.employee.user.first_name,
            participant_last_name=entity.employee.user.last_name,
            participant_email=entity.employee.user.email,
            title=entity.title,
            description=entity.description,
            feasibility_score=entity.feasibility_score,
            confidence_score=entity.confidence_score,
            impact_score=entity.impact_score,
            rate=entity.rate,
            created_at=entity.created_at.strftime(configs.date_time_format),
            updated_at=entity.updated_at.strftime(configs.date_time_format),
        )


class GetInnovationIdeaResponseModel(BaseModel):
    result: InnovationIdeaResponse


@router.get(
    "/innovation-ideas/{_id}/",
    tags=[Tags.management],
)
def get_innovation_idea_endpoint(
    _id: int,
    user: User = Depends(ManagerRequired()),
) -> GetInnovationIdeaResponseModel:
    assert isinstance(user.id, int)
    idea = get_innovation_idea(
        idea_id=_id,
        user_id=user.id,
    )
    idea_response = InnovationIdeaResponse.from_entity(entity=idea)
    return GetInnovationIdeaResponseModel(result=idea_response)
