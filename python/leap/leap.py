def leap_year(year):
    def div(n, d):
        return n%d == 0

    return div(year, 4) and (not div(year, 100) or div(year, 400))
