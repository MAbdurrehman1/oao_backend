from dataclasses import dataclass

from cexceptions import AbstractException
from cexceptions.errors import DOES_NOT_BELONG_ERROR


@dataclass(kw_only=True)
class DoesNotBelongException(AbstractException):
    first_entity: str
    first_value: str
    second_entity: str
    second_value: str
    message: str = DOES_NOT_BELONG_ERROR
