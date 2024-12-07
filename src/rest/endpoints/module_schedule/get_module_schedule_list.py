from datetime import datetime
from typing import Self

from fastapi import Depends, Security
from pydantic import BaseModel

from entity import User, ModuleSchedule
from services import get_module_schedules_list
from settings import configs
from ..dependencies import EmployeeRequired, auth_header
from ...router import router, Tags


class ModuleScheduleResponse(BaseModel):
    module_id: int
    participation_id: str
    selected_date: str
    id: int
    created_at: str
    updated_at: str

    @classmethod
    def from_entity(cls, entity: ModuleSchedule) -> Self:
        assert isinstance(entity.id, int)
        assert isinstance(entity.module_id, int)
        assert isinstance(entity.created_at, datetime)
        assert isinstance(entity.updated_at, datetime)
        return cls(
            id=entity.id,
            module_id=entity.module_id,
            participation_id=str(entity.participation_id),
            selected_date=entity.selected_date.strftime(configs.date_time_format),
            created_at=entity.created_at.strftime(configs.date_time_format),
            updated_at=entity.updated_at.strftime(configs.date_time_format),
        )


class GetModuleScheduleListResponseModel(BaseModel):
    result: list[ModuleScheduleResponse]


@router.get("/module-schedules/", tags=[Tags.participation])
def get_module_schedule_list_endpoint(
    user: User = Depends(EmployeeRequired()),
    __: str = Security(auth_header),
) -> GetModuleScheduleListResponseModel:
    assert isinstance(user.id, int)
    schedules_list = get_module_schedules_list(
        user_id=user.id,
    )
    response_models = [ModuleScheduleResponse.from_entity(m) for m in schedules_list]
    return GetModuleScheduleListResponseModel(result=response_models)
