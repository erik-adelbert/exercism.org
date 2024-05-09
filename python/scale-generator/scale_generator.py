"""
scale_generator.py
"""

from itertools import compress, repeat


class Scale:
    """
    An arbitrary minor, major or augmented second scales
    """

    Sharps = ["A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"]
    Flats = ["A", "Bb", "B", "C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab"]

    def __init__(self, tonic):
        self.tonic = tonic
        self.scale = []
        self.mode = Mode.Chromatic

    def chromatic(self) -> list[str]:
        """
        chromatic returns a chromatic scale based on the tonic
        """
        return self.__scale("Chromatic")

    def interval(self, interval: str) -> list[str]:
        """
        interval returns an arbitrary minor, major or augmented second scale
        """
        return self.__scale(interval)

    def __scale(self, m: str):
        self.__set_mode(m)
        scale = list(compress(self.scale, self.mode.selector()))

        return scale if m == "Chromatic" else scale + [scale[0]]

    def __set_mode(self, s: str):
        self.mode = Mode(s)
        base = self.__base()

        flat_conds = (
            lambda x: x in ("F", "Bb", "Eb", "Ab", "Db", "d", "g", "c", "f", "bb"),
            lambda x: x == "Gb" and self.mode.name() == "Major",
            lambda x: x == "eb" and self.mode.name() != "Major",
        )
        if any(test(tonic) for test, tonic in zip(flat_conds, repeat(self.tonic))):
            self.scale = Scale.Flats[base:] + Scale.Flats[:base]
        else:
            self.scale = Scale.Sharps[base:] + Scale.Sharps[:base]

    def __base(self) -> int:
        tonic = self.tonic.capitalize()

        try:
            return Scale.Sharps.index(tonic)
        except ValueError:
            return Scale.Flats.index(tonic)


class Mode:
    """
    A 12bit scale representation
    https://ianring.com/musictheory/scales/
    """

    Chromatic = int(0b111111111111)

    well_known = {
        int(0b111111111111): "Chromatic",
        int(0b101010110101): "Major",
        # int(0b010110101101): "Aeolian",
        # int(0b011010101101): "Dorian",
        # int(0b010101101011): "Locrian",
        # int(0b101011010101): "Lydian",
        # int(0b011010110101): "Mixolydian",
        # int(0b010110101011): "Phrygian",
        # int(0b010101010101): "Whole",
    }

    def __init__(self, interval: str):
        if interval.title() == "Chromatic":
            self.value = int(0b111111111111)
            return

        stride = {"m": 1, "M": 2, "A": 3}

        i, m = int(0), int(1)
        for c in interval:
            m |= 1 << i
            i += stride[c]

        self.value = m

    def selector(self) -> iter:
        """
        Builds a selector to be used by itertools.compress()
        """

        return map(int, reversed([*f"{self.value:012b}"]))

    def name(self) -> str:
        """
        Returns the mode name if known
        """

        if self.value in Mode.well_known:
            return Mode.well_known[self.value]
        return "unkown"
