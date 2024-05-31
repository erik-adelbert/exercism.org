"""
matrix.py
"""


class Matrix:
    """
    An integer matrix built out of a string
    """

    def __init__(self, matrix_string):
        # split string in rows then split and convert rows to integers
        self.matrix = [
            list(map(int, row.split(" "))) for row in matrix_string.split("\n")
        ]

    def row(self, index):
        """return a matrix row"""
        index -= 1  # convert to 0-based
        return self.matrix[index]

    def column(self, index):
        """return a matrix col"""
        index -= 1  # convert to 0-based
        return [row[index] for row in self.matrix]
