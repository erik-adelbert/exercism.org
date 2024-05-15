"""
rotational_cipher.py
solution to https://exercism.org/tracks/python/exercises/rotational-cipher
"""


def rotate(text: str, n: int):
    """
    RotN transcoding
    """

    plain = "abcdefghijklmnopqrstuvwxyz"
    wheel = plain[n:] + plain[:n]

    rotn = str.maketrans(
        plain + plain.upper(),
        wheel + wheel.upper(),
    )

    return text.translate(rotn)
