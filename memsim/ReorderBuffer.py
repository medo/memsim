class ReorderBuffer:
    def __init__(self, size):
        self.head = 0
        self.tail = 0
        self.buffer_ = [ ReorderBufferEntry() for i in range(size) ]

    def is_full(self):
        return not self.buffer_[self.tail].empty

    def get_current_empty(self):
        return self.buffer_[self.head]

    def get(self, id_):
        return self.buffer_[id_]

class ReorderBufferEntry:
    def __init__(self):
        clear()

    def clear(self):
        self.type_ = type
        self.dest = dest
        self.value = value
        self.ready = False
        self.empty = True
