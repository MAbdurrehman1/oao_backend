from datetime import datetime
from typing import Self

from pydantic import BaseModel, validator

from .business_unit import BusinessUnit
from .kpi_entity import ValuedKPI
from .report import Report


class ReportKPI(BaseModel):
    name: str
    score: int
    standard_deviation: int
    business_unit: BusinessUnit | None = None
    business_unit_id: int | None = None
    report: Report | None = None
    report_id: int | None = None
    id: int | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    @validator("report_id", pre=True, always=True)
    @classmethod
    def set_report_id(cls, v, values):
        if "report" in values and values["report"]:
            return values["report"].id
        return v

    @classmethod
    def from_valued_kpi(
        cls,
        valued_kpi: ValuedKPI,
        business_unit_id: int | None = None,
    ) -> Self:
        return cls(
            name=valued_kpi.kpi.name,
            score=valued_kpi.value.score,
            standard_deviation=valued_kpi.value.standard_deviation,
            report_id=valued_kpi.value.report_id,
            business_unit_id=business_unit_id,
        )
