class ReorderBuffer:
    def __init__(self, size):
        self.head = 0
        self.tail = 0
        self.buffer_ = [ ReorderBufferEntry(i) for i in range(size) ]

    def is_full(self):
        return not self.buffer_[self.tail].empty

    def get_current_empty(self):
        self.tail += 1
        return self.buffer_[self.tail]

    def get(self, id_):
        return self.buffer_[id_]

    def get_based_on_type(self, dest, type_):
        for i in self.buffer_:
            if i.type_ == type_ and i.dest == dest:
                return i

class ReorderBufferEntry:
    def __init__(self, id_):
        self.id_ = id_
        self.clear()

    def clear(self):
        self.type_ = type
        self.dest = -1
        self.value = 0
        self.ready = False
        self.empty = True

    def ready(self):
        return self.ready

    def set_ready(self, value):
        self.ready = value

    def get_id(self):
        return self.id_
