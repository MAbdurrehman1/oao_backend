from datetime import datetime

from pydantic import BaseModel, validator

from .organization import Organization


class BusinessUnit(BaseModel):
    name: str
    organization: Organization | None = None
    parent_id: int | None = None
    organization_id: int | None = None
    id: int | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    @validator("organization_id", pre=True, always=True)
    @classmethod
    def set_organization_id(cls, v, values):
        if "organization" in values and values["organization"] is not None:
            return values["organization"].id
        return v
