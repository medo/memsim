from InstructionProgress import InstructionProgress
from InstructionType import InstructionType
from FunctionalUnit import FunctionalUnit

class ReservationStations:
    def __init__(self, names, cycles, reorder_buffers, processor):
        self.reorder_buffers = reorder_buffers
        self.processor = processor
        self.entries = {}
        for i in cycles.keys():
            self.entries[i] = []
        for i in names:
            self.entries[i].append(ReservationStationEntry(i, cycles[i], self.reorder_buffers, processor))

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

    def __init__(self, type_, cycles, reorder_buffers, processor):
        self.type_ = type_
        self.cycles = cycles
        self.reorder_buffers = reorder_buffers
        self.processor = processor
        self.clear()

    def clear(self):
        self.busy = False
        self.vj = -1
        self.vk = -1
        self.qj = -1
        self.qk = -1
        self.address = -1
        self.cycles_left = 0
        self.progress = 0
        self.first_load = True
        self.dest = -1
        self.operation = -1
        self.result = 0
        self.pc = 0
        self.predicted_taken = False

    def start(self):
        if self.operation == InstructionType.load:
            self.cycles_left =  self.processor.data_store.get_address(self.address,True)[0]
        elif self.type_ == FunctionalUnit.branches:
            self.cycles_left = 1
        else:
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
        self.vj = int(self.vj)
        self.vk = int(self.vk)
        current_buffer = self.get_reorder_buffer()
        if self.operation == InstructionType.load :
            self.result = self.processor.data_store.get_address(self.address,False)[1]
        #if self.operation == InstructionType.store: self.store(instruction.reg_a, instruction.reg_b, instruction.imm)
        if self.operation == InstructionType.jump:
            self.processor.set_pc(self.address)
            self.reorder_buffers.clear_after(self.get_reorder_buffer().get_id())
        if self.operation == InstructionType.branch_if_equal:
            self.result = int(self.vj) - int(self.vk)
        #if self.operation == InstructionType.jump_and_link: self.jump_and_link(instruction.reg_a, instruction.reg_b)
        if self.operation == InstructionType.return_:
            self.processor.set_pc(self.address)
            self.reorder_buffers.clear_after(get_reorder_buffer().get_id())
        if self.operation == InstructionType.add: self.result = (self.vj + self.vk) & self.MASK
        if self.operation == InstructionType.subtract: self.result = (self.vj - self.vk) & self.MASK
        if self.operation == InstructionType.add_immediate: self.result = (self.vj + self.vk) & self.MASK
        if self.operation == InstructionType.nand: self.result = (~(self.vj & self.vk) & self.MASK)
        if self.operation == InstructionType.multiply: self.result = (self.vj * self.vk) & self.MASK

    def to_str(self):
        return self.__str__()

    def __str__(self):
        return "Type:%s, vj:%s, vk:%s, qj:%s, qk:%s, address:%s, cycles_left:%s, dest:%s, progress:%s, busy:%s" % (self.type_,self.vj,self.vk,self.qj,self.qk,self.address,self.cycles_left,self.dest,self.progress,self.busy)

