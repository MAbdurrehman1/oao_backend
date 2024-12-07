from datetime import datetime
from typing import Self

from fastapi import Depends
from pydantic import BaseModel

from entity import User, InnovationIdea, Employee
from services import get_report_innovation_ideas
from settings import configs
from ..dependencies import AdminOrManagerRequired
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
            created_at=entity.created_at.strftime(configs.date_time_format),
            updated_at=entity.updated_at.strftime(configs.date_time_format),
            rate=entity.rate,
        )


class GetReportInnovationIdeasListResponseModel(BaseModel):
    total_count: int
    result: list[InnovationIdeaResponse]


@router.get(
    "/report/{_id}/ideas/",
    tags=[Tags.management],
)
def get_report_innovation_ideas_list_endpoint(
    _id: int,
    rate: int | None = None,
    unrated: bool | None = None,
    offset: int = 0,
    limit: int = 10,
    user: User = Depends(AdminOrManagerRequired()),
) -> GetReportInnovationIdeasListResponseModel:
    assert isinstance(user.id, int)
    total_count, ideas = get_report_innovation_ideas(
        report_id=_id,
        user_id=user.id,
        offset=offset,
        limit=limit,
        is_admin=user.is_admin,
        rate=rate,
        unrated=unrated,
    )
    ideas_response = [InnovationIdeaResponse.from_entity(entity=idea) for idea in ideas]
    return GetReportInnovationIdeasListResponseModel(
        result=ideas_response, total_count=total_count
    )
