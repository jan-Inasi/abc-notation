from pathlib import Path

from tqdm import tqdm

from abc_notation.parsing.parsing import ParserABC


def main():
    root = Path(__file__).parent.parent
    print(root)

    parser = ParserABC(
        allow_illegal_chars=False,
        skip_tunes_with_error=False,
        recursive_search=True,
        sorted_search=False,
        skip_allowence=0,
    )

    tunes: list[int] = []
    for i, tune in tqdm(
        enumerate(
            parser.parse_dataset(
                root / "data/raw_abcnotation",
            )
        )
    ):
        tunes.append(tune)


if __name__ == "__main__":
    main()
