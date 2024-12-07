from datetime import datetime

from pydantic import BaseModel, validator

from .deep_dive import DeepDive
from .organization import Organization


class InformationLibrary(BaseModel):
    title: str
    short_description: str
    long_description: str
    organization: Organization | None = None
    deep_dive: DeepDive | None = None
    organization_id: int | None = None
    deep_dive_id: int | None = None
    id: int | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    @validator("deep_dive_id", pre=True, always=True)
    @classmethod
    def set_deep_dive_id(cls, v, values):
        if "deep_dive" in values and values["deep_dive"]:
            return values["deep_dive"].id
        return v

    @validator("organization_id", pre=True, always=True)
    @classmethod
    def set_organization_id(cls, v, values):
        if "organization" in values and values["organization"]:
            return values["organization_id"].id
        return v
