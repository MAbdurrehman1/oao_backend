from dataclasses import dataclass

from cexceptions import AbstractException
from cexceptions.errors import EMPTY_RESULT_ERROR


@dataclass(kw_only=True)
class EmptyResultException(AbstractException):
    first_entity: str
    second_entity: str
    message: str = EMPTY_RESULT_ERROR
