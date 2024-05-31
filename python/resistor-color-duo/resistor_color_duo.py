"""
resistor_color_duo.py --
"""

COLORCODE = [
    "black",
    "brown",
    "red",
    "orange",
    "yellow",
    "green",
    "blue",
    "violet",
    "grey",
    "white",
]


def value(colors: list[str]) -> int:
    """
    Decodes a bi-color resistor code
    """
    return COLORCODE.index(colors[0]) * 10 + COLORCODE.index(colors[1])
