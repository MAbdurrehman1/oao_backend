from dataclasses import dataclass

from .abc_kpi import AbstractKPI
from .empowerment_kpi import EmpowermentKPI


@dataclass
class PeopleReadinessKPI(AbstractKPI[EmpowermentKPI]):
    name: str = "PEOPLE_READINESS"
    dict_key: str = "People Readiness"
