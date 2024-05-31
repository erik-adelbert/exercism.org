"""
pangram.py --
"""

from string import ascii_lowercase


def is_pangram(sentence: str) -> bool:
    """is_pangram"""
    alphabet = set(ascii_lowercase)
    return alphabet.issubset(sentence.lower())
