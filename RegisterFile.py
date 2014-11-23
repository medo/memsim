class RegisterFile:
    
    def __init__(self, size):
        self.data = [0 for i in range(size)]

    def get(self, idx):
        return self.data[idx]

    def set(self, idx, value):
        self.data[idx] = value
