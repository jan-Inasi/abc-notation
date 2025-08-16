import pathlib as pl
import itertools as it

from abc_notation.parsing.parser import parse_tune

data = """"""

if __name__ == "__main__":
    path = pl.Path(__file__).parent.parent / "data/esac"

    for i, file_name in it.islice(enumerate(path.glob("*.abc")), 0, None):
        with open(file_name, "r") as file:
            str_tunes = file.read().split("\n\n")

        for j, str_tune in enumerate(str_tunes):

            if (i, j) in {
                (14, 20),
                (22, 106),
                (35, 373),
                (35, 444),
                (36, 12),
                (37, 26),
            }:
                continue
            if str_tune.strip() == "":
                continue
            print(i, j, file_name)

            try:
                tune = parse_tune(str_tune.strip(), allow_illegal_chars=False)
                if tune is None:
                    print(str_tune)
                    print("tune is none")
                    exit()
            except SyntaxError as ex:
                print(str_tune)
                print("#" * 20)
                print(ex)
                exit()

            tune.body
            print(repr(tune))
            exit()

        # if tune is None:
        #     print("tune is none")
        #     print(str_tune)
        # break

        # if j == 0:
        #     print(str_tune)
        #
        #     print("\n\ntune:")
        #     print(tune)
        #     break

        # # break
        # if i == 13:
        #     break
