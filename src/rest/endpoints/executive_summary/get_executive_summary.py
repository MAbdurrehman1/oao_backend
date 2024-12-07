from typing import Self

from fastapi import Depends
from pydantic import BaseModel

from entity import User, ExecutiveSummary
from services import get_executive_summary
from ..dependencies import AdminOrManagerRequired
from ...router import router, Tags


class ExecutiveSummaryResponse(BaseModel):
    snapshots: int
    key_insights: int
    speed_of_transformation: int
    recommendations_generated: int
    ideas_reviewed: int

    @classmethod
    def from_entity(cls, entity: ExecutiveSummary) -> Self:
        assert isinstance(entity.snapshots, int)
        assert isinstance(entity.key_insights, int)
        assert isinstance(entity.speed_of_transformation, int)
        assert isinstance(entity.recommendations_generated, int)
        assert isinstance(entity.ideas_reviewed, int)
        return cls(
            snapshots=entity.snapshots,
            key_insights=entity.key_insights,
            speed_of_transformation=entity.speed_of_transformation,
            recommendations_generated=entity.recommendations_generated,
            ideas_reviewed=entity.ideas_reviewed,
        )


class GetExecutiveSummaryResponseModel(BaseModel):
    result: ExecutiveSummaryResponse


@router.get(
    "/reports/{_id}/executive_summary/",
    tags=[Tags.management],
)
def get_executive_summary_endpoint(
    _id: int,
    user: User = Depends(AdminOrManagerRequired()),
) -> GetExecutiveSummaryResponseModel:
    assert isinstance(user.id, int)
    executive_summary = get_executive_summary(
        report_id=_id,
        user_id=user.id,
        is_admin=user.is_admin,
    )
    executive_summary_response = ExecutiveSummaryResponse.from_entity(
        entity=executive_summary
    )
    return GetExecutiveSummaryResponseModel(result=executive_summary_response)
