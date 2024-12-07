from dataclasses import dataclass

from .abstract_exception import AbstractException
from .errors import INVALID_ARGUMENT_ERROR


@dataclass(kw_only=True)
class ValidationException(AbstractException):
    entities: str
    values: str
    message: str = INVALID_ARGUMENT_ERROR
