"""
roman_numerals.py --
"""

BASE = {
    1000: "M",
    900: "CM",
    500: "D",
    400: "CD",
    100: "C",
    90: "XC",
    50: "L",
    40: "XL",
    10: "X",
    9: "IX",
    5: "V",
    4: "IV",
    1: "I",
}


def roman(number: int) -> str:
    """convert roman to decimal"""

    out: list[str] = []
    for n, rom in BASE.items():
        while number >= n:
            out.append(rom)
            number -= n

    return "".join(out)
