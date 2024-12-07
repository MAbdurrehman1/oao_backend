from dataclasses import dataclass

from .abc_kpi import AbstractKPI
from .general_kpi import GeneralKPI


@dataclass
class ExecutionKPI(AbstractKPI[GeneralKPI]):
    name: str = "EXECUTION"
    dict_key: str = "Execution"
