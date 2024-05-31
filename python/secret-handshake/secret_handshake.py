"""
secret_handshake.py --
"""


def commands(binary: str):
    """
    Decode the given secret handshake number
    """
    # prepare binary for decoding
    binary = binary[5::-1]  # slice the rightmost digits in reverse

    secret = [
        "wink",
        "double blink",
        "close your eyes",
        "jump",
        "reverse",
    ]

    # decode
    actions = [s for s, b in zip(secret, binary) if b == "1"]

    # check output and act accordingly
    if not actions or actions[-1] != "reverse":
        return actions  # all done!

    return actions[:-1][::-1]  # omit "reverse" and reverse
