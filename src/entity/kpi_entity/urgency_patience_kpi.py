from dataclasses import dataclass

from .abc_kpi import AbstractKPI
from .urgency_kpi import UrgencyKPI


@dataclass
class UrgencyPatienceKPI(AbstractKPI[UrgencyKPI]):
    name: str = "URGENCY_PATIENCE"
    dict_key: str = "Urgency Patience"
