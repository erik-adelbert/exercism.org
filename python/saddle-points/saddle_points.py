"""
saddle_points.py --
"""


def saddle_points(matrix: list[list[int]]) -> list[dict[str, int]]:
    """
    Find the matrix saddle points
    """
    if matrix == []:
        return []

    W, H = len(matrix[0]), len(matrix)  # pylint: disable=invalid-name

    rmax = [max(row) for row in matrix]
    cmin = [min(col) for col in zip(*matrix)]
    try:
        # a saddle point is the maximum in its row and the minimum in its column
        return [
            {"row": j + 1, "column": i + 1}  # 1-based
            for i in range(W)
            for j in range(H)
            if rmax[j] == cmin[i] == matrix[j][i]
        ]
    except IndexError as e:
        raise ValueError("irregular matrix") from e
