from fastapi import Depends, Security
from pydantic import BaseModel

from entity import User
from services import create_business_unit
from ..dependencies import AdminRequired, auth_header
from ...router import router, Tags


class CreateBusinessUnitRequestModel(BaseModel):
    name: str
    parent_id: int | None


class CreateBusinessUnitResponseModel(BaseModel):
    result: str = "Business Unit Created Successfully"


@router.post("/organizations/{_id}/business-units/", tags=[Tags.admin])
def create_business_unit_endpoint(
    _id,
    payload: CreateBusinessUnitRequestModel,
    _: User = Depends(AdminRequired()),
    __: str = Security(auth_header),
) -> CreateBusinessUnitResponseModel:
    create_business_unit(
        organization_id=_id, name=payload.name, parent_id=payload.parent_id
    )
    return CreateBusinessUnitResponseModel()
