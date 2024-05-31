"""
sum_of_multiples.py ==
"""


def sum_of_multiples(level: int, items: list[int]) -> int:
    """sum the multiples"""

    points = []
    for x in filter(None, items):
        m = x
        while m < level:
            points.append(m)
            m += x

    return sum(set(points))
