"""
word_count.py --
"""

from collections import Counter
from string import punctuation


def count_words(sentence: str) -> dict:
    """
    Count word frequencies in a sentence
    We really don't want to that in the real world!!!
    This solution is weak and contractions are a tough problem anyway.
    Use a NLP ingestion module instead.
    """

    sentence = sentence.strip("'")
    sentence = (
        sentence.lower()
        .replace("\t", " ")
        .replace("\n", " ")
        .replace(",", " ")
        .replace("_", " ")
        .replace("'", "X")
        .replace(" X", " ")
        .replace("X ", " ")
    )

    sentence = sentence.translate(str.maketrans("", "", punctuation))
    sentence = sentence.replace("X", "'")
    counts = Counter(sentence.split(" "))
    counts.pop("", None)

    return dict(counts)
