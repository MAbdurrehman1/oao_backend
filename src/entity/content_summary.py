from datetime import datetime

from pydantic import BaseModel

from entity import Module


class ContentSummary(BaseModel):
    title: str
    description: str
    module: Module | None = None
    module_id: int | None = None
    id: int | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
