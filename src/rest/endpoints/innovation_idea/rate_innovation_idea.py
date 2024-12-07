from fastapi import Depends
from pydantic import BaseModel

from entity import User
from services import rate_innovation_idea
from ..dependencies import ManagerRequired
from ...router import router, Tags


class RateInnovationIdeaResponseModel(BaseModel):
    result: str = "Innovation Idea Rated Successfully"


class RateInnovationIdeaRequestModel(BaseModel):
    rate: int


@router.post(
    "/ideas/{_id}/rate/",
    tags=[Tags.management],
)
def rate_innovation_idea_endpoint(
    _id: int,
    payload: RateInnovationIdeaRequestModel,
    user: User = Depends(ManagerRequired()),
) -> RateInnovationIdeaResponseModel:
    assert isinstance(user.id, int)
    rate_innovation_idea(
        innovation_idea_id=_id,
        user_id=user.id,
        rate=payload.rate,
    )
    return RateInnovationIdeaResponseModel()
