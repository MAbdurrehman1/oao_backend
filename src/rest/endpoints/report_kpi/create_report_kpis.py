from fastapi import Depends, Security
from pydantic import BaseModel

from services import create_report_kpis
from ..dependencies import ETLRequired, auth_header
from ...router import router, Tags


class CreateReportKPIsRequestModel(BaseModel):
    kpi_data: dict


class CreateReportKPIsResponseModel(BaseModel):
    result: str = "Report KPIs Created Successfully"


@router.post("/report/{_id}/kpis/", tags=[Tags.etl])
def create_report_kpis_endpoint(
    _id: int,
    payload: CreateReportKPIsRequestModel,
    _: bool = Depends(ETLRequired()),
    __: str = Security(auth_header),
) -> CreateReportKPIsResponseModel:
    create_report_kpis(report_id=_id, kpi_data=payload.kpi_data)
    return CreateReportKPIsResponseModel()
