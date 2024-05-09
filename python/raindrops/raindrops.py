""" 
exercism raindrops
"""

def convert(number: int) -> str:
    """
    convert a number into its corresponding raindrops sound.

    """

    number = int(number)
    sounds = (
        (3, 'Pling'),
        (5, 'Plang'),
        (7, 'Plong'),
    )

    def div(n, d):
        return n%d == 0

    sound = ''.join(s for d, s in sounds if div(number, d))
    if not sound:
        return str(number)
    return sound
