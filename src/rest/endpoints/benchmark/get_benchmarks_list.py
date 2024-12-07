from typing import Self

from fastapi import Depends, Security
from pydantic import BaseModel

from entity import User, BusinessUnit
from services import get_benchmarks_list
from ..dependencies import ManagerRequired, auth_header
from ...router import router, Tags


class BenchmarkResponse(BaseModel):
    name: str
    id: int

    @classmethod
    def from_entity(cls, entity: BusinessUnit) -> Self:
        assert isinstance(entity.id, int)
        return cls(name=entity.name, id=entity.id)


class GetBenchmarksListResponseModel(BaseModel):
    result: list[BenchmarkResponse]


@router.get("/reports/{_id}/benchmarks/", tags=[Tags.management])
def get_benchmarks_list_endpoint(
    _id: int,
    _: User = Depends(ManagerRequired()),
    __: str = Security(auth_header),
) -> GetBenchmarksListResponseModel:
    result = get_benchmarks_list(report_id=_id)
    business_unit_responses = [
        BenchmarkResponse.from_entity(benchmark) for benchmark in result
    ]
    return GetBenchmarksListResponseModel(result=business_unit_responses)
