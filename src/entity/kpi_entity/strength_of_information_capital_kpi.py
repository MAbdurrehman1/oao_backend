from dataclasses import dataclass

from .abc_kpi import AbstractKPI
from .info_capital_kpi import InfoCapitalKPI


@dataclass
class StrengthOfInformationCapitalKPI(AbstractKPI[InfoCapitalKPI]):
    name: str = "STRENGTH_OF_INFORMATION_CAPITAL"
    dict_key: str = "Strength of Information Capital"
