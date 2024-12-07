from dataclasses import dataclass

from .abstract_exception import AbstractException
from .errors import UNIQUE_PER_ENTITY_ARGUMENT_ERROR


@dataclass(kw_only=True)
class UniquePerEntityException(AbstractException):
    first_entity: str
    second_entity: str
    message: str = UNIQUE_PER_ENTITY_ARGUMENT_ERROR
