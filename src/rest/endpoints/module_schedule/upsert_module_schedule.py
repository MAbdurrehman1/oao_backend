from fastapi import Depends, Security
from pydantic import BaseModel

from entity import User
from services import upsert_module_schedule
from ..dependencies import EmployeeRequired, auth_header
from ...router import router, Tags


class UpsertModuleScheduleRequestModel(BaseModel):
    date: str


class UpsertModuleScheduleResponseModel(BaseModel):
    result: str = "Module schedule created successfully."


@router.post("/modules/{_id}/schedules/", tags=[Tags.participation])
def upsert_module_schedule_endpoint(
    _id: int,
    payload: UpsertModuleScheduleRequestModel,
    user: User = Depends(EmployeeRequired()),
    __: str = Security(auth_header),
) -> UpsertModuleScheduleResponseModel:
    assert isinstance(user.id, int)
    upsert_module_schedule(
        user_id=user.id,
        selected_date_str=payload.date,
        module_id=_id,
    )
    return UpsertModuleScheduleResponseModel()
