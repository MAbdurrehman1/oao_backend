from datetime import datetime

from pydantic import BaseModel, validator

from .employee import Employee
from .report import Report
from settings import FocusArea


class ReportGoal(BaseModel):
    title: str
    description: str
    focus_area: FocusArea
    report: Report | None = None
    manager: Employee | None = None
    report_id: int | None = None
    manager_id: int | None = None
    id: int | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    @validator("report_id", pre=True, always=True)
    @classmethod
    def set_report_id(cls, v, values):
        if "report" in values and values["report"]:
            return values["report"].id
        return v

    @validator("manager_id", pre=True, always=True)
    @classmethod
    def set_manager_id(cls, v, values):
        if "manager" in values and values["manager"]:
            return values["manager"].id
        return v
