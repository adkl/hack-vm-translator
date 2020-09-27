from enum import Enum


class ArithmeticInstruction(Enum):
    add = 1
    sub = 2
    neg = 3
    eq = 4
    gt = 5
    lt = 6
    and_ = 7
    or_ = 8
    not_ = 9


class MemoryInstruction(Enum):
    push = 1
    pop = 2
