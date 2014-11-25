from InstructionType import InstructionType
from RegisterFile import RegisterFile
from InstructionParser import InstructionParser
class Processor:

    NUMBER_OF_REGISTERS = 8
    MASK = 0xFFFF

    def __init__(self, data_store, instruction_store, start_address):
        self.data_store = data_store
        self.instruction_store = instruction_store
        self.cycles = 0
        self.busy_for = 0
        self.busy_for_2 = 0
        self.stopped = False
        self.reading = None
        self.pending = False
        self.register_file = RegisterFile(self.NUMBER_OF_REGISTERS)
        self.pc = start_address
        self.start_address = start_address
        self.instructions_count = 0
        self.current_instruction = None

    def progress(self):
        if self.stopped: return False
        self.cycles += 1
        if self.reading == None:
            self.reading = self.instruction_store.get_address(self.pc)
            self.busy_for += self.reading[0]
            if self.reading[1] in ["", 0, None]:
                self.cycles -=1
                self.stopped = True
                print ""
                print "Data Cache : "
                self.data_store.print_logs(0)
                print ""
                print "Instructions Cache : "
                self.instruction_store.print_logs(0)
                print ""
                print "Instructions Count : " + str(self.instructions_count)

                return False
            print "------> " + str(self.pc) + " " + str(self.reading)
        if self.current_instruction == None :
            if self.busy_for > 0:
                self.busy_for -= 1
            if self.busy_for == 0:
                self.current_instruction = InstructionParser.parse(self.reading[1])

        if self.current_instruction != None:
            if self.current_instruction.type_ not in [InstructionType.load, InstructionType.store]:
                self.reading = None
                self.busy_for = 0
                self.busy_for_2 = 0
                self.pc += 2
                self.execute_instruction(self.current_instruction)
                self.current_instruction = None
            else:
                if not self.pending:
                    self.pending = True
                    self.execute_instruction(self.current_instruction)
                else:
                    if self.busy_for > 0:
                        self.busy_for -= 1
                    if self.busy_for == 0:
                        self.reading = None
                        self.busy_for = 0
                        self.busy_for_2 = 0
                        self.pc += 2
                        self.current_instruction = None
                        self.pending = False
    def execute_all(self):
        while self.progress() != False:
            pass

    def execute_instruction(self, instruction):
        self.instructions_count += 1
        if instruction.type_ == InstructionType.load : self.load(instruction.reg_a, instruction.reg_b, instruction.imm)
        if instruction.type_ == InstructionType.store: self.store(instruction.reg_a, instruction.reg_b, instruction.imm)
        if instruction.type_ == InstructionType.jump: self.jump(instruction.reg_a, instruction.imm)
        if instruction.type_ == InstructionType.branch_if_equal: self.branch_if_equal(instruction.reg_a, instruction.reg_b, instruction.imm)
        if instruction.type_ == InstructionType.jump_and_link: self.jump_and_link(instruction.reg_a, instruction.reg_b)
        if instruction.type_ == InstructionType.return_: self.return_(instruction.reg_a)
        if instruction.type_ == InstructionType.add: self.add(instruction.reg_a, instruction.reg_b, instruction.reg_c)
        if instruction.type_ == InstructionType.subtract: self.subtract(instruction.reg_a, instruction.reg_b, instruction.reg_c)
        if instruction.type_ == InstructionType.add_immediate: self.add_immediate(instruction.reg_a, instruction.reg_b, instruction.imm)
        if instruction.type_ == InstructionType.nand: self.nand(instruction.reg_a, instruction.reg_b, instruction.reg_c)
        if instruction.type_ == InstructionType.multiply: self.multiply(instruction.reg_a, instruction.reg_b, instruction.reg_c)
        if instruction.type_ == InstructionType.halt: self.halt()

    def load(self, destination, base_address_register, offset):
        base_address = self.register_file.get(base_address_register)
        data = self.data_store.get_address(base_address + offset)
        self.busy_for += data[0]
        print "//////// " + str(data)
        self.register_file.set(destination, data[1])

    def store(self, source, base_address_register, offset):
        base_address = self.register_file.get(base_address_register)
        s = self.register_file.get(source)
        latency = self.data_store.write_in_address(base_address + offset, s)
        self.busy_for += latency

    def jump(self, base_address_register, offset):
        base_address = self.register_file.get(base_address_register)
        self.pc = self.pc + base_address + offset

    def branch_if_equal(self, source1, source2, address):
        s1 = self.register_file.get(source1)
        s2 = self.register_file.get(source2)
        if s1 == s2:
            self.pc = self.pc + address

    def jump_and_link(self, store_register, address_register):
        self.register_file.set(store_register, self.pc)
        self.pc = address_register

    def return_(self, source):
        self.pc = self.register_file.get(source)

    def add(self, destination, source1, source2):
        s1 = self.register_file.get(source1)
        s2 = self.register_file.get(source2)
        self.register_file.set(destination, (s1 + s2) & self.MASK)

    def subtract(self, destination, source1, source2):
        s1 = self.register_file.get(source1)
        s2 = self.register_file.get(source2)
        self.register_file.set(destination, (s1 - s2) & self.MASK)

    def add_immediate(self, destination, source1, value):
        s1 = self.register_file.get(source1)
        self.register_file.set(destination, (s1 + value) & self.MASK)

    def nand(self, destination, source1, source2):
        s1 = self.register_file.get(source1)
        s2 = self.register_file.get(source2)
        self.register_file.set(destination, (~(s1 & s2) & self.MASK))
    
    def multiply(self, destination, source1, source2):
        res = 0
        s1 = int(self.register_file.get(source1))
        s2 = self.register_file.get(source2)
        while s2 != 0:
            res += s1
            res &= self.MASK
            s2 -= 1
        self.register_file.set(destination, res)
    
    def halt(self):
        self.stopped = True

    def get_instruction_number(self):
        return (self.pc - self.start_address) / 2
