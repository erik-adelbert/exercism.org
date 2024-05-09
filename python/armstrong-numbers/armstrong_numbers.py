def is_armstrong_number(num: int) -> bool:
    return sum(map(lambda x: int(x)**len(str(num)), str(num))) == num
