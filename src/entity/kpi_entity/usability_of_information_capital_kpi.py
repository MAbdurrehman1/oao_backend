from dataclasses import dataclass

from .abc_kpi import AbstractKPI
from .info_capital_kpi import InfoCapitalKPI


@dataclass
class UsabilityOfInformationCapitalKPI(AbstractKPI[InfoCapitalKPI]):
    name: str = "USABILITY_OF_INFORMATION_CAPITAL"
    dict_key: str = "Usability of Information Capital"
