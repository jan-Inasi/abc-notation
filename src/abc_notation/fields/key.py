from __future__ import annotations
from abc_notation.fields.abstract_fields import InlinableField
import dataclasses as dc
from enum import Enum
from typing import ClassVar


class Mode(Enum):
    MAJOR = ""
    MINOR = "m"
    MIXOLYDIAN = "Mix"
    DORIAN = "Dor"
    PHRYGIAN = "Phr"
    LYDIAN = "Lyd"
    LOCRIAN = "Loc"

    @classmethod
    def parse(cls, text: str) -> Mode:
        text = text.strip().lower()
        if text == "" or text[:3] == "maj":
            return Mode.MAJOR
        elif text == "m" or text[:3] == "min":
            return Mode.MINOR
        elif text[:3] == "mix":
            return Mode.MIXOLYDIAN
        elif text[:3] == "dor":
            return Mode.DORIAN
        elif text[:3] == "phr":
            return Mode.PHRYGIAN
        elif text[:3] == "lyd":
            return Mode.LYDIAN
        elif text[:3] == "loc":
            return Mode.LOCRIAN
        else:
            raise ValueError(f"couldn't parse '{text}' to a mode")


@dc.dataclass(slots=True)
class Key(InlinableField):
    name: str = "C"
    mode: Mode = Mode.MAJOR
    inline: bool = dc.field(default=False, kw_only=True)

    LETTER_NAME: ClassVar[str] = "K"

    def _header_str(self) -> str:
        return f"{self.name}{self.mode.value}"
