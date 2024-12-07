from datetime import datetime
from typing import Self

from fastapi import Depends, Security
from pydantic import BaseModel

from entity import User, ManagementPosition
from services import get_management_position_details
from settings import configs
from ..dependencies import AdminRequired, auth_header
from ...router import router, Tags


class RolesResponse(BaseModel):
    id: int
    name: str


class ManagerResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str


class ManagementPositionResponse(BaseModel):
    id: int
    name: str
    roles: list[RolesResponse]
    managers: list[ManagerResponse]
    last_report_end_date: str
    pending_participants_count: int

    @classmethod
    def from_entity(cls, management_position: ManagementPosition) -> Self:
        assert isinstance(management_position.roles, list)
        role_responses = [
            RolesResponse(name=role.name, id=role.id)  # type: ignore
            for role in management_position.roles
        ]
        manager_responses = [
            ManagerResponse(
                id=employee.id,  # type: ignore
                first_name=employee.user.first_name,  # type: ignore
                last_name=employee.user.last_name,  # type: ignore
                email=employee.user.email,  # type: ignore
            )
            for employee in management_position.managers  # type: ignore
        ]
        assert isinstance(management_position.id, int)
        assert isinstance(management_position.pending_participants_count, int)
        assert isinstance(management_position.last_report_end_date, datetime)
        return cls(
            id=management_position.id,
            name=management_position.name,
            roles=role_responses,
            managers=manager_responses,
            pending_participants_count=management_position.pending_participants_count,
            last_report_end_date=management_position.last_report_end_date.strftime(
                configs.date_time_format
            ),
        )


class GetManagementPositionDetailsResponseModel(BaseModel):
    result: ManagementPositionResponse


@router.get(
    "/organizations/{organization_id}/management-positions/{position_id}/",
    tags=[Tags.admin],
)
def get_management_position_details_endpoint(
    position_id: int,
    _: User = Depends(AdminRequired()),
    __: str = Security(auth_header),
):
    management_position = get_management_position_details(position_id=position_id)
    response_model = ManagementPositionResponse.from_entity(management_position)
    return GetManagementPositionDetailsResponseModel(result=response_model)
