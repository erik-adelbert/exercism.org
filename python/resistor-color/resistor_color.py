"""
resistor_color.py --
"""

CODE = [
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


def color_code(color: str) -> int:
    """color code"""
    return CODE.index(color)


def colors():
    """colors"""
    return CODE
