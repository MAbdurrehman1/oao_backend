from datetime import datetime

from pydantic import BaseModel, validator

from .employee import Employee
from .organization import Organization


class SurveyCampaign(BaseModel):
    title: str
    start_date: datetime
    end_date: datetime
    organization: Organization | None = None
    participants: list[Employee] | None = None
    organization_id: int | None = None
    participant_ids: list[int] | None = None
    participants_count: int | None = None
    invited_participants_count: int | None = None
    responded_participants_count: int | None = None
    id: int | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    @validator("participant_ids", pre=True, always=True)
    @classmethod
    def set_user_ids(cls, v, values):
        if "participants" in values and values["participants"]:
            return [item.id for item in values["participants"]]
        return v

    @validator("organization_id", pre=True, always=True)
    @classmethod
    def set_organization_id(cls, v, values):
        if "organization" in values and values["organization"]:
            return values["organization"].id
        return v
