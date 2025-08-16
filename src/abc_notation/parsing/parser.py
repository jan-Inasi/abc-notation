import logging

from ply.yacc import yacc

from abc_notation.body import Body
from abc_notation.parsing.token_names import tokens  # it's necessary, don't delete
from abc_notation.tune import Head, Tune

# HEAD


def p_expresion(p):
    "expresion : REFERENCE_NUMBER TUNE_TITLE header_list KEY body"
    head = Head(
        title=p[2],
        reference_number=p[1],
        key=p[4],
        **p[3],
    )
    p[0] = Tune(head=head, body=p[5])


def p_header_list(p):
    "header_list :"
    p[0] = dict()


def p_header_list_meter(p):
    "header_list : header_list METER"
    p[1]["meter"] = p[2]
    p[0] = p[1]


def p_header_list_unit_note_length(p):
    "header_list : header_list UNIT_NOTE_LENGTH"
    p[1]["unit_note_length"] = p[2]
    p[0] = p[1]


def p_header_list_description(p):
    """header_list : header_list DESCRIPTION_HEADER
    | header_list TEMPO"""
    other: dict[str, str] = p[1].get("other", {})
    string_field = p[2]
    other.setdefault(string_field.LETTER_NAME, []).append(string_field)
    p[1]["other"] = other
    p[0] = p[1]


# BODY


def p_body_empty(p):
    "body :"
    p[0] = Body()


def p_body_symbol(p):
    """body : body NOTE
    | body REST
    | body MULTIMEASURE_REST
    | body NEW_LINE
    | body METER_CHANGE_FIELD
    | body BROKEN_RHYTHM
    | body TUPLET_SPECIFIER
    | body BAR_LINE
    | body CHORD_NAME
    | body SHORTHAND_DECORATION
    | body DECORATION
    | body TEMPO_INLINE
    | body INLINE_STRING_FIELD"""
    p[1].append(p[2])
    p[0] = p[1]


def p_body_slur_body(p):
    """body : body BEGIN_SLUR slur END_SLUR body"""
    p[1].append(p[2])
    p[1].extend(p[3])
    p[1].append(p[4])
    p[1].extend(p[5])
    p[0] = p[1]


def p_slur_symbol(p):
    """slur : slur NOTE
    | slur BROKEN_RHYTHM
    | slur BAR_LINE"""
    p[1].append(p[2])
    p[0] = p[1]


def p_slur_empty(p):
    """slur :"""
    p[0] = Body()


def p_error(p):
    raise SyntaxError(f"parsing error: {p}")
    # logging.warning(f"parser error: {p}")


parser = yacc()
