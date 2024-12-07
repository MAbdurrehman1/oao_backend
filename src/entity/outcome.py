from datetime import datetime
from pydantic import BaseModel, validator

from .oao_content import OAOContent


class Outcome(BaseModel):
    title: str
    description: str
    oao_content: OAOContent | None = None
    oao_content_id: int | None = None
    id: int | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    @validator("oao_content_id", pre=True, always=True)
    @classmethod
    def set_oao_content_id(cls, v, values):
        if "oao_content" in values and values["oao_content"]:
            return values["oao_content"].id
        return v
