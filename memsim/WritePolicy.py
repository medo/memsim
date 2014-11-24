from enum import Enum
class WritePolicy(Enum):
    write_through = 1
    write_back = 2
    write_allocate = 3
    write_around = 4
