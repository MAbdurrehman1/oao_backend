from dataclasses import dataclass

from .abc_kpi import AbstractKPI
from .urgency_kpi import UrgencyKPI


@dataclass
class UrgencyStrengthKPI(AbstractKPI[UrgencyKPI]):
    name: str = "URGENCY_STRENGTH"
    dict_key: str = "Urgency Strength"
