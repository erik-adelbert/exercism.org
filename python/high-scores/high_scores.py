"""
high_scores.py --
"""


class HighScores:
    """
    Handles scores.
    """

    def __init__(self, scores):
        self._scores = scores

    @property
    def scores(self):
        """Returns all scores"""
        return self._scores

    def latest(self):
        """Returns the latest score"""
        return self._scores[-1]

    def personal_best(self):
        """Returns the best score"""
        return max(self._scores)

    def personal_top_three(self):
        """Returns the best score"""
        return sorted(self._scores)[-3:][::-1]
