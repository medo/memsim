from BaseMemory import BaseMemory

class Cache(BaseMemory):

    '''
    cache_size in Bytes
    line_size is the number of words
    '''

    def __init__(self, cache_size, line_size, associativity_level, write_hit_policy, write_miss_policy, hit_cycles, miss_cycles, parent_memory=None):

        self.parent_memory = parent_memory
        self.__highest_address = cache_size / line_size
        self.__associaticity_level = associativity_level
        self.__entry_count = 0
        self.__hit_cycles = hit_cycles
        self.__miss_cycles = miss_cycles
        self.__line_size = line_size
        buckets = (cache_size / line_size) / associativity_level
        self.__bucket = [None] * buckets
        for i in range(0, buckets):
            tmp = [None] * associativity_level
            for j in range(0, associativity_level):
                tmp[j] = {'valid': 0}
            self.__bucket[i] = tmp

    def get_address(self, address):
        word = address / 2
        line = self.get_line(word / self.__line_size)
        cycles = 0
        return [cycles, line[address % self.__line_size]]

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
            if entry != None and entry['valid'] == 1 and entry['tag'] == tag:
                entry['accessed_at'] = self.__entry_count
                self.__entry_count += 1
                print "Cache hit"
                return [self.__hit_cycles, entry['data']]


        print "Cache miss"
        result = self.parent_memory.get_line(address)
        self.__cache(address, result[1])
        return [result[0] + self.__miss_cycles, result[1]]

    def __cache(self, address, data, dirty=0):
        bucket_index = address % self.__associaticity_level
        last_accessed = {'accessed_at': 99999999999}
        for entry in self.__bucket[bucket_index]:
            if entry['valid'] == 0:
                last_accessed = entry
                break
            else:
                last_accessed = entry if entry['accessed_at'] < last_accessed['accessed_at'] else last_accessed

        last_accessed['valid'] = 1
        last_accessed['data'] = data
        last_accessed['accessed_at'] = self.__entry_count
        self.__entry_count += 1
        last_accessed['tag'] = address / self.__associaticity_level
        last_accessed['dirty'] = dirty




