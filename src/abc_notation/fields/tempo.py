from __future__ import annotations
from .abstract_fields import InlinableField
import dataclasses as dc
from typing import Optional, ClassVar


@dc.dataclass(slots=True)
class Tempo(InlinableField):
    text: str = ""
    beats: list[Beat] = dc.field(default_factory=list)
    bpm: Optional[int] = None
    inline: bool = False

    LETTER_NAME: ClassVar[str] = "Q"

    def _header_str(self) -> str:
        parts = []
        if len(self.text):
            parts.append(f'"{self.text}"')

        if self.bpm:
            beats_str = [str(f) for f in self.beats]
            beats_str = " ".join(beats_str)

            eq = "=" if len(beats_str) else ""

            parts.append(f"{beats_str}{eq}{self.bpm}")

        return " ".join(parts)


@dc.dataclass(slots=True)
class Beat:
    top: int
    bottom: int

    def __str__(self) -> str:
        return f"{self.top}/{self.bottom}"
