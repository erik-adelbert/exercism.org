"""
variable_length_quantity.py --
"""


def encode(numbers: list[int]) -> list[int]:
    """VLQ encode a list of number"""

    def _encode_one(number: int) -> list[int]:
        encoded = [number & 0x7F]  # lsb word

        number >>= 7  # remaining
        while number:
            word = (1 << 7) | (number & 0x7F)
            encoded.append(word)
            number >>= 7

        return reversed(encoded)

    encoded: list[int] = []
    for n in numbers:
        encoded.extend(_encode_one(n))

    return encoded


def decode(encoded: list[int]) -> list[int]:
    """VLQ decode a number"""

    decoded = []

    n, done = 0, True
    for w in encoded:
        n, done = (n << 7) | (w & 0x7F), False

        if w & (1 << 7) == 0:
            decoded.append(n)
            n, done = 0, True

    if not done:
        raise ValueError("incomplete sequence")

    return decoded
