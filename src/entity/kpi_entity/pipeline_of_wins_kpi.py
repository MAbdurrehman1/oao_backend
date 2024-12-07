from dataclasses import dataclass

from .abc_kpi import AbstractKPI
from .wins_kpi import WinsKPI


@dataclass
class PipelineOfWinsKPI(AbstractKPI[WinsKPI]):
    name: str = "PIPELINE_OF_WINS"
    dict_key: str = "Pipeline of Wins"
