from typing import Self

from fastapi import Depends, Security
from pydantic import BaseModel

from entity import User, Report, ManagementPosition
from services import get_manager_reports_list
from ..dependencies import ManagerRequired, auth_header
from ...router import router, Tags


class ManagementPositionResponse(BaseModel):
    id: int
    name: str


class ReportResponse(BaseModel):
    id: int
    management_position: ManagementPositionResponse

    @classmethod
    def from_entity(cls, report: Report) -> Self:
        assert isinstance(report.id, int)
        assert isinstance(report.management_position, ManagementPosition)
        assert isinstance(report.management_position.id, int)
        management_position = ManagementPositionResponse(
            name=report.management_position.name, id=report.management_position.id
        )
        return cls(
            id=report.id,
            management_position=management_position,
        )


class GetReportsListResponseModel(BaseModel):
    total_count: int
    result: list[ReportResponse]


@router.get("/manager/{_id}/reports/", tags=[Tags.admin])
def get_manager_reports_list_endpoint(
    _id: int,
    offset: int = 0,
    limit: int = 5,
    _: User = Depends(ManagerRequired()),
    __: str = Security(auth_header),
):
    total_count, reports = get_manager_reports_list(
        offset=offset, limit=limit, manager_id=_id
    )
    response_models = [ReportResponse.from_entity(r) for r in reports]
    return GetReportsListResponseModel(
        result=response_models,
        total_count=total_count,
    )
