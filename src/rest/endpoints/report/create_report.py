from fastapi import Depends, Security
from pydantic import BaseModel

from entity import User
from services import create_report
from ..dependencies import AdminRequired, auth_header
from ...router import router, Tags


class CreateReportRequestModel(BaseModel):
    management_position_id: int
    title: str
    end_date: str
    start_date: str | None = None


class CreateReportResponseModel(BaseModel):
    result: str = "Report Creation Request Submitted"


@router.post("/reports/", tags=[Tags.admin])
def create_report_endpoint(
    payload: CreateReportRequestModel,
    _: User = Depends(AdminRequired()),
    __: str = Security(auth_header),
):
    create_report(
        position_id=payload.management_position_id,
        title=payload.title,
        end_date_str=payload.end_date,
        start_date_str=payload.start_date,
    )
    return CreateReportResponseModel()
