from BaseMemory import BaseMemory

class MainMemory(BaseMemory):

    '''
    cache_size in Bytes
    line_size is the number words in a block
    '''

    def __init__(self, memory_size, latency, line_size):
        self.__memory_size = memory_size
        self.memory = {}
        self.__latency = latency
        self.__line_size = line_size
        self.memory[30] = 15
        self.hits = 0
        self.misses = 0


    def get_address(self, address):
        self.hits += 1
        return (self.__latency, self.memory[address])

    def write_in_address(self, address, value):
        self.hits += 1
        self.memory[address] = value
        return self.__latency

    def get_misses(self):
        return self.misses

    def get_hits(self):
        return self.hits
    
    def print_logs(self, level):
        print "Main Memory, hits : " + str(self.get_hits()) + " -- misses : " + str(self.get_misses())

    def caclculate_cycles(self, address, is_read):
        pass

    def get_line(self, address):
        result = [None] * self.__line_size
        j = 0
        print address
        for i in range(address, address + self.__line_size):
            result[j] = self.memory.get(i * 2, 0)
            j += 1
        return (self.__latency, result)

    def write_block(self, line_address, data):
        j = 0
        for i in range(line_address, line_address + self.__line_size * 2, 2):
            self.memory[i] = data[j]
            j += 1
        return self.__latency

    def get_memory(self):
        return self.memory
