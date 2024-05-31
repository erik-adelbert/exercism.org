"""
wordy.py --
"""


def answer(question: str):
    """Parse ans eval a question"""

    # sanitize question
    question = (
        question.removeprefix("What is")
        .removesuffix("?")
        .strip()
        .replace("plus", "+")
        .replace("minus", "-")
        .replace("multiplied by", "*")
        .replace("divided by", "/")
    )

    if not question:
        raise SyntaxError

    if any(c.isalpha() for c in question):
        raise UnknownOpError

    return run(question)


SyntaxError = ValueError("syntax error")  # pylint: disable=redefined-builtin
UnknownOpError = ValueError("unknown operation")


def run(program: str) -> int:
    """parse/eval program"""

    def evaluate(OP: str, A: int, B: int) -> int:  # pylint: disable=invalid-name
        match OP:
            case "+":
                return A + B
            case "-":
                return A - B
            case "*":
                return A * B
            case "/":
                return A / B

    supported = "+-*/"

    tokens = program.split()

    ACC, N, OP = 0, 0, ""  # pylint: disable=invalid-name
    state = "init"
    for tok in tokens:
        match state:
            case "init":
                try:

                    ACC = int(tok)  # pylint: disable=invalid-name
                    state = "readOP"

                except ValueError as e:
                    raise SyntaxError from e
            case "readOP":
                if not tok in supported:
                    raise SyntaxError

                OP = tok  # pylint: disable=invalid-name
                state = "readA"

            case "readA":
                try:

                    N = int(tok)  # pylint: disable=invalid-name
                    ACC = evaluate(OP, ACC, N)  # pylint: disable=invalid-name
                    state = "readOP"

                except ValueError as e:
                    raise SyntaxError from e

    if state != "readOP":
        raise SyntaxError

    return ACC
