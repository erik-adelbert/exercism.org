"""
minesweeper.py --
"""

BoardError = ValueError("The board is invalid with current input.")


def annotate(minefield) -> list[str]:
    """annotate"""

    # validate minefield
    if set("".join(minefield)) > set(" *") or any(
        len(row) != len(minefield[0]) for row in minefield
    ):
        raise BoardError

    # null minefield is valid
    if not minefield:
        return minefield

    if len(minefield) == 1 and not minefield[0]:
        return [""]

    # extend minefield borders
    w = len(minefield[0])
    empty_row = list(" " * (w + 2))  # extended empty row

    extended = [empty_row]
    for row in minefield:
        extended.append([" ", *row, " "])  # extend row
    extended.append(empty_row)

    # count mines
    neighbors = (
        (-1, -1),
        (-1, +0),
        (-1, +1),
        (+0, -1),
        (+0, +1),
        (+1, -1),
        (+1, +0),
        (+1, +1),
    )

    # scan and annote inside extended without bounds checking
    h, w = len(extended), len(extended[0])
    for j in range(1, h - 1):
        for i in range(1, w - 1):
            if extended[j][i] == " ":
                extended[j][i] = str(
                    sum(1 for dj, di in neighbors if extended[j + dj][i + di] == "*")
                )

    # prepare and return annotated minefield
    return ["".join(row[1 : w - 1]).replace("0", " ") for row in extended[1 : h - 1]]
