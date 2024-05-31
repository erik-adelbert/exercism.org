"""
perfect_numbers.py --
"""

import math


def divisors(n):
    """Find all divisors of n"""
    larges = []
    for i in range(1, int(math.sqrt(n) + 1)):
        if n % i == 0:
            yield i
            if i * i != n:
                larges.append(n // i)

    for divisor in larges[::-1]:
        yield divisor


def classify(n: int):
    """A perfect number equals the sum of its positive divisors.

    :param number: int a positive integer
    :return: str the classification of the input integer
    """
    if n < 1:
        raise ValueError("Classification is only possible for positive integers.")

    nn = sum(list(divisors(n))) - n  # last item of list(divisors) is n
    if n < nn:
        return "abundant"
    if n == nn:
        return "perfect"
    return "deficient"
