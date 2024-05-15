"""
spiral_matrix.py
solution to https://exercism.org/tracks/python/exercises/spiral-matrix
"""


def spiral_matrix(size):
    """
    Build a size*size spiral matrix
    """
    n = int(size)
    num = _positive()
    spiral = [[0 for _ in range(n)] for _ in range(n)]

    left = top = 0
    right = down = n - 1

    while left <= right:
        for i in range(left, right + 1):
            spiral[top][i] = next(num)
        top += 1

        for j in range(top, down + 1):
            spiral[j][right] = next(num)
        right -= 1

        for i in range(right, left - 1, -1):
            spiral[down][i] = next(num)
        down -= 1

        for j in range(down, top - 1, -1):
            spiral[j][left] = next(num)
        left += 1

    return spiral


def _positive():
    i = 1
    while True:
        yield i
        i += 1
