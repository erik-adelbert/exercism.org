"""
tournament.py --
"""

from collections import defaultdict, namedtuple
from dataclasses import asdict, dataclass, field
from typing import ClassVar, NamedTuple


def tally(rows: list[str]):
    """tally a tournament"""

    tournament: TeamDict[str, Team] = TeamDict(dict)

    for row in rows:  # ex. Devastating Donkeys;Blithering Badgers;win
        ateam, bteam, aresult = row.split(";")
        bresult = "win" if aresult == "loss" else "loss" if aresult == "win" else "draw"

        # ex. (("Devastating Donkeys", "win") ("Blithering Badgers", loss))
        for team, result in ((ateam, aresult), (bteam, bresult)):
            tournament[team].tally(result)

    pretty: list[str] = [Team.header()] + [
        str(team) for team in sorted(tournament.values())
    ]
    return pretty


@dataclass
class Team:
    """A team scoreboard"""

    FMT: ClassVar[str] = "{0:30} |{1:3} |{2:3} |{3:3} |{4:3} |{5:>3}"
    SCALE: ClassVar[NamedTuple] = namedtuple("Scale", ["WIN", "DRAW", "LOSS"])(3, 1, 0)

    name: str = "noname"
    mp: int = field(init=False, default=0)
    w: int = field(init=False, default=0)
    d: int = field(init=False, default=0)
    l: int = field(init=False, default=0)

    @property  # virtual
    def p(self) -> int:
        """computes team score"""
        scale = __class__.SCALE
        return self.w * scale.WIN + self.d * scale.DRAW + self.l * scale.LOSS

    def __lt__(self, other):
        if self.p == other.p:
            return self.name < other.name  # 2nd ascending names
        return self.p > other.p  # 1st descending scores

    def tally(self, result):
        """tally a team result"""
        match result:
            case "win":
                self.w += 1
            case "loss":
                self.l += 1
            case "draw":
                self.d += 1
            case _:
                raise ValueError(f"unkown result: {result[:5]}...")
        self.mp += 1

    def __str__(self):
        """create a custom string representation"""
        return __class__.FMT.format(*asdict(self).values(), self.p)

    @staticmethod
    def header() -> str:
        """make a header row"""
        return __class__.FMT.format("Team", " MP", "  W", "  D", "  L", " P")


class TeamDict(defaultdict):
    """An adhoc team map with a sensible default"""

    def __init__(self, default_factory):
        super().__init__(default_factory)

    def __missing__(self, key):
        self[key] = value = Team(key)
        return value
