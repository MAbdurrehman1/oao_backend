from dataclasses import dataclass

from .abc_kpi import AbstractKPI
from .empowerment_kpi import EmpowermentKPI


@dataclass
class OrganizationalSupportKPI(AbstractKPI[EmpowermentKPI]):
    name: str = "ORGANIZATIONAL_SUPPORT"
    dict_key: str = "Organizational Support"
