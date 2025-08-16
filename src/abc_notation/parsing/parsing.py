from abc_notation.parsing.parser import parser
from abc_notation.parsing.calclex import lexer
from abc_notation.tune import Tune
from typing import Iterable
from pathlib import Path
import logging
from typing import Optional


class ParserABC:

    def __init__(
        self,
        allow_illegal_chars=False,
        skip_tunes_with_error=True,
        recursive_search=True,
        sorted_search=False,
        skip_allowence=0,
    ):
        self.allow_illegal_chars = allow_illegal_chars
        self.skip_tunes_with_error = skip_tunes_with_error
        self.recursive_search = recursive_search
        self.sorted_search = sorted_search
        self.skip_allowence = skip_allowence

        self._current_file_path: Optional[Path] = None
        self._current_tune_block: Optional[str] = None

    def parse_tune(self, text: str) -> Tune:
        lex = lexer.clone()
        # par = parser.clone()
        lex.disallow_illegal_characters = True
        # par.disallow_illegal_characters = True
        parser.disallow_illegal_characters = True
        try:
            tune = parser.parse(text, lexer=lex)
        except ValueError as ex:
            raise ValueError(
                f"{ex}\nfile at: {self._current_file_path}\n{text}")
        if not self.allow_illegal_chars and lex.illegal_character:
            raise SyntaxError(f"{self._current_file_path}\n{text}")
        return tune

    def parse_abcfile(self, text: str) -> Iterable[Tune]:
        for tune_block in text.split("\n\n"):
            tune_block = tune_block.strip()
            if tune_block == "":
                continue

            yield "tune"

            if self.skip_allowence > 0 or self.skip_tunes_with_error:
                self.skip_allowence = max(self.skip_allowence - 1, 0)
                try:
                    yield self.parse_tune(tune_block)
                except ValueError:
                    logging.warning("tune skipped (ValueError)")
                except SyntaxError:
                    logging.warning("tune skipped (illegal character)")
            else:
                yield self.parse_tune(tune_block)

    def parse_dataset(self, path: str | Path) -> Iterable[Tune]:

        path = Path(path)
        file_names = path.rglob(
            "*.abc") if self.recursive_search else path.glob("*.abc")
        file_names = sorted(file_names) if self.sorted_search else file_names

        for file_name in file_names:
            self._current_file_path = file_name
            with open(file_name, "r") as file:
                abcfile = file.read()
                try:
                    yield from self.parse_abcfile(abcfile)
                except Exception as ex:
                    raise ex
            self._current_file_path = None
