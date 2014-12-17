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
        self.hits = 0
        self.misses = 0


    def get_address(self, address, no_effect=False):
        if not no_effect:
            self.hits += 1
        return (self.__latency, self.memory[address])


    def write_in_address(self, address, value, no_effect=False):
        if not no_effect:
            self.memory[address] = value
            print self.memory
            self.hits += 1
        return self.__latency

    def get_misses(self):
        return self.misses

    def get_hits(self):
        return self.hits
    
    def print_logs(self, level):
        print "Main Memory, hits : " + str(self.get_hits()) + " -- misses : " + str(self.get_misses())

    def caclculate_cycles(self, address, is_read):
        pass

    def get_line(self, address, no_effect=False):
        result = [None] * self.__line_size
        j = 0
        address *= self.__line_size * 2
        print address
        print range(address, address + self.__line_size * 2, 2)
        for i in range(address, address + self.__line_size * 2, 2):
            result[j] = self.memory.get(i, 0)
            j += 1
        return (self.__latency, result)

    def write_block(self, line_address, data, no_effect=False):
        j = 0
        if not no_effect:
            for i in range(line_address, line_address + self.__line_size * 2, 2):
                self.memory[i] = data[j]
                j += 1
        return self.__latency

    def get_memory(self):
        return self.memory
