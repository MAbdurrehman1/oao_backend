from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, validator

from .participant import Participant
from .module import Module


class ModuleSchedule(BaseModel):
    id: int | None = None
    selected_date: datetime
    module: Module | None = None
    participant: Participant | None = None
    module_id: int | None = None
    participation_id: UUID | None = None
    ms_graph_event_id: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    @validator("participation_id", pre=True, always=True)
    @classmethod
    def set_participation_id(cls, v, values):
        if "participant" in values and values["participant"]:
            return values["participant"].id
        return v

    @validator("module_id", pre=True, always=True)
    @classmethod
    def set_module_id(cls, v, values):
        if "module" in values and values["module"]:
            return values["module"].id
        return v
