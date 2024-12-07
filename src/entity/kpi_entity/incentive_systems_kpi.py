from dataclasses import dataclass

from .abc_kpi import AbstractKPI
from .leadership_kpi import LeadershipKPI


@dataclass
class IncentiveSystemsKPI(AbstractKPI[LeadershipKPI]):
    name: str = "INCENTIVE_SYSTEMS"
    dict_key: str = "Incentive Systems"
