"""
resistor_color_expert.py --
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

TOLERANCE = {
    "grey": "±0.05%",
    "violet": "±0.1%",
    "blue": "±0.25%",
    "green": "±0.5%",
    "brown": "±1%",
    "red": "±2%",
    "gold": "±5%",
    "silver": "±10%",
}


def resistor_label(colors: list[str]) -> str:
    """
    Decodes a resistor code
    """

    # Helper function to convert a color to its value
    def _int(color: str) -> int:
        return COLORCODE.index(color)

    if len(colors) == 1:  # Handle single color case
        return f"{_int(colors[0])} ohms"

    # Multiple colors layout:
    # colors[0:-2] | colors[-2]  | colors[-1]
    # value        | Log(factor) | tolerance

    # Unpack the last two color fields
    *colors, _pow, _color = colors  # pylint: disable=invalid-name

    # Extract tolerance, compute multiplier
    tolerance_str = TOLERANCE[_color]
    factor: int = 10 ** _int(_pow)

    # Compute the scaled value from the least significant colors
    value = (
        sum(_int(color) * 10**i for i, color in enumerate(colors[::-1])) * factor
    )  # map/reduce

    # Normalize the value to use appropriate SI prefixes
    prefix = ""
    for lim, iso in (  # pylint: disable= invalid-name
        (1_000_000_000, "giga"),
        (1_000_000, "mega"),
        (1_000, "kilo"),
    ):
        if value >= lim:  # sieve filter
            value, prefix = value / lim, iso
            break

    # Format the value to remove unnecessary decimal places
    value_str = f"{value:.2f}".rstrip("0").rstrip(".")  # ex: 12.0 -> 12, 3.40 -> 3.4

    # Build and return the final readable label
    return f"{value_str} {prefix}ohms {tolerance_str}"
