from __future__ import annotations
import dataclasses as dc
from enum import Enum
from abc import ABC, abstractmethod
from fractions import Fraction
from typing import Optional


class Symbol(ABC):
    pass

    @abstractmethod
    def _get_duration(
        self, measure_dur: Fraction = Fraction(4)) -> Fraction: ...


class SymbolDurationZero(ABC):

    def _get_duration(self, _=None) -> Fraction:
        return Fraction(0)


# conversion beween decoration and decoration shortand
@dc.dataclass(slots=True)
class ShorthandDecoration(SymbolDurationZero):
    name: str

    def __str__(self) -> str:
        return f"{self.name}"


@dc.dataclass(slots=True)
class Decoration(SymbolDurationZero):
    name: str

    def __str__(self) -> str:
        return f"!{self.name}!"


class NewLine(SymbolDurationZero):

    def __str__(self) -> str:
        return "\n"


class BeginSlur(SymbolDurationZero):

    def __str__(self) -> str:
        return "("


class EndSlur(SymbolDurationZero):

    def __str__(self) -> str:
        return ")"


@dc.dataclass(slots=True)
class ChordName(SymbolDurationZero):
    name: str

    def __str__(self) -> str:
        return f'"{self.name}"'


@dc.dataclass(slots=True)
class BarLine(SymbolDurationZero):
    bar_type: str
    repeat: Optional[int] = None

    def __str__(self) -> str:
        if self.repeat is None:
            return self.bar_type
        else:
            return f"{self.bar_type}{self.repeat}"


@dc.dataclass(slots=True)
class TupletSpecifier(SymbolDurationZero):
    p: int

    def __str__(self) -> str:
        return f"({self.p}"


@dc.dataclass(slots=True)
class TupletSpecifierComplex(TupletSpecifier):
    q: int
    r: int

    def __str__(self) -> str:
        return f"({self.p}:{self.q}:{self.r}"


class Tie(SymbolDurationZero):

    def __str__(self) -> str:
        return "-"


class BrokenRhythm(SymbolDurationZero):
    pass


class BrokenRhythmLeft(BrokenRhythm):

    def __str__(self) -> str:
        return "<"


class BrokenRhythmRight(BrokenRhythm):
    def __str__(self) -> str:
        return ">"


class Accidental(Enum):
    NONE = ""
    SHARP = "^"
    DOUBLE_SHARP = "^^"
    FLAT = "_"
    DOUBLE_FLAT = "__"
    NATURAL = "="

    @classmethod
    def from_str(cls, symbol: str) -> Accidental:
        if symbol == "":
            return Accidental.NONE
        elif symbol == "^":
            return Accidental.SHARP
        elif symbol == "^^":
            return Accidental.DOUBLE_SHARP
        elif symbol == "_":
            return Accidental.FLAT
        elif symbol == "__":
            return Accidental.DOUBLE_FLAT
        elif symbol == "=":
            return Accidental.NATURAL
        else:
            raise ValueError(
                "The Accidental class accepts only the following symbols: "
                "{'', '^', '^^', '_', '__', '='}.\n"
                f"The '{symbol}' is not one of them."
            )


@dc.dataclass(slots=True)
class Note(Symbol):
    """Note class"""

    pitch: str
    duration: Fraction = Fraction(1)
    accidental: Accidental = Accidental.NONE
    octave: int = 0
    tied: bool = False

    def __str__(self) -> str:
        dur = "" if self.duration == 1 else str(self.duration)
        tie = "-" if self.tied else ""
        return f"{self.accidental.value}{self.pitch}{dur}{tie}"

    def _get_duration(self, _=None) -> Fraction:
        return self.duration


@dc.dataclass(slots=True)
class Rest(Symbol):
    duration: Fraction = Fraction(1)
    tied: bool = False

    def __str__(self) -> str:
        dur = "" if self.duration == Fraction(1) else str(self.duration)
        tie = "-" if self.tied else ""
        return f"z{dur}{tie}"

    def _get_duration(self, _=None) -> Fraction:
        return self.duration


@dc.dataclass(slots=True)
class MultimeasureRest(Symbol):
    number_of_measures: int = 1

    def _get_duration(self, measure_dur: Fraction = Fraction(4)) -> Fraction:
        return self.number_of_measures * measure_dur
