from fastapi import Depends, Security
from pydantic import BaseModel

from entity import User
from services import remove_manager_from_management_position
from ..dependencies import AdminRequired, auth_header
from ...router import router, Tags


class RemoveManagerResponseModel(BaseModel):
    result: str = "Manager Removed Successfully"


class RemoveManagerRequestModel(BaseModel):
    manager_id: int


@router.post(
    "/organizations/{org_id}/management-positions/{position_id}/remove-manager/",
    tags=[Tags.admin],
)
def remove_manager_from_management_position_endpoint(
    payload: RemoveManagerRequestModel,
    org_id: int,
    position_id: int,
    _: User = Depends(AdminRequired()),
    __: str = Security(auth_header),
) -> RemoveManagerResponseModel:
    remove_manager_from_management_position(
        organization_id=org_id,
        management_position_id=position_id,
        manager_id=payload.manager_id,
    )
    return RemoveManagerResponseModel()
