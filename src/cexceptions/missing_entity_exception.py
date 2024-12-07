from dataclasses import dataclass

from .abstract_exception import AbstractException
from .errors import MISSING_ENTITY_ERROR


@dataclass(kw_only=True)
class MissingEntityException(AbstractException):
    entity: str
    message: str = MISSING_ENTITY_ERROR
