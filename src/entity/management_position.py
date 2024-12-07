from datetime import datetime

from pydantic import BaseModel, validator

from .business_unit import BusinessUnit
from .organization import Organization
from .employee import Employee


class ManagementPosition(BaseModel):
    name: str
    organization: Organization | None = None
    roles: list[BusinessUnit] | None = None
    managers: list[Employee] | None = None
    managers_count: int | None = None
    pending_participants_count: int | None = None
    last_report_end_date: datetime | None = None
    manager_ids: list[int] | None = None
    organization_id: int | None = None
    role_ids: list[int] | None = None
    id: int | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    @validator("role_ids", pre=True, always=True)
    @classmethod
    def set_role_ids(cls, v, values):
        if "roles" in values and values["roles"]:
            return [role.id for role in values["roles"]]
        return v

    @validator("manager_ids", pre=True, always=True)
    @classmethod
    def set_manager_ids(cls, v, values):
        if "managers" in values and values["managers"]:
            return [manager.id for manager in values["managers"]]
        return v

    @validator("organization_id", pre=True, always=True)
    @classmethod
    def set_organization_id(cls, v, values):
        if "organization" in values and values["organization"]:
            return values["organization"].id
        return v
