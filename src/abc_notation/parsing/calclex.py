from ply.lex import lex, TOKEN

# import abc_notation.header as header
import abc_notation.symbols as symbols

import abc_notation.fields as abcf
# somehow removing it brakes the code (I have no idea why)
from abc_notation.fields.string_fields import string_field_dict
from abc_notation.fields.tempo import Tempo

from .token_names import tokens  # it's necessary, don't delete

from fractions import Fraction
import logging


t_ignore = "\t "
t_ignore_COMMENT = r"%[^\n]*\n"
t_ignore_line_skip = r"\\\n"
# t_ignore_TODO_FIELD = r"\[[A-LN-Za-z^M]:[^\n\]]*\]"

# t_TUPLET_SPECIFIER = r"\(\d+"


def t_REFERENCE_NUMBER(t):
    r"X:[^\S\r\n]*(?P<value>\d+)[^\S\r\n]*\n"
    t.value = t.lexer.lexmatch.group("value")
    return t


def t_TUNE_TITLE(t):
    r"T:[^\S\r\n]*(?P<title>[^\n]*)[^\S\r\n]*\n"
    t.value = t.lexer.lexmatch.group("title")
    return t


def t_DESCRIPTION_HEADER(t):
    r"(?P<field>[NORSZBFC]):[^\S\r\n]*(?P<text>[^\n]*)[^\S\r\n]*\n"

    field = t.lexer.lexmatch.group("field")
    text = t.lexer.lexmatch.group("text")

    t.value = abcf.string_fields.string_field_dict[field.strip()](text)

    return t


def t_KEY(t):
    r"K:[ \t]*(?P<name>[A-GH][#b]?)[ \t]*(?P<mode>\w*)[ \t]*\n"

    name = t.lexer.lexmatch.group("name")

    t.value = abcf.key.Key(
        name="B" if name == "H" else name,
        mode=abcf.key.Mode.parse(t.lexer.lexmatch.group("mode")),
    )
    return t


re_tempo = (
    r'((?P<text_only>"\w*")|'
    r'(("(?P<ltext>\w+)")?[^\S\r\n]*'
    r'(?P<fr1>\d+\/\d+)?[^\S\r\n]*(?P<fr2>\d+\/\d+)?'
    r'[^\S\r\n]*(?P<fr3>\d+\/\d+)?[^\S\r\n]*'
    r'((?P<fr4>\d+\/\d+)=)?(?P<bpm>\d+)[^\S\r\n]*'
    r'("(?P<rtext>\w+)")?))'
)
re_tempo_header = fr"Q:[^\S\r\n]*{re_tempo}[^\S\r\n]*\n"
# re_tempo_inline = fr"\[Q:({re_tempo})\]"
# re_tempo_field = r"\[Q:" + re_tempo + r"\]"
# re_tempo_field = re_tempo


@TOKEN(re_tempo_header)
def t_TEMPO(t):
    t.value = _make_tempo_from_t(t)
    return t


def _make_tempo_from_t(t) -> Tempo:
    text = t.lexer.lexmatch.group("text_only")
    if text is None:
        text = t.lexer.lexmatch.group("ltext")
    if text is None:
        text = t.lexer.lexmatch.group("rtext")
    if text is None:
        text = ""

    beats = [
        t.lexer.lexmatch.group("fr1"),
        t.lexer.lexmatch.group("fr2"),
        t.lexer.lexmatch.group("fr3"),
        t.lexer.lexmatch.group("fr4"),
    ]

    beats = [Fraction(b) for b in beats if b is not None]
    bpm = t.lexer.lexmatch.group("bpm")

    return Tempo(
        text=text,
        beats=beats,
        bpm=int(bpm) if bpm is not None else None
    )


def t_UNIT_NOTE_LENGTH(t):
    r"L:[^\S\r\n]*1[^\S\r\n]*/[^\S\r\n]*(?P<value>\d+)[^\S\r\n]*\n"
    t.value = abcf.unit_note_length.UnitNoteLength(
        int(t.lexer.lexmatch.group("value")))
    return t


