"""
cahnge.py --
"""


def find_fewest_coins(coins, amount):
    """
    find fewest coins needed to change for amount
    """
    if amount < 0:
        raise ValueError("target can't be negative")

    # sort the available coins
    coins.sort()

    # Create a list to store the fewest number of coins for each amount from 0 to the target amount
    fewest = [float("inf")] * (amount + 1)
    fewest[0] = 0  # Base case: 0 coins needed to make change for 0

    for coin in coins:
        for i in range(coin, amount + 1):
            fewest[i] = min(fewest[i], fewest[i - coin] + 1)

    # Reconstruct the coins used
    result = []
    i = amount
    while i > 0:
        for coin in coins:
            if i - coin >= 0 and fewest[i - coin] == fewest[i] - 1:
                result.append(coin)
                i -= coin
                break
        else:
            raise ValueError("can't make target with given coins")

    return result
