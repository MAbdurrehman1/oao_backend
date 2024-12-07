from datetime import datetime

from pydantic import BaseModel, validator

from .file import File
from .deep_dive import DeepDive


class OAOContent(BaseModel):
    title: str
    short_description: str
    long_description: str
    content_url: str
    deep_dive: DeepDive | None = None
    thumbnail: File | None = None
    deep_dive_id: int | None = None
    thumbnail_id: int | None = None
    id: int | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    @validator("deep_dive_id", pre=True, always=True)
    @classmethod
    def set_deep_dive_id(cls, v, values):
        if "deep_dive" in values and values["deep_dive"]:
            return values["deep_dive"].id
        return v

    @validator("thumbnail_id", pre=True, always=True)
    @classmethod
    def set_thumbnail_id(cls, v, values):
        if "thumbnail" in values and values["thumbnail"]:
            return values["thumbnail"].id
        return v
