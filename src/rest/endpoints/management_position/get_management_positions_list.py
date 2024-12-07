from datetime import datetime
from typing import Self

from fastapi import Depends, Security
from pydantic import BaseModel

from entity import User, ManagementPosition
from services import get_management_position_list
from settings import configs
from ..dependencies import AdminRequired, auth_header
from ...router import router, Tags


class RolesResponse(BaseModel):
    id: int
    name: str


class ManagementPositionResponse(BaseModel):
    id: int
    name: str
    roles: list[RolesResponse]
    managers_count: int
    last_report_end_date: str
    pending_participants_count: int

    @classmethod
    def from_entity(cls, management_position: ManagementPosition) -> Self:
        assert isinstance(management_position.roles, list)
        role_responses = [
            RolesResponse(name=role.name, id=role.id)  # type: ignore
            for role in management_position.roles
        ]
        assert isinstance(management_position.id, int)
        assert isinstance(management_position.managers_count, int)
        assert isinstance(management_position.last_report_end_date, datetime)
        assert isinstance(management_position.pending_participants_count, int)
        return cls(
            id=management_position.id,
            name=management_position.name,
            roles=role_responses,
            managers_count=management_position.managers_count,
            pending_participants_count=management_position.pending_participants_count,
            last_report_end_date=management_position.last_report_end_date.strftime(
                configs.date_time_format
            ),
        )


class GetManagementPositionsListResponseModel(BaseModel):
    total_count: int
    result: list[ManagementPositionResponse]


@router.get("/organizations/{_id}/management-positions/", tags=[Tags.admin])
def get_management_positions_list_endpoint(
    _id: int,
    offset: int = 0,
    limit: int = 5,
    _: User = Depends(AdminRequired()),
    __: str = Security(auth_header),
):
    total_count, management_positions = get_management_position_list(
        offset=offset, limit=limit, organization_id=_id
    )
    response_models = [
        ManagementPositionResponse.from_entity(mp) for mp in management_positions
    ]
    return GetManagementPositionsListResponseModel(
        result=response_models, total_count=total_count
    )
