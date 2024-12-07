from dataclasses import dataclass

from .abstract_exception import AbstractException
from .errors import NOT_FOUND_ENTITY_ERROR


@dataclass(kw_only=True)
class NotFoundException(AbstractException):
    entity: str
    arg: str
    value: str
    message: str = NOT_FOUND_ENTITY_ERROR
