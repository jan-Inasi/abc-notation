from abc_notation.body import Body
import abc_notation.symbols as sb
import pytest


class TestBody:

    def test_single_bar_iteration(self):
        bars = Body(sb.Note("a"), sb.Rest(1)).bars()
        assert next(bars) == Body(sb.Note("a"), sb.Rest(1))
        with pytest.raises(StopIteration):
            next(bars)

        bars = Body(sb.Note("a"), sb.Rest(1), sb.BarLine("|")).bars()
        assert next(bars) == Body(sb.Note("a"), sb.Rest(1), sb.BarLine("|"))
        with pytest.raises(StopIteration):
            next(bars)

        bars = Body(sb.BarLine("|"), sb.Note("a"), sb.Rest(1)).bars()
        assert next(bars) == Body(sb.BarLine("|"), sb.Note("a"), sb.Rest(1))
        with pytest.raises(StopIteration):
            next(bars)

        bars = Body(sb.BarLine("|"), sb.Note("a"), sb.Rest(1), sb.BarLine("|")).bars()
        assert next(bars) == Body(
            sb.BarLine("|"), sb.Note("a"), sb.Rest(1), sb.BarLine("|")
        )
        with pytest.raises(StopIteration):
            next(bars)

    def test_multiple_bar_iteration(self):
        b1 = Body(sb.BarLine("|"), sb.Note("a"), sb.Rest(1), sb.BarLine("|"))
        b2 = Body(sb.Note("a"), sb.Rest(1), sb.BarLine("|"))
        b3 = Body(sb.Note("a"), sb.Rest(1))

        bars = Body().extend_with_bars(b1, b2, b3).bars()
        assert next(bars) == b1
        assert next(bars) == b2
        assert next(bars) == b3
        with pytest.raises(StopIteration):
            next(bars)

        bars = Body().extend_with_bars(b2, b1, b3).bars()
        assert next(bars) == b2
        assert next(bars) == Body(sb.BarLine("|"))
        assert next(bars) == b1[1:]
        assert next(bars) == b3
        with pytest.raises(StopIteration):
            next(bars)
