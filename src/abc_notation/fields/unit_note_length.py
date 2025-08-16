from abc_notation.fields.abstract_fields import InlinableField
import dataclasses as dc
from typing import ClassVar


@dc.dataclass(slots=True)
class UnitNoteLength(InlinableField):
    value: int = 8
    inline: bool = dc.field(default=False, kw_only=True)

    LETTER_NAME: ClassVar[str] = "L"

    def _header_str(self) -> str:
        return f"1/{self.value}"
