from dataclasses import dataclass

from .abstract_exception import AbstractException
from .errors import EXPIRE_ERROR


@dataclass(kw_only=True)
class ExpireException(AbstractException):
    entity: str
    message: str = EXPIRE_ERROR
