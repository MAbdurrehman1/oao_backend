from dataclasses import dataclass

from cexceptions import AbstractException
from .errors import GREATER_OR_EQUAL_ERROR


@dataclass(kw_only=True)
class GreaterThanOrEqualException(AbstractException):
    first_entity: str
    second_entity: str
    message: str = GREATER_OR_EQUAL_ERROR
