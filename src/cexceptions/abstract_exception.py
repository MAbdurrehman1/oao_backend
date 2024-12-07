from abc import ABCMeta
from dataclasses import dataclass, replace
from typing_extensions import Self


@dataclass(kw_only=True)
class AbstractException(Exception, metaclass=ABCMeta):
    message: str

    @property
    def full_message(self):
        return self.message.format(**self.__dict__)

    def __str__(self):
        return self.full_message

    def replace(self, **changes) -> Self:
        return replace(self, **changes)
