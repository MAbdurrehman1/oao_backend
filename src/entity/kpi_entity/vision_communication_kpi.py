from dataclasses import dataclass

from .abc_kpi import AbstractKPI
from .vision_kpi import VisionKPI


@dataclass
class VisionCommunicationKPI(AbstractKPI[VisionKPI]):
    name: str = "VISION_COMMUNICATION"
    dict_key: str = "Vision Communication"
