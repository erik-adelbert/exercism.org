"""
robot_simulator.py --
"""

from dataclasses import dataclass
from typing import ClassVar, Dict, Tuple


# Globals for the directions
# Change the values as you see fit
EAST: int = 0
NORTH: int = 1
WEST: int = 2
SOUTH: int = 3


@dataclass(init=False)
class Robot:
    """Robot"""

    offsets: ClassVar[Dict[int, Tuple[int, int]]] = {
        NORTH: (0, 1),
        EAST: (1, 0),
        SOUTH: (0, -1),
        WEST: (-1, 0),
    }

    direction: int = NORTH
    coordinates: Tuple[int, int] = (0, 0)

    def __init__(self, direction: int, x: int, y: int):
        self.direction = direction
        self._x = x
        self._y = y

    @property
    def coordinates(self) -> Tuple[int, int]:
        """coos"""
        return (self._x, self._y)

    def move(self, moves: str):
        """move"""

        for bearing in moves:
            match bearing:
                case "R":
                    self.direction = (self.direction - 1) % 4
                case "L":
                    self.direction = (self.direction + 1) % 4
                case "A":
                    self._x += Robot.offsets[self.direction][0]
                    self._y += Robot.offsets[self.direction][1]
