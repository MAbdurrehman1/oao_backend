from copy import deepcopy
from dataclasses import dataclass

from .abc_kpi import AbstractKPI


@dataclass
class GeneralKPI(AbstractKPI):
    name: str = "GENERAL"

    @classmethod
    def _get_dict_keys(cls) -> list[str]:
        parent_keys = super()._get_dict_keys()
        keys = deepcopy(parent_keys)
        if cls.dict_key:
            keys.append(cls.dict_key)
        return keys
