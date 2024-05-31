"""
luhn.py --
"""


class Luhn:
    """Luhn validation class"""

    def __init__(self, card_num: str):
        card_num = card_num.replace(" ", "")

        if card_num == "0" or not set(card_num) <= set("0123456789"):
            self.isvalid = False
            return

        card = list(map(int, card_num))[::-1]

        for i in range(1, len(card), 2):
            n = 2 * card[i]
            card[i] = n if n < 10 else n - 9

        self.isvalid = sum(card) % 10 == 0

    def valid(self) -> bool:
        """Validates a Luhn number."""
        return self.isvalid
