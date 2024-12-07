from datetime import datetime
from typing import Self

from fastapi import Depends, Security
from pydantic import BaseModel

from entity import User, ReportGoal
from services import get_report_goals
from settings import configs
from ..dependencies import AdminOrManagerRequired, auth_header
from ...router import router, Tags


class ReportGoalResponse(BaseModel):
    id: int
    title: str
    manager_id: int
    description: str
    focus_area: str
    created_at: str
    updated_at: str

    @classmethod
    def from_entity(cls, report_goal: ReportGoal) -> Self:
        assert isinstance(report_goal.id, int)
        assert isinstance(report_goal.manager_id, int)
        assert isinstance(report_goal.created_at, datetime)
        assert isinstance(report_goal.updated_at, datetime)
        return cls(
            id=report_goal.id,
            manager_id=report_goal.manager_id,
            title=report_goal.title,
            description=report_goal.description,
            focus_area=report_goal.focus_area,
            created_at=report_goal.created_at.strftime(configs.date_time_format),
            updated_at=report_goal.updated_at.strftime(configs.date_time_format),
        )


class GetReportGoalsResponseModel(BaseModel):
    total_count: int
    result: list[ReportGoalResponse]


@router.get("/reports/{_id}/goals/", tags=[Tags.management])
async def get_report_goals_endpoint(
    _id: int,
    focus_area: str | None = None,
    offset: int = 0,
    limit: int = 10,
    user: User = Depends(AdminOrManagerRequired()),
    __: str = Security(auth_header),
) -> GetReportGoalsResponseModel:
    assert isinstance(user.id, int)
    total_count, report_goals = get_report_goals(
        report_id=_id,
        focus_area_str=focus_area,
        limit=limit,
        user_id=user.id,
        offset=offset,
        is_admin=user.is_admin,
    )
    return GetReportGoalsResponseModel(
        total_count=total_count,
        result=[ReportGoalResponse.from_entity(goal) for goal in report_goals],
    )
