"""
proverb.py --
"""


def proverb(*args, qualifier: str = ""):
    """proverb"""

    if len(args) == 0:
        return []

    rhymes = [
        f"For want of a {arg1} the {arg2} was lost."
        for arg1, arg2 in zip(args, args[1:])
    ]

    if qualifier:
        rhymes.append(f"And all for the want of a {qualifier} {args[0]}.")
    else:
        rhymes.append(f"And all for the want of a {args[0]}.")
    return rhymes
