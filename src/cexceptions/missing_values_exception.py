from dataclasses import dataclass

from .abstract_exception import AbstractException
from .errors import MISSING_VALUES_ERROR


@dataclass(kw_only=True)
class MissingValuesException(AbstractException):
    entities: str
    values: str
    message: str = MISSING_VALUES_ERROR
