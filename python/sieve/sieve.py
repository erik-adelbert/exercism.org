"""
sieve.py --
"""


def primes(limit: int):
    """Eratosthenes sieve"""
    if limit < 2:
        return []

    sieve = list(range(2, limit + 1))

    def _biff(i: int, prime: int):
        for ii in range(i + 1, len(sieve)):
            if not sieve[ii]:
                continue
            if sieve[ii] % prime == 0:
                sieve[ii] = 0

    for i, prime in enumerate(sieve):
        match prime:
            case 0:
                continue
            case _:
                _biff(i, prime)

    return list(filter(None, sieve))
