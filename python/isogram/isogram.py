"""
isogram.py --
"""


def is_isogram(word: str) -> bool:
    """Checks if the given word as no repeating letters"""
    letters = list(filter(lambda c: c.isalpha(), word.lower()))
    return len(set(letters)) == len(letters)
