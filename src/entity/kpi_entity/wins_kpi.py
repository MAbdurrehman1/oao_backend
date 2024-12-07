from dataclasses import dataclass

from .abc_kpi import AbstractKPI
from .execution_kpi import ExecutionKPI


@dataclass
class WinsKPI(AbstractKPI[ExecutionKPI]):
    name: str = "WINS"
    dict_key: str = "Wins"
