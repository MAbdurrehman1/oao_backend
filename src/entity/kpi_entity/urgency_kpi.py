from dataclasses import dataclass

from .abc_kpi import AbstractKPI
from .readiness_kpi import ReadinessKPI


@dataclass
class UrgencyKPI(AbstractKPI[ReadinessKPI]):
    name: str = "URGENCY"
    dict_key: str = "Urgency"
