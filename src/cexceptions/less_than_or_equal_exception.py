from dataclasses import dataclass

from cexceptions import AbstractException
from .errors import LESS_OR_EQUAL_ERROR


@dataclass(kw_only=True)
class LessThanOrEqualException(AbstractException):
    first_entity: str
    second_entity: str
    message: str = LESS_OR_EQUAL_ERROR
