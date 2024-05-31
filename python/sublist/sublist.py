"""
This exercise stub and the test suite contain several enumerated constants.

Enumerated constants can be done with a NAME assigned to an arbitrary,
but unique value. An integer is traditionally used because it’s memory
efficient.
It is a common practice to export both constants and functions that work with
those constants (ex. the constants in the os, subprocess and re modules).

You can learn more here: https://en.wikipedia.org/wiki/Enumerated_type
"""

# Possible sublist categories.
# Change the values as you see fit.
SUBLIST = 0
SUPERLIST = 1
EQUAL = 2
UNEQUAL = 3


def sublist(list_one: list, list_two: list):
    """
    Checks relation between to lists.
    """
    a, b = list_one, list_two

    def is_sub(sub: list, test: list):
        return any(
            test[i : i + len(sub)] == sub for i in range(len(test) - len(sub) + 1)
        )

    if a == b:
        return EQUAL

    if is_sub(a, b):
        return SUBLIST

    if is_sub(b, a):
        return SUPERLIST

    return UNEQUAL
