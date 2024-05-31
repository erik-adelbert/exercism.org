"""
dnd_character.py --
"""

from random import randint


def modifier(score: int) -> int:
    """compute a modifier"""
    return (score - 10) // 2


class Character:
    """DND Character"""

    attributes = [
        "strength",
        "dexterity",
        "constitution",
        "intelligence",
        "wisdom",
        "charisma",
        "hitpoints",
    ]

    def __init__(self):
        self._scores = [randint(3, 18) for _ in self.attributes]
        self._scores[-1] = 10 + modifier(self._scores[2])

    def __getattr__(self, attr):
        try:
            return self._scores[self.attributes.index(attr)]
        except ValueError as exc:
            raise AttributeError from exc

    def ability(self) -> int:
        """random ability"""
        return self._scores[randint(0, len(self._scores) - 2)]
