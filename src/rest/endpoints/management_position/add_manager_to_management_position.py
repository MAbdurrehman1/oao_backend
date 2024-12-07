from fastapi import Depends, Security
from pydantic import BaseModel

from entity import User
from services import add_manager_to_management_position
from ..dependencies import AdminRequired, auth_header
from ...router import router, Tags


class AddManagerResponseModel(BaseModel):
    result: str = "Manager Added Successfully"


class AddManagerRequestModel(BaseModel):
    employee_email: str


@router.post(
    "/organizations/{organization_id}/management-positions/{position_id}/add-manager/",
    tags=[Tags.admin],
)
def add_manager_to_management_position_endpoint(
    payload: AddManagerRequestModel,
    organization_id: int,
    position_id: int,
    _: User = Depends(AdminRequired()),
    __: str = Security(auth_header),
) -> AddManagerResponseModel:
    add_manager_to_management_position(
        organization_id=organization_id,
        management_position_id=position_id,
        manager_email=payload.employee_email,
    )
    return AddManagerResponseModel()
