from BaseMemory import BaseMemory

class MainMemory(BaseMemory):

    '''
    cache_size in Bytes
    line_size in Bytes
    '''

    def __init__(self):
        pass

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
        return [100, "aho leil w 3ada"]


