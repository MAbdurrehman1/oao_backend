from datetime import datetime
from typing import Self

from fastapi import Depends, Security
from pydantic import BaseModel

from entity import User, Report
from entity.management_position import ManagementPosition
from services import get_organization_reports
from settings import configs, ReportStatus
from ..dependencies import AdminRequired, auth_header
from ...router import router, Tags


class ManagementPositionResponse(BaseModel):
    id: int
    name: str


class ReportResponse(BaseModel):
    title: str
    end_date: str
    management_position: ManagementPositionResponse
    id: int
    status: ReportStatus
    created_at: str
    updated_at: str

    @classmethod
    def from_report(cls, report: Report) -> Self:
        assert isinstance(report.id, int)
        assert isinstance(report.title, str)
        assert isinstance(report.end_date, datetime)
        assert isinstance(report.created_at, datetime)
        assert isinstance(report.updated_at, datetime)
        assert isinstance(report.status, ReportStatus)
        assert isinstance(report.management_position, ManagementPosition)
        assert isinstance(report.management_position.id, int)
        management_position = ManagementPositionResponse(
            name=report.management_position.name, id=report.management_position.id
        )
        return cls(
            id=report.id,
            title=report.title,
            end_date=report.end_date.strftime(configs.date_time_format),
            management_position=management_position,
            status=report.status,
            created_at=report.created_at.strftime(configs.date_time_format),
            updated_at=report.updated_at.strftime(configs.date_time_format),
        )


class GetReportResponseModel(BaseModel):
    total_count: int
    result: list[ReportResponse]


@router.get("/organizations/{_id}/reports/", tags=[Tags.admin])
def get_organization_reports_endpoint(
    _id: int,
    offset: int = 0,
    limit: int = 10,
    _: User = Depends(AdminRequired()),
    __: str = Security(auth_header),
) -> GetReportResponseModel:
    total_count, reports = get_organization_reports(
        organization_id=_id,
        offset=offset,
        limit=limit,
    )
    return GetReportResponseModel(
        total_count=total_count,
        result=[ReportResponse.from_report(report) for report in reports],
    )
