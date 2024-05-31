"""
anagram.py --
"""

from collections import Counter


def find_anagrams(word: str, candidates: list[str]):
    """find anagrams"""
    return list(
        filter(
            lambda w: w.lower() != word.lower()
            and Counter(w.lower()) == Counter(word.lower()),
            candidates,
        )
    )
