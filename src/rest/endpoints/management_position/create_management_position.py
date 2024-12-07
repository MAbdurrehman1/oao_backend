from fastapi import Depends
from pydantic import BaseModel

from entity import User
from services import create_management_position
from ..dependencies import AdminRequired
from ...router import router, Tags


class CreateManagementPositionRequestModel(BaseModel):
    name: str
    business_unit_ids: list[int]


class CreateManagementPositionResponseModel(BaseModel):
    result: str = "Management Position Created Successfully"


@router.post(
    "/organizations/{organization_id}/management-positions/",
    tags=[Tags.admin],
)
def create_management_position_endpoint(
    organization_id: int,
    payload: CreateManagementPositionRequestModel,
    _: User = Depends(AdminRequired()),
) -> CreateManagementPositionResponseModel:
    create_management_position(
        organization_id=organization_id,
        name=payload.name,
        business_unit_ids=payload.business_unit_ids,
    )
    return CreateManagementPositionResponseModel()
