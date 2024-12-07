from dataclasses import dataclass

from .abc_kpi import AbstractKPI
from .guidance_kpi import GuidanceKPI


@dataclass
class VisionKPI(AbstractKPI[GuidanceKPI]):
    name: str = "VISION"
    dict_key: str = "Vision"
