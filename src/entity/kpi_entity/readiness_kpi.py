from dataclasses import dataclass

from .abc_kpi import AbstractKPI
from .general_kpi import GeneralKPI


@dataclass
class ReadinessKPI(AbstractKPI[GeneralKPI]):
    name: str = "READINESS"
    dict_key: str = "Readiness"
