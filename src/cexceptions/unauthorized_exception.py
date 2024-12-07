from dataclasses import dataclass

from .abstract_exception import AbstractException
from .errors import UNAUTHORIZED_ERROR


@dataclass(kw_only=True)
class UnauthorizedException(AbstractException):
    message: str = UNAUTHORIZED_ERROR
