"""
diamond.py --
"""

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def rows(letter: str) -> list[str]:
    """
    Build an ascii diamond
    """

    print(letter, "->")

    letter = letter.upper()[0]  # first capital character
    index = ALPHABET.index(letter)  # 0-based

    if not letter:
        return []

    width = 2 * index + 1  # alway odd diamond width

    def mkrow(i: int) -> str:
        # build content and padding for a given row (0-based)
        content = (
            (
                ALPHABET[i]
                + " " * (2 * i - 1)
                + ALPHABET[i]  # always odd (2*n + 1) + 2 == 2 (n+1) +1
            )
            if i != 0
            else "A"
        )

        pad = " " * ((width - len(content)) // 2)
        return pad + content + pad  # row!

    # build upper diamond
    rows = []  # pylint: disable=redefined-outer-name
    for i in range(0, index + 1):
        rows.append(mkrow(i))

    # diamond is upper row + a vertical mirror accounting for the middle row
    return rows + rows[:-1][::-1]
