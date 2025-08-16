from __future__ import annotations
import dataclasses as dc

from .fields.abstract_fields import Meter
from .fields.meter import FreeMeter
from .fields.unit_note_length import UnitNoteLength
from .fields.key import Key
from .body import Body
import io
from fractions import Fraction


@dc.dataclass(slots=True)
class Tune:
    head: Head
    body: Body

    def __str__(self) -> str:
        return f"{self.head}{self.body}"

    def duration_in_units(self) -> Fraction:
        measure_duration = Fraction(
            self.head.meter.duration_component(),
            self.head.unit_note_length.value,
        )
        return sum(s._get_duration(measure_duration) for s in self.body)

    def duration_in_sec(self, bpm: float) -> float:
        units = self.duration_in_units()


@dc.dataclass(slots=True)
class Head:
    title: str = ""
    meter: Meter = dc.field(default_factory=FreeMeter)
    unit_note_length: UnitNoteLength = dc.field(default_factory=UnitNoteLength)
    key: Key = dc.field(default_factory=Key)
    reference_number: int = 0
    other: dict[str, list[str]] = dc.field(default_factory=dict)

    def __str__(self) -> str:
        buffer = io.StringIO()
        buffer.write(f"X: {self.reference_number}\n")
        buffer.write(f"T: {self.title}\n")
        for key, values in self.other.items():
            for v in values:
                buffer.write(f"{v}")
        buffer.write(f"{self.unit_note_length}")
        buffer.write(f"{self.meter}")
        buffer.write(f"{self.key}")

        return buffer.getvalue()
