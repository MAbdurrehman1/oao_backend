from dataclasses import dataclass

from cexceptions import AbstractException
from cexceptions.errors import ENTITY_PROCESS_ERROR


@dataclass(kw_only=True)
class EntityProcessException(AbstractException):
    entity: str
    message: str = ENTITY_PROCESS_ERROR
