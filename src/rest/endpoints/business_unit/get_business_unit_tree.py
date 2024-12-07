from fastapi import Depends, Security
from pydantic import BaseModel

from entity import User, BusinessUnitHierarchy
from services import get_business_units_tree
from ..dependencies import AdminRequired, auth_header
from ...router import router, Tags


class GetBusinessUnitTreeResponseModel(BaseModel):
    result: BusinessUnitHierarchy | None


@router.get("/organizations/{_id}/business-units/", tags=[Tags.admin])
def get_business_unit_tree_endpoint(
    _id,
    _: User = Depends(AdminRequired()),
    __: str = Security(auth_header),
) -> GetBusinessUnitTreeResponseModel:
    result = get_business_units_tree(organization_id=_id)
    return GetBusinessUnitTreeResponseModel(result=result)
