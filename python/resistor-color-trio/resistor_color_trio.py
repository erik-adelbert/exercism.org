"""
resistor_color_trio.py --
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


def label(colors: list[str]) -> str:
    """
    Decodes a tri-color resistor code
    """

    # Helper function to convert a color to its value
    def _int(color: str) -> int:
        return COLORCODE.index(color)

    # Unpack the significant color fields, ignore extra colors
    d1, d0, _pow, *colors = colors

    # Compute the scaled value
    value: int = (_int(d1) * 10 + _int(d0)) * (10 ** _int(_pow))

    # Normalize the value to use appropriate SI prefixes
    prefix = ""
    for lim, iso in (  # pylint: disable= invalid-name
        (1_000_000_000, "giga"),
        (1_000_000, "mega"),
        (1_000, "kilo"),
    ):
        if value >= lim:  # sieve filter
            value, prefix = value // lim, iso
            break

    # Build and return the final readable label
    return f"{value} {prefix}ohms"
