from dataclasses import dataclass

from .abc_kpi import AbstractKPI
from .general_kpi import GeneralKPI


@dataclass
class GuidanceKPI(AbstractKPI[GeneralKPI]):
    name: str = "GUIDANCE"
    dict_key: str = "Guidance"
