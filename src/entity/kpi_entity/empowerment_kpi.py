from dataclasses import dataclass

from .abc_kpi import AbstractKPI
from .readiness_kpi import ReadinessKPI


@dataclass
class EmpowermentKPI(AbstractKPI[ReadinessKPI]):
    name: str = "EMPOWERMENT"
    dict_key: str = "Empowerment"
