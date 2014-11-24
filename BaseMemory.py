from abc import ABCMeta, abstractmethod
class BaseMemory:
    __metaclass__ = ABCMeta
    
    @abstractmethod
    def get_address(self, address):
        pass

    @abstractmethod
    def write_in_address(self, address, value):
        pass

    @abstractmethod
    def get_misses(self):
        pass

    @abstractmethod
    def get_hits(self):
        pass

    @abstractmethod
    def caclculate_cycles(self, address, is_read):
        pass

    @abstractmethod
    def get_line(self, address):
        pass