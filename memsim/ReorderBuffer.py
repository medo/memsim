class ReorderBuffer:
    def __init__(self, size):
        self.head = 0
        self.tail = 0
        self.buffer_ = [ ReorderBufferEntry(i) for i in range(size) ]

    def is_full(self):
        return not self.buffer_[self.tail].empty

    def get_current_empty(self):
        ret = self.buffer_[self.tail]
        self.tail += 1
        self.tail = self.tail % len(self.buffer_)
        return ret

    def get_head(self):
        return self.buffer_[self.head]

    def inc_head(self):
        self.head += 1
        self.head = self.head % len(self.buffer_)

    def get(self, id_):
        return self.buffer_[id_]

    def get_based_on_type(self, dest, type_):
        for i in self.buffer_:
            if i.type_ == type_ and i.dest == dest:
                return i

    def __str__(self):
        return "\n".join([ i.to_str() for i in self.buffer_ ])

class ReorderBufferEntry:
    def __init__(self, id_):
        self.id_ = id_
        self.clear()

    def clear(self):
        self.type_ = -1
        self.dest = -1
        self.value = 0
        self.ready = False
        self.empty = True

    def is_ready(self):
        return self.ready

    def set_ready(self, value):
        self.ready = value

    def get_id(self):
        return self.id_

    def set_empty(self, value):
        self.empty = value

    def to_str(self):
        return "Type:%s, dest:%s, value:%s, ready:%s, empty:%s" % (self.type_,self.dest,self.value,self.ready,self.empty)
