"""
bottle_song.py --
"""

NUMBERS = [
    "no",
    "one",
    "two",
    "three",
    "four",
    "five",
    "six",
    "seven",
    "eight",
    "nine",
    "ten",
]


def recite(start, take=1):
    """Recite verses of the song"""

    def _str(d: int) -> str:
        return NUMBERS[d]

    def verse(i: int):
        lines = [
            f"{_str(i).title()} green bottle{'s' if i != 1 else ''} hanging on the wall,",
            f"{_str(i).title()} green bottle{'s' if i != 1 else ''} hanging on the wall,",
            "And if one green bottle should accidentally fall,",
            f"There'll be {_str(i-1)} green bottle{'s' if i != 2 else ''} hanging on the wall.",
            "",
        ]

        return lines

    return [rhyme for i in range(start, start - take, -1) for rhyme in verse(i)][:-1]
