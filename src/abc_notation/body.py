from __future__ import annotations
from collections import UserList
import abc_notation.symbols as sb
from typing import Iterable, overload


class Body(UserList):

    def __init__(self, *symbols: sb.Symbol):
        super().__init__(symbols)

    def __str__(self) -> str:
        return "".join((str(s) for s in self))

    def extend_with_bars(self, *bars: Body) -> Body:
        for bar in bars:
            self.extend(bar)
        return self

    def bars(self) -> Iterable[Body]:
        bar = Body()
        for i, s in enumerate(self):
            bar.append(s)
            if i > 0 and isinstance(s, sb.BarLine):
                yield bar
                bar = Body()

        if len(bar):
            yield bar

    @overload
    def __getitem__(self, idx: int) -> sb.Symbol:
        return self[idx]

    @overload
    def __getitem__(self, slice: slice) -> Body:
        return self[slice]

    def __getitem__(self, idx: int | slice) -> sb.Symbol | Body:
        if isinstance(idx, slice):
            return Body(*super().__getitem__(idx)[0])
        else:
            return super().__getitem__(idx)


if __name__ == "__main__":
    body = Body()
    b1 = body[0]
