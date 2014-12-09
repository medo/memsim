class RegisterStat:
    def __init__(self, number_of_registers):
        self.registers = [ -1 for i in range(number_of_registers) ]

    def get(self, register):
        return self.registers[register]

    def set(self, register, value):
        self.registers[register] = value

    def busy(self, register):
        return self.registers[register] != -1

