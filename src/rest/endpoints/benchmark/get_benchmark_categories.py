from fastapi import Depends, Security
from pydantic import BaseModel

from entity import User, BusinessUnitHierarchy
from services import get_benchmark_categories_hierarchy
from ..dependencies import AdminRequired, auth_header
from ...router import router, Tags


class GetBenchmarkCategoriesResponseModel(BaseModel):
    result: list[BusinessUnitHierarchy]


@router.get("/management-position/{_id}/benchmark-categories/", tags=[Tags.admin])
def get_benchmark_categories_endpoint(
    _id: int,
    _: User = Depends(AdminRequired()),
    __: str = Security(auth_header),
) -> GetBenchmarkCategoriesResponseModel:
    result = get_benchmark_categories_hierarchy(position_id=_id)
    return GetBenchmarkCategoriesResponseModel(result=result)
