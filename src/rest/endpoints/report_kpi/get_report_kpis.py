from typing import Self
from datetime import datetime

from fastapi import Depends, Security
from pydantic import BaseModel

from entity import User, ReportKPI
from services import get_report_kpis
from settings import configs
from ..dependencies import AdminOrManagerRequired, auth_header
from ...router import router, Tags


class KPIResponse(BaseModel):
    id: int
    name: str
    score: int
    report_id: int
    standard_deviation: int
    created_at: str
    updated_at: str

    @classmethod
    def from_entity(cls, entity: ReportKPI) -> Self:
        assert isinstance(entity.report_id, int)
        assert isinstance(entity.id, int)
        assert isinstance(entity.created_at, datetime)
        assert isinstance(entity.updated_at, datetime)
        return cls(
            name=entity.name,
            score=entity.score,
            standard_deviation=entity.standard_deviation,
            report_id=entity.report_id,
            id=entity.id,
            created_at=entity.created_at.strftime(configs.date_time_format),
            updated_at=entity.created_at.strftime(configs.date_time_format),
        )


class GetReportKPIsResponseModel(BaseModel):
    result: list[KPIResponse]
    hierarchy: dict


@router.get("/report/{_id}/kpis/", tags=[Tags.management])
def get_report_kpis_endpoint(
    _id: int,
    benchmark_id: int | None = None,
    parent_kpi: str | None = None,
    user: User = Depends(AdminOrManagerRequired()),
    __: str = Security(auth_header),
) -> GetReportKPIsResponseModel:
    kpis_list, hierarchy = get_report_kpis(
        report_id=_id,
        parent_kpi=parent_kpi,
        is_admin=user.is_admin,
        benchmark_id=benchmark_id,
    )
    return GetReportKPIsResponseModel(
        hierarchy=hierarchy, result=[KPIResponse.from_entity(kpi) for kpi in kpis_list]
    )
