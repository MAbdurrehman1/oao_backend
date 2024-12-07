from dataclasses import dataclass

from .abc_kpi import AbstractKPI
from .vision_kpi import VisionKPI


@dataclass
class VisionStrengthKPI(AbstractKPI[VisionKPI]):
    name: str = "VISION_STRENGTH"
    dict_key: str = "Vision Strength"
