from pydantic import BaseModel


class ExecutiveSummary(BaseModel):
    snapshots: int
    recommendations_generated: int
    ideas_reviewed: int
    key_insights: int
    speed_of_transformation: int
