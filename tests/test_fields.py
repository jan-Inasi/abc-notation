from abc_notation.fields.unit_note_length import UnitNoteLength
from abc_notation.fields.tempo import Tempo, Beat


class TestFields:

    def test_unit_note_length(self):
        unl_header = UnitNoteLength(4)
        unl_inline = UnitNoteLength(4, inline=True)

        assert str(unl_header) == "L: 1/4\n"
        assert str(unl_inline) == "[L:1/4]"

    def test_tempo(self):
        tempo = Tempo("Allegro")

        assert str(tempo) == 'Q: "Allegro"\n'
        tempo.inline = True
        assert str(tempo) == '[Q:"Allegro"]'

        tempo = Tempo(bpm=120)

        assert str(tempo) == 'Q: 120\n'
        tempo.inline = True
        assert str(tempo) == '[Q:120]'

        tempo.inline = False
        tempo.beats = [Beat(4, 4)]
        assert str(tempo) == 'Q: 4/4=120\n'
        tempo.inline = True
        assert str(tempo) == '[Q:4/4=120]'

        tempo = Tempo(beats=[Beat(1, 4), Beat(2, 4), Beat(1, 4)], bpm=100)
        assert str(tempo) == 'Q: 1/4 2/4 1/4=100\n'
        tempo.inline = True
        assert str(tempo) == '[Q:1/4 2/4 1/4=100]'

        tempo = Tempo(text="Allegro", beats=[Beat(1, 4), Beat(3, 4)], bpm=100)
        assert str(tempo) == 'Q: "Allegro" 1/4 3/4=100\n'
        tempo.inline = True
        assert str(tempo) == '[Q:"Allegro" 1/4 3/4=100]'

        tempo = Tempo(text="Allegro", bpm=80)
        assert str(tempo) == 'Q: "Allegro" 80\n'
        tempo.inline = True
        assert str(tempo) == '[Q:"Allegro" 80]'
