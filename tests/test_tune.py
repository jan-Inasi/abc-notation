from abc_notation.parsing.parsing import ParserABC
from fractions import Fraction

data = """X:0
T: Bohnenlied
M: 4/4
L: 1/8
K: F
c2d2d2 | G2c2A3F | G2G2F4 | z2
"""

class TestTune:

    def test_duration(self):
        parser = ParserABC()
        tune = parser.parse_tune(data)
        assert tune.duration_in_units() == Fraction(6 + 8 + 8 + 2)
