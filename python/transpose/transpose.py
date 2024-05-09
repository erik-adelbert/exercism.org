from itertools import zip_longest


def transpose(input: str) -> str:
    """
    Output the transposed of the given input lines
    """
    lines = input.splitlines()
    trans = map("".join, list(zip_longest(*lines, fillvalue="\N{THIN SPACE}")))
    trans = map(lambda x: x.rstrip("\N{THIN SPACE}"), trans)
    return "\n".join(trans).replace("\N{THIN SPACE}", " ")
