from fastapi import Depends, Security
from pydantic import BaseModel

from entity import User
from services import update_business_unit
from ..dependencies import AdminRequired, auth_header
from ...router import router, Tags


class UpdateBusinessUnitRequestModel(BaseModel):
    name: str
    parent_id: int | None


class UpdateBusinessUnitResponseModel(BaseModel):
    result: str = "Business Unit Updated Successfully"


@router.put(
    "/organizations/{organization_id}/business-units/{business_unit_id}/",
    tags=[Tags.admin],
)
def update_business_unit_endpoint(
    organization_id,
    business_unit_id,
    payload: UpdateBusinessUnitRequestModel,
    _: User = Depends(AdminRequired()),
    __: str = Security(auth_header),
) -> UpdateBusinessUnitResponseModel:
    update_business_unit(
        organization_id=organization_id,
        _id=business_unit_id,
        name=payload.name,
        parent_id=payload.parent_id,
    )
    return UpdateBusinessUnitResponseModel()
