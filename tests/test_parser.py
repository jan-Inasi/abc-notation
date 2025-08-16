from fractions import Fraction

import abc_notation.fields as abcf
import abc_notation.symbols as symbols
from abc_notation.parsing.parsing import ParserABC
from abc_notation.symbols import Accidental, Note

data = """ X:314
T: Bohnenlied
M: 4/4
L: 1/8
N: A0362
O: Europa, Mitteleuropa, Deutschland
N: Pet. Schoeffer II. 1537 No. 6., hier giebt Boehme die vereinfachte
N: Form nach Werlin 1646 S. 3135.
R: Romanze, Ballade, Lied
K: F
c2d2d2 | G2c2A3F | G2G2F4 | z2
% comment
c2c2c2 | d3c=B2c2 | =B4c4 | z2
c2d2d2 | G2c2A3F | G2G2F4 | z2
c2c2c2 | d3c=B2c2 | =B4c4 | z2
c2d2e2 | f4z2e2 | d2^c2d4 | z2
f2d2e2 | f3ed2c2 | B4A4 | z2
c2d2=B2 | c4z2A2 | B2G2A4 | z2
F2c2A2 | F2A2G4 | F8 | z2
"""


class TestParser:
    def test_parse(self):
        parser = ParserABC()
        tune = parser.parse_tune(data)

        assert tune.head.title == "Bohnenlied"
        assert tune.head.meter == abcf.meter.SimpleMeter(4, 4)
        assert len(tune.head.other["N"]) == 3
        assert tune.head.other["R"][0] == abcf.string_fields.Rhythm(
            "Romanze, Ballade, Lied"
        )
        assert tune.head.key == abcf.key.Key("F")

        b = tune.body
        assert b[0] == Note("c", 2)
        assert b[1] == Note("d", 2)
        assert b[2] == Note("d", 2)
        assert b[3] == symbols.BarLine("|")
        assert b[13] == symbols.Rest(2)

    def test_fraction_durations(self):
        data = """X:314
T: Bohnenlied
K: F
c1/2d//  e/5 _G3/4
"""
        parser = ParserABC()
        tune = parser.parse_tune(data)
        notes = tune.body
        assert notes[0] == Note("c", Fraction(1, 2))
        assert notes[1] == Note("d", Fraction(1, 4))
        assert notes[2] == Note("e", Fraction(1, 5))
        assert notes[3] == Note("G", Fraction(3, 4), Accidental.FLAT)

    def test_tuplet_specifier(self):
        data = """X:314
T: Bohnenlied
K: F
(3 a b c (4:2:3 (3:2 (8::
"""
        parser = ParserABC()
        tune = parser.parse_tune(data)
        notes = tune.body
        assert notes[0] == symbols.TupletSpecifier(3)
        assert notes[4] == symbols.TupletSpecifierComplex(4, 2, 3)
        assert notes[5] == symbols.TupletSpecifierComplex(3, 2, 3)
        assert notes[6] == symbols.TupletSpecifier(8)

    def test_measure_repetitions(self):
        data = """ X: 1
T: Lord Leitrim
R: barndance
M: 4/4
L: 1/8
K: Cmaj
CDEF G2 FD|G2 FE FDDF|G,DFA G2 FD|1 G2 FD ECA,G,:|2 G2 FD EC C2||
cdcB G3 F|E2 GE FD D2|cdcB G3 F|D2 FD EC C2|
cdcB G3 F|E2 GE FD D2|ecdB c2 cA|GAGF DEFD||
"""

        parser = ParserABC()
        tune = parser.parse_tune(data)
        bars = tune.body.bars()
        assert next(bars)[-1] == symbols.BarLine("|")
        assert next(bars)[-1] == symbols.BarLine("|")
        assert next(bars)[-1] == symbols.BarLine("|", repeat=1)
        assert next(bars)[-1] == symbols.BarLine(":|", repeat=2)
        assert next(bars)[-1] == symbols.BarLine("||")

    def test_slurs(self):
        data = """X: 373
T: Lord Kelly's Reel
R: reel
M: C
L: 1/8
Z: 2012 John Chambers <jc:trillian.mit.edu>
B: J. Anderson "Budget of Strathspeys, Reels and Country Dances" (Early 1800s) p.37 #3
F: http://imslp.org/wiki/Anderson%27s_Budget_of_Strathspeys,_Reels_and_Country_Dances_(Various)
K: Am
c | EAcA eAcA | DGBg G>A c/B/A/^G/ | EAAc Bdce  | d>g (e/d/c/B/) cAA :|
(a/b/) | c'aea Aeac' | bgdg Gdgb | c'aea  gedc  | B>g  e/d/c/B/  cAA ||
(a/b/) | c'aea Aeac' | bgdg Gdgb | c'ab^g ae=gd | Bg  (e/d/c/B/) cAA |]"""
        parser = ParserABC()
        tune = parser.parse_tune(data)

    def test_tempo(self):
        data = """X:1
T: Lord John Campbell
C:
R:Strathspey
Q: 128
M:4/4
L:1/16
K:D
|:A,2|DDD2 F3D C2E2 E3F|DDD2 F3D A2D2 F2D2|G2BG F2AF GFED C3E|DDD2 f3e d2D2 D2:|"""

        parser = ParserABC()
        tune = parser.parse_tune(data)

    def test_empty_body(self):
        data = """X:1
T:Lord Loudon’s March [2]
M:C
L:1/8
R:March
C: Georg Fredric Handel
B:  https://digital.nls.uk/special-collections-of-printed-music/archive/87709669
B: Neil Stewart – Select Collection of Scots, English, Irish and Foreign Airs, Jiggs &
B:Marches, vol. 1 (Edinburgh, 1784, No. 116, p. 56)
Z:AK/Fiddler’s Companion
K:G"""

    parser = ParserABC()
    tune = parser.parse_tune(data)