meter = (
    r"([^\S\r\n]*(?P<other>(none)|(C\|?))|([^\S\r\n]*\(?[^\S\r\n]*"
    r"(?P<top>\d+([^\S\r\n]*\+[^\S\r\n]*\d+)*)"
    r"[^\S\r\n]*\)?[^\S\r\n]*\/[^\S\r\n]*(?P<bottom>\d+))[^\S\r\n]*)"
)


meter_header = r"M:" + meter + r"\n"
meter_field = r"\[M:" + meter + r"\]"


@TOKEN(meter_header)
def t_METER(t):

    top = t.lexer.lexmatch.group("top")
    bottom = t.lexer.lexmatch.group("bottom")

    if other := t.lexer.lexmatch.group("other"):
        match other.strip():
            case "none": t.value = abcf.meter.FreeMeter()
            case "C": t.value = abcf.meter.SimpleMeter(4, 4)
            case "C|": t.value = abcf.meter.SimpleMeter(2, 2)
        return t

    # if bottom is None:
    #     t.value = abcf.meter.FreeMeter()
    #     return t

    int_bottom = int(bottom)

    try:
        int_top = int(top)
    except ValueError:
        top_list = top.split("+")
    else:
        t.value = abcf.meter.SimpleMeter(int_top, int_bottom)
        return t

    t.value = abcf.meter.ComplexMeter(
        top=[int(x) for x in top_list],
        bottom=bottom,
    )
    return t


# todo remove disallowed spaces from notes
wl = r"[^\S\r\n]*"
octave = r"(?P<oct>[,']*)"
duration = r"(?P<top>\d*)(?P<slash>\/*)(?P<bottom>\d*)"
accidental = r"(?P<acc>=|(\^{1,2})|(\_{1,2})){0,1}"
pitch = r"(?P<pit>[a-gA-G])"
tie = r"(?P<tied>-?)"
note = accidental + pitch + octave + duration + tie
rest = r"[zx]" + duration + tie


@TOKEN(rest)
def t_REST(t):
    top = t.lexer.lexmatch.group("top")
    bottom = t.lexer.lexmatch.group("bottom")
    slashes = t.lexer.lexmatch.group("slash")
    tie = t.lexer.lexmatch.group("tied")

    if len(bottom) > 0 and len(slashes) != 1:
        raise SyntaxError("invalid state of rest's duration")
    elif len(top) == 0 and len(bottom) == 0:
        top = 1
        bottom = 2 ** len(slashes)

    top = 1 if top == "" else int(top)
    bottom = 1 if bottom == "" else int(bottom)

    t.value = symbols.Rest(
        duration=Fraction(top, bottom),
        tied=tie == "-",
    )
    return t


def t_MULTIMEASURE_REST(t):
    r"Z[^\S\r\n]*(?P<dur>\d*)"

    dur = t.lexer.lexmatch.group("dur")
    dur = Fraction(1) if dur == "" else Fraction(dur)
    t.value = symbols.MultimeasureRest(
        number_of_measures=dur,
    )
    return t


def t_NEW_LINE(t):
    r"\n"
    t.value = symbols.NewLine()
    return t


def t_CHORD_NAME(t):
    r'"(?P<name>\S+)"'
    t.value = symbols.ChordName(t.lexer.lexmatch.group("name"))
    return t


@TOKEN(note)
def t_NOTE(t):
    top = t.lexer.lexmatch.group("top")
    bottom = t.lexer.lexmatch.group("bottom")
    acc = t.lexer.lexmatch.group("acc")
    oct = t.lexer.lexmatch.group("oct")
    slashes = t.lexer.lexmatch.group("slash")
    tie = t.lexer.lexmatch.group("tied")

    octave = sum(1 if s == "'" else -1 for s in oct)

    if len(bottom) > 0 and len(slashes) != 1:
        raise SyntaxError("invalid state of note's duration")
    elif len(top) == 0 and len(bottom) == 0:
        top = 1
        bottom = 2 ** len(slashes)

    top = 1 if top == "" else int(top)
    bottom = 1 if bottom == "" else int(bottom)

    t.value = symbols.Note(
        pitch=t.lexer.lexmatch.group("pit"),
        octave=octave,
        duration=Fraction(top, bottom),
        accidental=symbols.Accidental.from_str("" if acc is None else acc),
        tied=tie == "-",
    )
    return t


