from dataclasses import dataclass

from .abstract_exception import AbstractException
from .errors import UNIQUE_ARGUMENT_ERROR


@dataclass(kw_only=True)
class UniqueException(AbstractException):
    arg: str
    value: str
    message: str = UNIQUE_ARGUMENT_ERROR
