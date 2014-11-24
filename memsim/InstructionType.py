from enum import Enum
class InstructionType(Enum):
    load = 1
    store = 2
    jump = 3
    branch_if_equal = 4
    jump_and_link = 5
    return_ = 6
    add = 7
    subtract = 8
    add_immediate = 9
    nand = 10
    multiply = 11
