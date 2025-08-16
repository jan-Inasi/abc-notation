from abc_notation.fields.abstract_fields import Meter
import dataclasses as dc


@dc.dataclass(slots=True)
class FreeMeter(Meter):
    """Class representing a free meter.
    In free meter, bar lines can be placed anywhere you want."""
    inline: bool = dc.field(default=False, kw_only=True)

    def _header_str(self) -> str:
        return "none"

    def duration_component(self) -> int:
        return 0


@dc.dataclass(slots=True)
class SimpleMeter(Meter):
    top: int = 4
    bottom: int = 4
    inline: bool = dc.field(default=False, kw_only=True)

    def _header_str(self) -> str:
        return f"{self.top}/{self.bottom}"

    def duration_component(self) -> int:
        return self.top * self.bottom


@dc.dataclass(slots=True)
class ComplexMeter(Meter):
    top: list[int]
    bottom: int
    inline: bool = dc.field(default=False, kw_only=True)


    def _header_str(self) -> str:
        top = " + ".join(self.top)
        return f"{top}/{self.bottom}"

    def duration_component(self) -> int:
        return sum(self.top) * self.bottom

