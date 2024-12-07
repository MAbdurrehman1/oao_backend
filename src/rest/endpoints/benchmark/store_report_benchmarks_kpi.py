from fastapi import Depends, Security
from pydantic import BaseModel

from entity import User
from services import store_benchmark_kpis
from ..dependencies import ETLRequired, auth_header
from ...router import router, Tags


class BenchmarkRequestModel(BaseModel):
    business_unit_id: int
    kpi_data: dict


class StoreReportBenchmarksRequestModel(BaseModel):
    benchmarks: list[BenchmarkRequestModel]


class StoreReportBenchmarkResponseModel(BaseModel):
    result: str = "Report Benchmarks Stored Successfully"


@router.post("/reports/{_id}/benchmarks/", tags=[Tags.admin])
def store_report_benchmarks_kpi_endpoint(
    _id: int,
    payload: StoreReportBenchmarksRequestModel,
    _: User = Depends(ETLRequired()),
    __: str = Security(auth_header),
) -> StoreReportBenchmarkResponseModel:
    store_benchmark_kpis(report_id=_id, benchmark_kpi_data=payload.dict()["benchmarks"])
    return StoreReportBenchmarkResponseModel()
