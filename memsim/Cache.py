from BaseMemory import BaseMemory
from WritePolicy import WritePolicy
from InstructionParser import InstructionParser

class Cache(BaseMemory):

    '''
    cache_size in Bytes
    line_size is the number of words
    '''

    def __init__(self, cache_size, line_size, associativity_level, write_hit_policy, write_miss_policy, hit_cycles, parent_memory=None):

        self.__parent_memory = parent_memory
        self.__hits = 0
        self.__misses = 0
        self.__highest_address = cache_size / line_size
        self.__associaticity_level = associativity_level
        self.__entry_count = 0
        self.__hit_cycles = hit_cycles
        self.__write_miss_policy = write_miss_policy
        self.__write_hit_policy = write_hit_policy
        self.__line_size = line_size
        self.__cache_entries = cache_size/(2*line_size)
        buckets = (cache_size / (2*line_size)) / associativity_level
        self.__bucket = [None] * buckets
        for i in range(0, buckets):
            tmp = [None] * associativity_level
            for j in range(0, associativity_level):
                tmp[j] = {'valid': 0}
            self.__bucket[i] = tmp

    def get_address(self, address, no_effect=False):
        word = address / 2
        result = self.get_line(word, no_effect)
        print result[1]
        return [result[0], result[1][word % self.__line_size]]

    def write_block(self, line_address, data, no_effect=False):
        tag = line_address / self.__associaticity_level
        bucket_index = line_address % self.__associaticity_level
        cycles = self.__hit_cycles

        for entry in self.__bucket[bucket_index]:
            if entry['valid'] == 1 and entry['tag'] == tag:
                if not no_effect:
                    entry['accessed_at'] = self.__entry_count
                    self.__entry_count += 1
                    self.__hits += 1
                    entry['data'] = data
                if self.__write_hit_policy == WritePolicy.write_through:
                    return cycles + self.__parent_memory.write_block(line_address, data, no_effect)
                elif self.__write_hit_policy == WritePolicy.write_back:
                    if not no_effect:
                        entry['dirty'] = 1
                    return cycles

        if self.__write_miss_policy == WritePolicy.write_allocate:
            cycles += self.__parent_memory.write_block(line_address, data, no_effect)
            self.__cache(line_address, data)
        elif self.__write_miss_policy == WritePolicy.write_around:
            self.__parent_memory.write_block(line_address, data, no_effect)



    def write_in_address(self, address, value, no_effect=False):
        word = address / 2
        index = address % self.__line_size
        address =  word / self.__line_size
        tag = address / (self.__cache_entries / self.__associaticity_level)
        bucket_index = address % (self.__cache_entries / self.__associaticity_level)
        found = False
        cycles = self.__hit_cycles
        for entry in self.__bucket[bucket_index]:
            if entry['valid'] == 1 and entry['tag'] == tag:
                if not no_effect:
                    entry['accessed_at'] = self.__entry_count
                    self.__entry_count += 1
                    self.__hits += 1

                    entry['data'][index] = value
                if self.__write_hit_policy == WritePolicy.write_through:
                    return cycles + self.__parent_memory.write_in_address(word * 2, value, no_effect)
                elif self.__write_hit_policy == WritePolicy.write_back:
                    if not no_effect:
                        entry['dirty'] = 1
                    return cycles

        print "gena ne write am miss -> " + str(self.__hit_cycles)
        if self.__write_miss_policy == WritePolicy.write_allocate:
            result = self.__parent_memory.get_line(word / self.__line_size, no_effect)
            print "-> " + str(result[1])
            result[1][word % self.__line_size] = value
            cycles += self.__cache(word / self.__line_size, result[1], no_effect)
            #self.__parent_memory.write_block(word / self.__line_size, result[1])
            cycles += result[0]
        elif self.__write_miss_policy == WritePolicy.write_around:
            cycles += self.__parent_memory.write_in_address(word * 2, value, no_effect)

        if not no_effect:
            self.__misses += 1
        result = self.__parent_memory.get_line(address, no_effect)
        self.__cache(address, result[1], no_effect)
        return cycles


    def get_misses(self):
        return self.__misses

    def get_hits(self):
        return self.__hits

    def caclculate_cycles(self, address, is_read):
        pass

    def get_line(self, address, no_effect=False):
        word = address
        address /= self.__line_size
        tag = address / (self.__cache_entries / self.__associaticity_level)
        bucket_index = address % (self.__cache_entries / self.__associaticity_level)
        found = False
        print self.__bucket
        for entry in self.__bucket[bucket_index]:
            if entry != None and entry['valid'] == 1 and entry['tag'] == tag:
                if not no_effect:
                    entry['accessed_at'] = self.__entry_count
                    self.__entry_count += 1
                    print "Cache hit"
                    self.__hits += 1
                return (self.__hit_cycles, entry['data'])


        print "Cache miss"
        if not no_effect:
            self.__misses += 1
        result = self.__parent_memory.get_line(word / self.__line_size, no_effect)
        cycles = self.__cache(address, result[1], no_effect)

        return (result[0] + cycles, result[1])

    def __cache(self, address, data, dirty=0, no_effect=False):
        bucket_index = address % (self.__cache_entries / self.__associaticity_level)
        last_accessed = {'accessed_at': 99999999999}
        for entry in self.__bucket[bucket_index]:
            if entry['valid'] == 0:
                last_accessed = entry
                break
            else:
                last_accessed = entry if entry['accessed_at'] < last_accessed['accessed_at'] else last_accessed

        cycles = self.__hit_cycles
        if last_accessed.get('dirty', 0) == 1:
            cycles += self.__parent_memory.write_block(address, last_accessed['data'], no_effect)
        if not no_effect:
            last_accessed['valid'] = 1
            last_accessed['data'] = data
            last_accessed['accessed_at'] = self.__entry_count
            self.__entry_count += 1
            last_accessed['tag'] = address / (self.__cache_entries / self.__associaticity_level)
            last_accessed['dirty'] = dirty
        return cycles

    def print_logs(self, level):
        print "L"+ str(level) +", hits : " + str(self.get_hits()) + " -- misses : " + str(self.get_misses())
        self.__parent_memory.print_logs(level+1)
