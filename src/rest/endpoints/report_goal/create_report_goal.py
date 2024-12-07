from fastapi import Depends, Security
from pydantic import BaseModel

from entity import User
from services import create_report_goal
from ..dependencies import ManagerRequired, auth_header
from ...router import router, Tags


class CreateReportGoalRequestModel(BaseModel):
    title: str
    description: str
    focus_area: str


class CreateReportGoalResponseModel(BaseModel):
    result: str = "Report Goal Created Successfully"


@router.post("/reports/{_id}/goals/", tags=[Tags.admin])
def create_report_goal_endpoint(
    _id: int,
    payload: CreateReportGoalRequestModel,
    user: User = Depends(ManagerRequired()),
    __: str = Security(auth_header),
) -> CreateReportGoalResponseModel:
    assert isinstance(user.id, int)
    create_report_goal(
        report_id=_id,
        user_id=user.id,
        title=payload.title,
        description=payload.description,
        focus_area=payload.focus_area,
    )
    return CreateReportGoalResponseModel()
