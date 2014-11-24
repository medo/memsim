from BaseMemory import BaseMemory

class Cache(BaseMemory):

    '''
    cache_size in Bytes
    line_size in Bytes
    '''

    def __init__(self, cache_size, line_size, associativity_level, write_hit_policy, write_miss_policy, hit_cycles, miss_cycles, parent_memory=None):

        self.parent_memory = parent_memory
        self.__highest_address = cache_size / line_size
        self.__memory = {}
        self.__valid  = {}

    def get_address(self, address):
        pass

    def write_in_address(self, address, value):
        pass

    def get_misses(self):
        pass

    def get_hits(self):
        pass

    def caclculate_cycles(self, address, is_read):
        pass

    def get_line(self, address):

        if address < self.__highest_line_address:
            if self.__valid.get(address ,False):
                return self.__memory[address]
            elif self.parent_memroy:
                data = self.parM
                ent_memory.get_line(address)
                self.__cache(address, data)
                return data

            return None

    def __cache(self, address, data):
        self.__memory[address] = data
        self.__memory[address] = True


m = Cache(1024 * 1024, 1, 10, 10, 10, 10, 10, -1)
c = Cache(1024, 1, 10, 10, 10, 10, 10, m)
print c.get_address(1)