def t_BROKEN_RHYTHM(t):
    r"[<>]"

    if t.value == ">":
        t.value = symbols.BrokenRhythmRight()
    else:
        t.value = symbols.BrokenRhythmLeft()

    return t


@TOKEN(meter_field)
def t_METER_CHANGE_FIELD(t):
    top = t.lexer.lexmatch.group("top")
    bottom = t.lexer.lexmatch.group("bottom")

    if bottom is None:
        t.value = abcf.meter.FreeMeter(inline=True)
        return t
    else:
        int_bottom = int(bottom)

    try:
        int_top = int(top)
    except ValueError:
        top_list = top.split("+")
    else:
        t.value = abcf.meter.SimpleMeter(int_top, int_bottom, inline=True)
        return t

    t.value = abcf.meter.ComplexMeter(
        top=[int(x) for x in top_list],
        bottom=bottom,
        inline=True,
    )
    return t


def t_INLINE_STRING_FIELD(t):
    r"\[(?P<code>[I]):(?P<text>[^\n\]]*)\]"

    code = t.lexer.lexmatch.group("code")
    text = t.lexer.lexmatch.group("text")

    match code:
        case "I": t.value = abcf.string_fields.Instruction(text, inline=True)

    return t


re_tempo_inline = "asdlkfjalwkejflakwjeflakjwflakjf"


@TOKEN(re_tempo_inline)
def t_TEMPO_INLINE(t):
    t.value = _make_tempo_from_t(t)
    return t


def t_TUPLET_SPECIFIER(t):
    r"\((?P<p>\d+)(:(?P<q>\d*)(:(?P<r>\d*))?)?"

    p = int(t.lexer.lexmatch.group("p"))

    q = t.lexer.lexmatch.group("q")
    r = t.lexer.lexmatch.group("r")

    if not q and not r:
        t.value = symbols.TupletSpecifier(p)
    else:
        r = int(r) if r else p
        if q != "":
            q = int(q)
        else:
            # TODO: https://abcnotation.com/wiki/abc:standard:v2.1#duplets_triplets_quadruplets_etc
            q = 3 - (p % 2)
        t.value = symbols.TupletSpecifierComplex(p, q, r)

    return t


def t_BEGIN_SLUR(t):
    r"\("
    t.value = symbols.BeginSlur()
    return t


def t_END_SLUR(t):
    r"\)"
    t.value = symbols.EndSlur()
    return t


def t_BAR_LINE(t):
    r"(?P<line>\|\]|\|\||\[\||::|:?\|:?)(?P<rep>\d*)"

    line = t.lexer.lexmatch.group("line")
    rep = t.lexer.lexmatch.group("rep")

    rep = int(rep) if len(rep.strip()) > 0 else None

    t.value = symbols.BarLine(line, repeat=rep)
    return t


def t_DECORATION(t):
    r"!(?P<decoration>\S+)!"
    dec = t.lexer.lexmatch.group("decoration")
    t.value = symbols.Decoration(dec)
    return t


def t_SHORTHAND_DECORATION(t):
    r"[.~HLMOPSTuv]"
    t.value = symbols.ShorthandDecoration(t.value)
    return t


def t_error(t):
    if t.lexer.disallow_illegal_characters:
        raise ValueError(f"Illegal character {t.value[0]!r}")
    logging.warning(f"Illegal character {t.value[0]!r}")
    t.lexer.illegal_character = True
    logging.info("LEXMATCH", t.lexer.lexpos)
    p = t.lexer.lexpos
    d = t.lexer.lexdata
    logging.info(d[p - 10: p + 10])

    t.lexer.skip(1)


lexer = lex()
lexer.illegal_character = False
lexer.disallow_illegal_characters = False
