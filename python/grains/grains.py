MAXSQUARE = 64

def square(num: int) -> int:
    if num < 1 or num > MAXSQUARE:
        raise ValueError("square must be between 1 and 64")
    return 1 << (num-1)


def total() -> int:
    return (1 << MAXSQUARE)-1
