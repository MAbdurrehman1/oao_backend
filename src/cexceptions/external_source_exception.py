from dataclasses import dataclass

from cexceptions import AbstractException
from cexceptions.errors import EXTERNAL_SOURCE_ERROR


@dataclass(kw_only=True)
class ExternalSourceException(AbstractException):
    source: str
    source_error: str
    message: str = EXTERNAL_SOURCE_ERROR
