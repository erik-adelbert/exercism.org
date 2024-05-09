from functools import cache

@cache
def steps(num: int)->int:
    num = int(num)

    if num <= 0:
        raise ValueError("Only positive integers are allowed")
    
    if num == 1:
        return 0
    
    nstep = 1
    if num&1 == 0 :
        nstep += steps(num / 2)
    else:
        nstep += steps(3*num + 1)

    return nstep
    