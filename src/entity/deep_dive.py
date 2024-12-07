from datetime import datetime

from pydantic import BaseModel, validator

from entity import File


class DeepDive(BaseModel):
    title: str
    description: str | None
    slug: str | None = None
    thumbnail: File | None = None
    thumbnail_id: int | None = None
    id: int | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    @validator("thumbnail_id", pre=True, always=True)
    @classmethod
    def set_thumbnail_id(cls, v, values):
        if "thumbnail" in values and values["thumbnail"]:
            return values["thumbnail"].id
        return v
