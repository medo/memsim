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


    def get_address(self, address):
        return (self.__latency, self.memory[address])

    def write_in_address(self, address, value):
        self.memory[address] = value
        return self.__latency

    def get_misses(self):
        pass

    def get_hits(self):
        pass

    def caclculate_cycles(self, address, is_read):
        pass

    def get_line(self, address):
        result = [None] * self.__line_size
        j = 0
        for i in range(address, address + self.__line_size * 2, 2):
            result[j] = self.memory.get(i, 0)
            j += 1
        return (self.__latency, result)

    def write_block(self, line_address, data):
        j = 0
        for i in range(line_address, line_address + self.__line_size * 2, 2):
            self.memory[i] = data[j]
            j += 1
        return self.__latency
