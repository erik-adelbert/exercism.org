"""
all_your_base.py --
"""

from functools import reduce


def rebase(ibase: int, digits: list[int], obase: list[int]):
    """translate digits between bases"""
    if ibase < 2:
        raise ValueError("input base must be >= 2")

    if obase < 2:
        raise ValueError("output base must be >= 2")

    if not all(0 <= d < ibase for d in digits):
        raise ValueError("all digits must satisfy 0 <= d < input base")

    n = reduce(lambda a, b: a * ibase + b, digits, 0)
    if n == 0:
        return [0]

    out = []
    while n:
        out.append(n % obase)
        n = n // obase
    return out[::-1]
