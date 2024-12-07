from uuid import UUID

from fastapi import Depends
from pydantic import BaseModel

from entity import User
from services import create_innovation_idea
from ..dependencies import EmployeeRequired
from ...router import router, Tags


class CreateInnovationIdeaRequestModel(BaseModel):
    title: str
    description: str
    feasibility_score: int
    confidence_score: int
    impact_score: int


class CreateInnovationIdeaResponseModel(BaseModel):
    result: str = "Innovation Idea Created Successfully"


@router.post(
    "/participants/{participation_id}/ideas/",
    tags=[Tags.participation],
)
def create_innovation_idea_endpoint(
    participation_id: UUID,
    payload: CreateInnovationIdeaRequestModel,
    user: User = Depends(EmployeeRequired()),
) -> CreateInnovationIdeaResponseModel:
    assert isinstance(user.id, int)
    create_innovation_idea(
        participation_id=participation_id,
        user_id=user.id,
        title=payload.title,
        description=payload.description,
        feasibility_score=payload.feasibility_score,
        confidence_score=payload.confidence_score,
        impact_score=payload.impact_score,
    )
    return CreateInnovationIdeaResponseModel()
