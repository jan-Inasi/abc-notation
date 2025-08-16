from abc import ABC, abstractmethod, abstractproperty
import dataclasses as dc


class Field(ABC):
    @abstractproperty
    def LETTER_NAME(cls) -> str:
        ...

    @abstractmethod
    def _header_str(self) -> str:
        ...

    def __str__(self) -> str:
        return f"{self.LETTER_NAME}: {self._header_str()}\n"


@dc.dataclass
class StringField(Field):
    text: str

    def _header_str(self) -> str:
        return self.text


class InlinableField(Field):

    @abstractproperty
    def inline(self) -> str:
        ...

    def __str__(self) -> str:
        if self.inline:
            return f"[{self.LETTER_NAME}:{self._header_str()}]"
        else:
            return super().__str__()


class Meter(InlinableField):
    LETTER_NAME = "M"

    @abstractmethod
    def duration_component(self) -> int: ...
