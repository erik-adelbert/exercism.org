"""
atbash.py
solution to https://exercism.org/tracks/python/exercises/atbash-cipher
"""

from textwrap import wrap


def atbash(s: str, decode: bool = False) -> str:  # pylint: disable=redefined-outer-name
    """
    Prepare and apply atbash transcoding
    """

    plain = "abcdefghijklmnopqrstuvwxyz"
    cipher = "".join(reversed(plain))

    atbash = str.maketrans(plain, cipher)  # pylint: disable=redefined-outer-name

    def compact(s: str) -> str:
        return "".join(s.lower().split())

    def coder(c: str) -> str:
        return c if c.isdecimal() else c.translate(atbash) if c.isalpha() else ""

    def transcode(s: str) -> str:
        return "".join(map(coder, compact(s)))

    if decode:
        return transcode(s)
    return " ".join(wrap(transcode(s), 5))


def encode(plain_text: str) -> str:
    """
    Encode a string using atbash
    """

    return atbash(plain_text)


def decode(ciphered_text: str) -> str:
    """
    Decode an atbash string
    """

    return atbash(ciphered_text, decode=True)
