"""
darts.py --

"""

from math import sqrt


def score(x, y):
    """
    Returns dart score
    """
    radius = sqrt(x**2 + y**2)

    for point in [(1, 10), (5, 5), (10, 1)]:
        if radius <= point[0]:
            return point[1]

    return 0
