"""
isbn_verifier.py --
"""


def is_valid(isbn: str) -> bool:
    """Validates an ISBN number."""
    isbn = isbn.replace("-", "").upper()

    if not isbn or len(isbn) != 10 or "X" in isbn[:-1]:
        return False

    if not set(isbn) <= set("0123456789X"):
        return False

    def _toint(c: str):
        if c == "X":
            return 10
        return int(c)

    digits = [_toint(c) for c in isbn[::-1]]

    return sum(a * b for a, b in enumerate(digits, start=1)) % 11 == 0
