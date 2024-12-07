from typing import Self

from fastapi import Depends
from pydantic import BaseModel

from entity import User, MatrixInnovationIdea
from services import get_report_matrix_innovation_ideas
from ..dependencies import AdminOrManagerRequired
from ...router import router, Tags


class InnovationIdeaResponse(BaseModel):
    id: int
    title: str
    feasibility_score: int
    confidence_score: int
    impact_score: int

    @classmethod
    def from_entity(cls, entity: MatrixInnovationIdea) -> Self:
        assert isinstance(entity.id, int)
        return cls(
            id=entity.id,
            title=entity.title,
            feasibility_score=entity.feasibility_score,
            confidence_score=entity.confidence_score,
            impact_score=entity.impact_score,
        )


class GetReportMatrixInnovationIdeasListResponseModel(BaseModel):
    result: list[InnovationIdeaResponse]


@router.get(
    "/report/{_id}/ideas-matrix/",
    tags=[Tags.management],
)
def get_report_matrix_innovation_ideas_list_endpoint(
    _id: int,
    user: User = Depends(AdminOrManagerRequired()),
) -> GetReportMatrixInnovationIdeasListResponseModel:
    assert isinstance(user.id, int)
    ideas = get_report_matrix_innovation_ideas(
        report_id=_id,
        user_id=user.id,
    )
    ideas_response = [InnovationIdeaResponse.from_entity(entity=idea) for idea in ideas]
    return GetReportMatrixInnovationIdeasListResponseModel(result=ideas_response)
