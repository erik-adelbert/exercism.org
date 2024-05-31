"""
pythagorean_triplet.py --

No other implementation presented in the dig deeper section is able to 
compute triplets_with_sum(128_123_456_789_256) in a reasonable amount 
of time on my machine but this one performs in a few hundred ms.

This implementation seems to be dominated by O(sqrt(n))
"""

from math import isqrt

NMIN = 12  # no triplet (a, b, c) with a+b+c < 12


def triplets_with_sum(n: int):
    """triplets_with_sum
    We are using euclid's formula to generate triples from primitive
    so we also have to generate triples for m, n coprimes and not both odd.
    Passing composite factors can produce duplicates, they have to be removed.
    """

    # return find_pythagorean_triples(n)
    triples = set()

    for factor in list(factors(n)):
        if factor & 1 == 0:  # discard even factors
            continue

        # scale down n by factor until there's no more triples
        if (m := n // factor) < NMIN:
            break

        # generate new triplets from scaled down
        for t in euclid_triplets_with_sum(m):
            triples.add(frozenset(x * factor for x in t))  # scale back up and dedup

    # reorder triplets and output
    return sorted(sorted(x) for x in triples)


def euclid_triplets_with_sum(n: int):
    """euler triplets with sum
    we have:
        a^2 + b^2 = c^2
        a + b + c = n

    with:
        a = u^2 - v^2
        b = 2uv
        c = u^2 + v^2

       (
        with U = u^2 and V = v^2 <=> a = U-V, b^2= 4UV, c = U+V
        a^2 + b^2 = U^2 - 2.UV + V^2 + 4.UV
        = U^2 + 2.U.V + V^2
        = (U + V)^2
        = c^2
        )

    it comes:
        a+b+c = 2 u^2 + 2 uv = n

        u (u+v) = n/2
        v = n/2u - u

        with 0 < u < (u+v) any cofactors of n/2
    """
    triples = []

    if n < NMIN or n & 1:
        return triples

    for u in list(factors(n // 2)):
        if (v := n // (2 * u) - u) <= 0:
            break
        if u > v:
            triples.append((u**2 - v**2, 2 * u * v, u**2 + v**2))

    return triples


def factors(n: int):
    """
    ordered factors of a positive int
    """
    larges = []

    for i in range(1, isqrt(n) + 1):
        if n % i == 0:
            yield i
            if i * i != n:
                larges.append(n // i)
    for i in reversed(larges):
        yield i


# print(triplets_with_sum(128_123_456_789_256))
# [
#   [4944966942504, 61489987747497, 61688502099255],
#   [21156381182184, 51391340451287, 55575735155785],
#   [32030864197314, 42707818929752, 53384773662190],
#   [35739589404192, 39278831400244, 53105035984820]
# ]

# ❯ time python pythagorean_triplet.py
# [[4944966942504, 61489987747497, 61688502099255], ...
# python pythagorean_triplet.py  0.67s user 0.01s system 99% cpu 0.682 total
