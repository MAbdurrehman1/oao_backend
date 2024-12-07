from dataclasses import dataclass

from .abc_kpi import AbstractKPI
from .execution_kpi import ExecutionKPI


@dataclass
class InfoCapitalKPI(AbstractKPI[ExecutionKPI]):
    name: str = "INFO_CAPITAL"
    dict_key: str = "Info Capital"
