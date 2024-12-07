from pydantic import BaseModel


class MatrixInnovationIdea(BaseModel):
    id: int | None = None
    title: str
    feasibility_score: int
    confidence_score: int
    impact_score: int
