from dataclasses import dataclass

from cexceptions import AbstractException
from cexceptions.errors import INVALID_CREDENTIALS_ERROR


@dataclass(kw_only=True)
class CredentialValidationException(AbstractException):
    entity: str
    message: str = INVALID_CREDENTIALS_ERROR
