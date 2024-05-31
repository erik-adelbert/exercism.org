"""
grade_school.py --

"""

from collections import OrderedDict
from functools import wraps
from typing import List, Callable


class School:
    """A simple school roster"""

    def keepclean(fun: Callable):  # pylint: disable=E0213
        """Decorator which ensure roster ordering"""

        @wraps(fun)
        def inner(self, *args, **kwargs):
            self.clean()
            return fun(self, *args, **kwargs)  # pylint: disable=E1102

        return inner

    def __init__(self):
        self._dirty: bool = False
        self._roster: OrderedDict[str, int] = {}
        self._added: List[bool] = []

    def add_student(self, name, grade):
        """Add a student to the roster"""
        if name in self._roster:
            self._added.append(False)
            return

        self._roster[name] = grade
        self._added.append(True)
        self._dirty = True

    def clean(self):
        """Ensure ordering"""
        if self._dirty:
            self._roster = OrderedDict(
                sorted(self._roster.items(), key=lambda x: (x[1], x[0]))
            )
            self._dirty = False

    @keepclean
    def roster(self):
        """Get the school roster sorted by grade and names"""
        return list(self._roster.keys())

    @keepclean
    def grade(self, grade_number):
        """Get all students of a grade"""
        return [k for k, v in self._roster.items() if v == grade_number]

    def added(self):
        """Add ops statuses"""
        return self._added
