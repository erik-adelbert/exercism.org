def valid(f):
    def check(sides):
        return sum(sides) > 2 * max(sides) and f(sides)
    return check

@valid
def equilateral(sides) -> bool:
    return len(set(sides)) == 1

@valid
def isosceles(sides):
    return len(set(sides)) < 3

@valid
def scalene(sides):
    return not (isosceles(sides) or equilateral(sides))
