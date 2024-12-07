from datetime import datetime

from pydantic import BaseModel, validator

from .file import File
from .information_library import InformationLibrary


class LibraryContent(BaseModel):
    title: str
    description: str
    content_url: str
    information_library: InformationLibrary | None = None
    thumbnail: File | None = None
    information_library_id: int | None = None
    thumbnail_id: int | None = None
    id: int | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    @validator("information_library_id", pre=True, always=True)
    @classmethod
    def set_information_library_id(cls, v, values):
        if "information_library" in values and values["information_library"]:
            return values["information_library"].id
        return v

    @validator("thumbnail_id", pre=True, always=True)
    @classmethod
    def set_thumbnail_id(cls, v, values):
        if "thumbnail" in values and values["thumbnail"]:
            return values["thumbnail"].id
        return v
