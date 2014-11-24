from BaseMemory import BaseMemory

class Cache(BaseMemory):

    '''
    cache_size in Bytes
    line_size in Bytes
    '''

    def __init__(self, cache_size, line_size, associativity_level, write_hit_policy, write_miss_policy, hit_cycles, miss_cycles, parent_memory=None):

        self.parent_memory = parent_memory
        self.__highest_address = cache_size / line_size
        self.__associaticity_level = associativity_level
        self.__entry_count = 0
        buckets = (cache_size / line_size) / associativity_level
        self.__bucket = [[{'valid': 0}] * associativity_level] * buckets

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
        tag = address / self.__associaticity_level
        bucket_index = address % self.__associaticity_level
        found = False
        for entry in self.__bucket[bucket_index]:
            if entry['valid'] == 1 and entry['tag'] == tag:
                entry['accessed_at'] = self.__entry_count
                self.__entry_count += 1
                found = True

        if not found:
            line = self.parent_memory.get_line(address)
            self.__cache(address, line)

    def __cache(self, address, line):
        pass


m = Cache(1024 * 1024, 1, 10, 10, 10, 10, 10, -1)
c = Cache(1024, 1, 10, 10, 10, 10, 10, m)
print c.get_address(1)
