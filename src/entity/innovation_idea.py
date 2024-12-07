from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from entity import Employee


class InnovationIdea(BaseModel):
    title: str
    description: str
    feasibility_score: int
    confidence_score: int
    impact_score: int
    employee: Employee | None = None
    participation_id: UUID | None = None
    id: int | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    rate: int | None = None
