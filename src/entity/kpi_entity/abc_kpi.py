import importlib
import inspect
import pkgutil
from copy import deepcopy
from dataclasses import dataclass
from typing import TypeVar, Type, Generic, get_args

K = TypeVar("K", bound="AbstractKPI")


@dataclass
class KPIValue:
    report_id: int
    score: int
    standard_deviation: int


@dataclass
class ValuedKPI:
    kpi: Type["AbstractKPI"]
    value: KPIValue


def _get_score(data: dict) -> tuple[int, int]:
    score = int(data["score"]["score"])
    standard_deviation = int(data["score"]["standard_deviation"])
    return score, standard_deviation


@dataclass
class AbstractKPI(Generic[K]):
    name: str
    dict_key: str | None = None

    @classmethod
    def get_parent(cls) -> Type[K] | None:
        try:
            parent = get_args(cls.__orig_bases__[0])[0]  # type: ignore
            return parent
        except IndexError:
            return None

    @classmethod
    def get_children(cls) -> list[Type["AbstractKPI"]]:
        package = importlib.import_module("entity.kpi_entity")
        package_classes_data = []
        for _, module_name, _ in pkgutil.iter_modules(
            package.__path__, "entity.kpi_entity."
        ):
            module = importlib.import_module(module_name)
            classes_data = inspect.getmembers(module, inspect.isclass)
            package_classes_data.extend(classes_data)
        package_classes = [item[1] for item in set(package_classes_data)]
        children = []
        for _class in package_classes:
            if (
                issubclass(_class, AbstractKPI)
                and get_args(_class.__orig_bases__[0])[0] is cls  # type: ignore
            ):
                children.append(_class)
        return children

    @classmethod
    def assign_value(
        cls, report_id: int, score: int, standard_deviation: int
    ) -> ValuedKPI:
        value = KPIValue(
            report_id=report_id,
            score=score,
            standard_deviation=standard_deviation,
        )
        return ValuedKPI(
            kpi=cls,
            value=value,
        )

    @classmethod
    def _get_dict_keys(cls) -> list[str]:
        parent_class = cls.get_parent()
        try:
            parent_keys = parent_class._get_dict_keys()  # type: ignore
        except AttributeError:
            parent_keys = []
        keys = deepcopy(parent_keys)
        if cls.dict_key:
            keys.append(cls.dict_key)
        return keys

    @classmethod
    def _get_kpi_data(cls, data: dict) -> dict:
        for key in cls._get_dict_keys():
            data = data[key]
        return data

    @classmethod
    def get_valued_kpi(cls, report_id: int, data) -> ValuedKPI:
        kpi_data = cls._get_kpi_data(data)
        score, standard_deviation = _get_score(kpi_data)
        value = KPIValue(
            report_id=report_id,
            score=score,
            standard_deviation=standard_deviation,
        )
        return ValuedKPI(
            kpi=cls,
            value=value,
        )
