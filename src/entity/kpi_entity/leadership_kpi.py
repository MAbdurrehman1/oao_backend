from dataclasses import dataclass

from .abc_kpi import AbstractKPI
from .guidance_kpi import GuidanceKPI


@dataclass
class LeadershipKPI(AbstractKPI[GuidanceKPI]):
    name: str = "LEADERSHIP"
    dict_key: str = "Leadership"
