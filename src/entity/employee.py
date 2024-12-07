from datetime import datetime

from pydantic import BaseModel, validator

from .business_unit import BusinessUnit
from .organization import Organization
from .user import User


class Employee(BaseModel):
    role_title: str
    location: str
    organization: Organization | None = None
    business_unit: BusinessUnit | None = None
    user: User | None = None
    user_id: int | None = None
    organization_id: int | None = None
    business_unit_id: int | None = None
    id: int | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    @validator("business_unit_id", pre=True, always=True)
    @classmethod
    def set_business_unit_ids(cls, v, values):
        if "business_unit" in values and values["business_unit"]:
            return values["business_unit"].id
        return v

    @validator("user_id", pre=True, always=True)
    @classmethod
    def set_user_id(cls, v, values):
        if "user" in values and values["user"]:
            return values["user"].id
        return v

    @validator("organization_id", pre=True, always=True)
    @classmethod
    def set_organization_id(cls, v, values):
        if "organization" in values and values["organization"]:
            return values["organization"].id
        return v
