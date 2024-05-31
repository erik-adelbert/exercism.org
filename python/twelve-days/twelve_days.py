"""
twelve_day.py --
"""

GIFTS = [
    "",
    ("first", "and a Partridge in a Pear Tree."),
    ("second", "two Turtle Doves, "),
    ("third", "three French Hens, "),
    ("fourth", "four Calling Birds, "),
    ("fifth", "five Gold Rings, "),
    ("sixth", "six Geese-a-Laying, "),
    ("seventh", "seven Swans-a-Swimming, "),
    ("eighth", "eight Maids-a-Milking, "),
    ("ninth", "nine Ladies Dancing, "),
    ("tenth", "ten Lords-a-Leaping, "),
    ("eleventh", "eleven Pipers Piping, "),
    ("twelfth", "twelve Drummers Drumming, "),
]


def recite(start: int, end: int):
    """
    Recite twelve days of christmas
    """

    def recite_one(verse):
        rhymes = []

        rhymes.append(
            f"On the {GIFTS[verse][0]} day of Christmas my true love gave to me: "
        )
        rhymes.extend([GIFTS[day][1] for day in range(verse, 0, -1)])

        if verse == 1:
            rhymes[-1] = rhymes[-1][4:]

        return "".join(rhymes)

    return [recite_one(verse) for verse in range(start, end + 1)]
