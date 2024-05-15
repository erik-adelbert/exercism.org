"""
exercism meetup.py
"""

from calendar import Calendar
from typing import List


# subclassing the built-in ValueError to create MeetupDayException
class MeetupDayException(ValueError):
    """Exception raised when the Meetup weekday and count do not result in a valid date.
    message: explanation of the error.

    """

    def __init__(self, message):
        self.message = message


WEEKS = ["first", "second", "third", "fourth", "fifth"]
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


def meetup(year: int, month: int, week: str, weekday: str):
    """Find the date of a Meetup day based on the given year,
    month, week, and day of the week."""

    dates = Calendar().monthdatescalendar(year, month)
    dates = filter(lambda x: x.month == month, flatten(dates))

    # ex. days = {'Monday': [datetime.date(2013, 7, 1), datetime.date...], 'Tuesday':...
    days = {d: [] for d in DAYS}
    for d in dates:
        days[DAYS[d.weekday()]].append(d)

    match week:
        case "teenth":
            return next(filter(lambda x: 13 <= x.day <= 19, days[weekday]))
        case "last":
            return days[weekday][-1]

    try:
        i = WEEKS.index(week)
        return days[weekday][i]
    except IndexError as inexist:
        raise MeetupDayException("That day does not exist.") from inexist


def flatten(ll: List[List]) -> List:
    """Flatten a list of lists into a single list."""
    return [x for l in ll for x in l]
