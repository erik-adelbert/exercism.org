"""
forth.py
solution for https://exercism.org/tracks/python/exercises/forth
"""

from dataclasses import dataclass
from enum import Enum
from typing import ClassVar


def evaluate(input_data):
    """
    Evaluates a Forth program from a list of strings and returns the resulting stack.
    """
    return ForthProgram(input_data).stack


class OP(Enum):
    """List of Forth operation codes"""

    NOP = 0x0  # No operation
    INT = 0x1  # Integer value
    DEF = 0x2  # Define new word
    END = 0x3  # End definition
    ADD = 0x5  # Addition
    SUB = 0x6  # Subtraction
    MUL = 0x7  # Multiplication
    DIV = 0x8  # Division
    DUP = 0x9  # Duplicate the top of the stack
    DRP = 0xA  # Drop the top of the stack
    SWP = 0xB  # Swap the top two items on the stack
    OVR = 0xC  # Copy the second item to the top of the stack


@dataclass(slots=True)
class ForthOp:
    """
    Represents a single command or value in the Forth program.
    """

    code: OP = OP.NOP
    key: str = ""
    val: int = 0


class ForthProgram:
    """
    Represents a complete Forth program consisting of a list of commands,
    user-defined symbols, and an execution stack.
    """

    words: dict[str, list[ForthOp]]  # user defined words
    stack: list[int]

    # Map of Forth commands to internal operation codes
    BUILTINS: ClassVar[dict[str, OP]] = {
        ":": OP.DEF,
        ";": OP.END,
        "+": OP.ADD,
        "-": OP.SUB,
        "*": OP.MUL,
        "/": OP.DIV,
        "DUP": OP.DUP,
        "DROP": OP.DRP,
        "SWAP": OP.SWP,
        "OVER": OP.OVR,
    }

    def __init__(self, source: list[str]):
        self.words = {}
        self.stack = []

        for line in source:
            self._eval(self._parse(line))

    def _parse(self, source: str) -> list[ForthOp]:
        """
        Parses a line of Forth code into a list of ForthOps.
        """
        source = source.upper()
        tokens: list[ForthOp] = []

        defining = False  # defining context
        for token in source.split():
            # tokenize and continue at first match (cond switch)

            # look for an integer first...
            try:
                n = int(token)
                if defining:
                    # redefining an integer is illegal
                    raise ValueError("illegal operation")  # anti pattern for ValueError

                tokens.append(ForthOp(code=OP.INT, val=n))
                continue
            except ValueError as err:
                if not str(err).startswith("invalid literal for int()"):
                    raise err
                # tok is not a number proceed!

            # ...then if defining context is opened
            # token is the currently defined name...
            if defining:
                defining = False
                tokens.append(ForthOp(code=OP.DEF, key=token))
                continue

            # ...or maybe a user defined word...
            if token in self.words:
                tokens.extend(self.words[token])
                continue

            # ...or a builtin...
            if token in ForthProgram.BUILTINS:
                match (builtin := ForthProgram.BUILTINS[token]):
                    case OP.DEF:
                        defining = True  # open defining context
                    case _:
                        tokens.append(ForthOp(code=builtin, key=token))
                continue

            # token is not supported
            raise ValueError("undefined operation")

        return tokens

    def _eval(self, prog: list[ForthOp]):
        """
        Evaluates a list of ForthOps.
        """

        # binary builtins
        binary = {
            OP.ADD: lambda a, b: self.stack.append(a + b),
            OP.SUB: lambda a, b: self.stack.append(a - b),
            OP.MUL: lambda a, b: self.stack.append(a * b),
            OP.DIV: lambda a, b: self.stack.append(int(a / b)),
            OP.OVR: lambda a, b: list(map(self.stack.append, (a, b, a))),
            OP.SWP: lambda a, b: list(map(self.stack.append, (b, a))),
        }

        i = 0  # cmd index
        while i < len(prog):
            cmd = prog[i]

            match cmd.code:
                case OP.INT:
                    self.stack.append(cmd.val)  # push

                case OP.DEF:
                    # scan commands until definition end or fail
                    lo = hi = i + 1
                    while prog[hi].code != OP.END and hi < len(prog):
                        hi += 1

                    if hi == len(prog):
                        raise SyntaxError(f"def {cmd.key} missing closing ';'")

                    # store definition slice in word table
                    self.words[cmd.key] = prog[lo:hi]

                    # update i for outer scan
                    i = (hi - lo) + 1

                case OP.ADD | OP.SUB | OP.MUL | OP.DIV | OP.OVR | OP.SWP:
                    # binary op
                    try:
                        b, a = (
                            self.stack.pop(),
                            self.stack.pop(),
                        )  # order matters: b, a
                        binary[cmd.code](a, b)
                    except IndexError as exc:
                        raise StackUnderflowError from exc
                    except ZeroDivisionError as exc:
                        raise ZeroDivisionError("divide by zero") from exc

                case OP.DUP | OP.DRP:
                    # unary op
                    try:
                        a = self.stack.pop()  # drop
                        if cmd.code == OP.DUP:
                            self.stack.append(a)  # undo drop
                            self.stack.append(a)  # dup
                    except IndexError as exc:
                        raise StackUnderflowError from exc

                case OP.NOP:
                    pass  # nothing to do

                case _:
                    raise ValueError("illegal operation")  # anti pattern for ValueError

            i += 1  # next cmd
        return


class StackUnderflowError(Exception):
    """
    Raised when there are insufficient items on the stack to perform an operation.
    """

    def __init__(
        self,
        msg: str = "Insufficient number of items in stack",  # should'nt be titled
    ):
        super().__init__(msg)


# anti-pattern should be corrected to use these:
# class IllegalOperation(ValueError):
#     """illegal operation"""
#
#     def __init__(self, msg: str = "illegal operation"):
#         super().__init__(msg)
#
#
# class UndefinedVariable(ValueError):
#     """undefined variable"""
#
#     def __init__(self, varname: str):
#         super().__init__(f'"{varname}" is not defined')
