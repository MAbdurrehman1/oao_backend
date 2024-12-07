from datetime import datetime

from pydantic import BaseModel, validator

from .management_position import ManagementPosition
from settings import ReportStatus


class Report(BaseModel):
    title: str
    management_position: ManagementPosition | None = None
    end_date: datetime | None = None
    management_position_id: int | None = None
    status: ReportStatus | None = None
    id: int | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    @validator("management_position_id", pre=True, always=True)
    @classmethod
    def set_management_position_id(cls, v, values):
        if "management_position" in values and values["management_position"]:
            return values["management_position"].id
        return v
