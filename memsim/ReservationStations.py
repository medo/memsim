from InstructionProgress import InstructionProgress
class ReservationStations:
    def __init__(self, names, cycles):
        for i in cycles.keys():
            self.entries[i] = []
        for i in names:
            self.entries[i].append(ReservationStationEntry(i, cycles[i]))

    def can_hold(self, type_):
        self.get(type_) != -1

    def get(self, type_):
        for i in range(len(self.entries[type_])):
            if not self.entries[type_][i].busy:
                return i
        return -1
    
class ReservationStationEntry:
    def __init__(self, type_, cycles):
        self.type_ = type_
        self.cycles = cycles
        self.clear()

    def clear(self):
        self.busy = False
        self.op = ""
        self.vj = 0
        self.vk = 0
        self.qj = 0
        self.qk = 0
        self.address = -1
        self.cycles_left = 0
        self.progress = 0
        self.first_load = True
        self.dest = 0

    def start(self):
        self.cycles_left = cycles

    def progress(self):
        if self.cycles_left > 0:
            self.cycles_left -= 1
    
    def finished(self):
        return self.cycles_left == 0

