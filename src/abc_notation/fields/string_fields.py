from abc_notation.fields.abstract_fields import StringField, InlinableField
import dataclasses as dc
import inspect
import sys


class Notes(StringField):
    LETTER_NAME = "N"


class Origin(StringField):
    LETTER_NAME = "O"


class Rhythm(StringField):
    LETTER_NAME = "R"


class Source(StringField):
    LETTER_NAME = "S"


class FileURL(StringField):
    LETTER_NAME = "F"


class TranscriptionField(StringField):
    LETTER_NAME = "Z"


class BookField(StringField):
    LETTER_NAME = "B"


class ComposerField(StringField):
    LETTER_NAME = "C"


@dc.dataclass(slots=True)
class Instruction(StringField, InlinableField):
    inline: bool = dc.field(default=False, kw_only=True)
    LETTER_NAME = "I"


# collecting every class defined in this file into a dictionary
# {class.LETTER_NAME: class}
string_field_dict = {
    obj.LETTER_NAME: obj
    for name, obj in vars(sys.modules[__name__]).items()
    if inspect.isclass(obj) and obj not in [StringField, InlinableField]
}
