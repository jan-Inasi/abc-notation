from abc_notation.parsing.parsing import ParserABC

parser = ParserABC()

data = """X:314
T: Bohnenlied
K: F
c1/2d//  e/5 _G3/4
"""

tune = parser.parse_tune(data)
print(tune)
