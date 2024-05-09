from functools import reduce

NBOOK = 5
BOOKPRICE = 800

discounts = [
    0,
    0,
    2 * int(BOOKPRICE / 20),  # 5%  discount for sets of 2 different books
    3 * int(BOOKPRICE / 10),  # 10%  .
    4 * int(BOOKPRICE / 5),  # 20%  .
    5 * int(BOOKPRICE / 4),  # 25% discount for sets of 5 different books
]


def total(books: list[int]) -> int:
    """
    total calculates the total cost of purchasing the given books,
    considering discounts.

    args:
        books (List[int]): raw list of book types
    """
    list_price = len(books) * BOOKPRICE

    booksets = [0] * (NBOOK + 1)
    while len(books) > 0:
        s = set(books)
        booksets[len(s)] += 1
        list(map(books.remove, s))

    if (n := min(booksets[3], booksets[5])) > 0:
        booksets[3] -= n
        booksets[4] += 2 * n
        booksets[5] -= n

    discount = reduce(
        lambda a, b: a + b,
        [a * b for a, b in zip(booksets, discounts)],
    )

    return list_price - discount
