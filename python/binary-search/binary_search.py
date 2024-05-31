"""
binary_search.py --
"""

from math import floor

NotFound = ValueError("value not in array")


def find(search_list: list[int], value: int) -> int:
    """Bin searches for value in search_list"""
    l, r = 0, len(search_list) - 1

    while l <= r:
        m = floor((r + l) / 2)
        if search_list[m] < value:
            l = m + 1
        elif search_list[m] > value:
            r = m - 1
        else:
            return m
    raise NotFound
