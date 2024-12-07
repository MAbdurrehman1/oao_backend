from dataclasses import dataclass

from .abc_kpi import AbstractKPI
from .leadership_kpi import LeadershipKPI


@dataclass
class LeadershipStrengthKPI(AbstractKPI[LeadershipKPI]):
    name: str = "LEADERSHIP_STRENGTH"
    dict_key: str = "Leadership Strength"
