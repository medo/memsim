from InstructionProgress import InstructionProgress
class ReservationStations:
    def __init__(self, names, cycles):
        self.entries = {}
        for i in cycles.keys():
            self.entries[i] = []
        for i in names:
            self.entries[i].append(ReservationStationEntry(i, cycles[i]))

    def can_hold(self, type_):
        return self.get(type_) != -1

    def get(self, type_):
        for i in range(len(self.entries[type_])):
            if not self.entries[type_][i].busy:
                return self.entries[type_][i]
        return -1

    def __str__(self):
        ret = ""
        for i in self.entries.keys():
            for j in range(len(self.entries[i])):
                ret += self.entries[i][j].to_str() + "\n"
        return ret

    
class ReservationStationEntry:
    def __init__(self, type_, cycles):
        self.type_ = type_
        self.cycles = cycles
        self.clear()

    def clear(self):
        self.busy = False
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
        self.cycles_left = self.cycles

    def progress_single_cycle(self):
        if self.cycles_left > 0:
            self.cycles_left -= 1
    
    def finished(self):
        return self.cycles_left == 0

    def set_busy(self, value):
        self.busy = value

    def busy(self):
        return self.busy
    
    def to_str(self):
        return self.__str__()

    def __str__(self):
        return "Type:%s, vj:%s, vk:%s, qj:%s, qk:%s, address:%s, cycles_left:%s, dest:%s, progress:%s" % (self.type_,self.vj,self.vk,self.qj,self.qk,self.address,self.cycles_left,self.dest,self.progress)

