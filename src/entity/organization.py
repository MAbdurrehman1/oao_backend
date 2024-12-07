from datetime import datetime

from pydantic import BaseModel, validator

from .file import File


class Organization(BaseModel):
    company_name: str
    industry: str
    hq_location: str
    size: str
    logo: File | None = None
    meta_data: dict | None = None
    logo_id: int | None = None
    id: int | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    def equal_value(self, other):
        return (
            self.company_name == other.company_name
            and self.industry == other.industry
            and self.hq_location == other.hq_location
            and self.size == other.size
            and self.meta_data == other.meta_data
            and self.logo_id == other.logo_id
        )

    @validator("logo_id", pre=True, always=True)
    @classmethod
    def set_logo_id(cls, v, values):
        if "logo" in values and values["logo"]:
            return values["logo"].id
        return v
