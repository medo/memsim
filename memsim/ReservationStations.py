from InstructionProgress import InstructionProgress
from InstructionType import InstructionType

class ReservationStations:
    def __init__(self, names, cycles, reorder_buffers):
        self.reorder_buffers = reorder_buffers
        self.entries = {}
        for i in cycles.keys():
            self.entries[i] = []
        for i in names:
            self.entries[i].append(ReservationStationEntry(i, cycles[i], self.reorder_buffers))

    def can_hold(self, type_):
        return self.get(type_) != -1

    def get(self, type_):
        for i in range(len(self.entries[type_])):
            if self.entries[type_][i].operation == -1:
                return self.entries[type_][i]
        return -1

    def __str__(self):
        ret = ""
        for i in self.entries.keys():
            for j in range(len(self.entries[i])):
                ret += self.entries[i][j].to_str() + "\n"
        return ret

    
class ReservationStationEntry:

    MASK = 0xFFFF

    def __init__(self, type_, cycles, reorder_buffers):
        self.type_ = type_
        self.cycles = cycles
        self.reorder_buffers = reorder_buffers
        self.clear()

    def clear(self):
        self.busy = False
        self.vj = 0
        self.vk = 0
        self.qj = -1
        self.qk = -1
        self.address = -1
        self.cycles_left = 0
        self.progress = 0
        self.first_load = True
        self.dest = 0
        self.operation = -1
        self.result = 0

    def start(self):
        self.cycles_left = self.cycles

    def progress_single_cycle(self):
        if self.cycles_left > 0:
            self.cycles_left -= 1
    
    def finished(self):
        return self.cycles_left == 0

    def set_busy(self, value):
        self.busy = value

    def is_busy(self):
        return self.busy

    def get_reorder_buffer(self):
        return self.reorder_buffers.get(self.dest)

    def execute(self):
        current_buffer = self.get_reorder_buffer()
        #if self.operation == InstructionType.load : self.load(instruction.reg_a, instruction.reg_b, instruction.imm)
        #if self.operation == InstructionType.store: self.store(instruction.reg_a, instruction.reg_b, instruction.imm)
        #if self.operation == InstructionType.jump: self.jump(instruction.reg_a, instruction.imm)
        #if self.operation == InstructionType.branch_if_equal: self.branch_if_equal(instruction.reg_a, instruction.reg_b, instruction.imm)
        #if self.operation == InstructionType.jump_and_link: self.jump_and_link(instruction.reg_a, instruction.reg_b)
        #if self.operation == InstructionType.return_: self.return_(instruction.reg_a)
        if self.operation == InstructionType.add: self.result = (self.vj + self.vk) & self.MASK
        if self.operation == InstructionType.subtract: self.result = (self.vj - self.vk) & self.MASK
        if self.operation == InstructionType.add_immediate: self.result = (self.vj + self.vk) & self.MASK
        if self.operation == InstructionType.nand: self.result = (~(self.vj & self.vk) & self.MASK)
        if self.operation == InstructionType.multiply: self.result = (self.vj * self.vk) & self.MASK
        #if self.operation == InstructionType.halt: self.halt()

    def to_str(self):
        return self.__str__()

    def __str__(self):
        return "Type:%s, vj:%s, vk:%s, qj:%s, qk:%s, address:%s, cycles_left:%s, dest:%s, progress:%s, busy:%s" % (self.type_,self.vj,self.vk,self.qj,self.qk,self.address,self.cycles_left,self.dest,self.progress,self.busy)

