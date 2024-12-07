from dataclasses import dataclass

from .abstract_exception import AbstractException
from .errors import ALREADY_BELONG_ERROR


@dataclass(kw_only=True)
class AlreadyBelongException(AbstractException):
    owner_entity: str
    owned_entity: str
    arg: str
    values: str
    message: str = ALREADY_BELONG_ERROR
