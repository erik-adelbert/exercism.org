"""
ocr_numbers.py --
"""

BASE = [
    [" _ ", "| |", "|_|"],  # 0
    ["   ", "  |", "  |"],  # 1
    [" _ ", " _|", "|_ "],  # 2
    [" _ ", " _|", " _|"],  # 3
    ["   ", "|_|", "  |"],  # 4
    [" _ ", "|_ ", " _|"],  # 5
    [" _ ", "|_ ", "|_|"],  # 6
    [" _ ", "  |", "  |"],  # 7
    [" _ ", "|_|", "|_|"],  # 8
    [" _ ", "|_|", " _|"],  # 9
]


def convert(input_grid: list[str]) -> list[int]:
    """
    read rasterized numbers
    """

    if len(input_grid) % 4 != 0:
        raise ValueError("Number of input lines is not a multiple of four")

    if len(input_grid) > 4:
        # numbers separated by empty lines are recognized
        return ",".join(
            [
                convert(x)
                for x in [input_grid[i : i + 4] for i in range(0, len(input_grid), 4)]
            ]
        )

    # transpose input digits
    numbers = ["".join(x) for x in zip(*(input_grid[:-1]))]  # transpose strings
    if len(numbers) % 3 != 0:
        raise ValueError("Number of input columns is not a multiple of three")

    numbers = [
        (numbers[i], numbers[i + 1], numbers[i + 2]) for i in range(0, len(numbers), 3)
    ]

    # transpose BASE items
    base = [
        "".join("".join(x) for x in zip(*n))  # transpose wrapped strings
        for n in [[list(x) for x in n] for n in BASE]
    ]

    # match numbers
    for i, x in enumerate(numbers):
        try:
            numbers[i] = base.index("".join(x))
        except ValueError:
            numbers[i] = "?"

    return "".join(list(map(str, numbers)))
