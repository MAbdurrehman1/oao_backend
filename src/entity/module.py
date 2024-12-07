from datetime import datetime

from pydantic import BaseModel, validator

from entity import File


class Module(BaseModel):
    title: str
    description: str
    duration: int
    order: int
    animated_thumbnail: File | None = None
    still_thumbnail: File | None = None
    end_date: datetime | None = None
    url: str | None = None
    animated_thumbnail_id: int | None = None
    still_thumbnail_id: int | None = None
    id: int | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    @validator("animated_thumbnail_id", pre=True, always=True)
    @classmethod
    def set_animated_thumbnail_id(cls, v, values):
        if "animated_thumbnail" in values and values["animated_thumbnail"]:
            return values["animated_thumbnail"].id
        return v

    @validator("still_thumbnail_id", pre=True, always=True)
    @classmethod
    def set_still_thumbnail_id(cls, v, values):
        if "still_thumbnail" in values and values["still_thumbnail"]:
            return values["still_thumbnail"].id
        return v
