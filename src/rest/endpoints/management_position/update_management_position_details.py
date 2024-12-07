from fastapi import Depends, Security
from pydantic import BaseModel

from entity import User
from services import update_management_position_details
from ..dependencies import AdminRequired, auth_header
from ...router import router, Tags


class UpdateManagementPositionDetailsResponseModel(BaseModel):
    result: str = "Position Updated Successfully"


class UpdateManagementPositionDetailsRequestModel(BaseModel):
    name: str


@router.put(
    "/organizations/{organization_id}/management-positions/{position_id}/",
    tags=[Tags.admin],
)
def update_management_position_details_endpoint(
    position_id: int,
    payload: UpdateManagementPositionDetailsRequestModel,
    _: User = Depends(AdminRequired()),
    __: str = Security(auth_header),
):
    update_management_position_details(position_id=position_id, name=payload.name)
    return UpdateManagementPositionDetailsResponseModel()
