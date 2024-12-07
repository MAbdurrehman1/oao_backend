from uuid import UUID

from pydantic import BaseModel, validator

from .survey_campaign import SurveyCampaign
from .employee import Employee
from settings import ParticipationStatus


class Participant(BaseModel):
    status: ParticipationStatus
    id: UUID | None = None
    employee: Employee | None = None
    survey_campaign: SurveyCampaign | None = None
    employee_id: int | None = None
    survey_campaign_id: int | None = None

    @validator("employee_id", pre=True, always=True)
    @classmethod
    def set_employee_id(cls, v, values):
        if "employee" in values and values["employee"]:
            return values["employee"].id
        return v

    @validator("survey_campaign_id", pre=True, always=True)
    @classmethod
    def set_survey_campaign_id(cls, v, values):
        if "survey_campaign" in values and values["survey_campaign"]:
            return values["survey_campaign"].id
        return v
