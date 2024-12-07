from dataclasses import dataclass

from .abc_kpi import AbstractKPI
from .wins_kpi import WinsKPI


@dataclass
class AwarenessOfSuccessfulWinsKPI(AbstractKPI[WinsKPI]):
    name: str = "AWARENESS_OF_SUCCESSFUL_WINS"
    dict_key: str = "Awareness of Successful Wins"
