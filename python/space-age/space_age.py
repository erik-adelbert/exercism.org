"""
space_age.py --
"""

from functools import partialmethod


class SpaceAge:  # pylint: disable=too-few-public-methods
    """
    Computes age in space.
    """

    EARTHYEAR = 31557600

    ratios = {
        "mercury": 0.2408467,
        "venus": 0.61519726,
        "earth": 1,
        "mars": 1.8808158,
        "jupiter": 11.862615,
        "saturn": 29.447498,
        "uranus": 84.016846,
        "neptune": 164.79132,
    }

    def __init__(self, seconds: int):
        # Dynamically create member (age) and methods (on_earth(), on_mercury(), ...)
        setattr(SpaceAge, "age", seconds)  # self.age = seconds

        for planet in SpaceAge.ratios:
            setattr(
                SpaceAge,
                f"on_{planet}",
                partialmethod(self._compute, planet),
            )

    def _compute(self, planet: str) -> float:
        year = SpaceAge.ratios[planet] * SpaceAge.EARTHYEAR

        # two decimal hard precision
        return round(self.age / year, 2)  # pylint: disable=no-member
