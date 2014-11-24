from memsim import *
class Processor:

    NUMBER_OF_REGISTERS = 8
    MASK = 0xFFFF

    def __init__(self, data_store, instruction_store, start_address):
        self.data_store = data_store
        self.instruction_store = instruction_store
        self.cycles = 0
        self.busy_for = 0
        self.instruction_read = False
        self.instruction_ready_for_execution = False
        self.busy_execute = 0
        self.register_file = RegisterFile(NUMBER_OF_REGISTERS)
        self.pc = start_address
        self.current_instruction = None

    def progress(self):
        self.cycles += 1
        if not self.instruction_read:
            self.current_instruction = InstructionParser.parse(instruction_store.get(self.pc))
        #if busy_for == 0:
        #if self.current_instruction.type_ == InstructionType.load or self.current_instruction.type_ == InstructionType.store:


    def execute_instruction(self, instruction):
        {
            InstructionType.load : load(instruction.reg_a, instruction.reg_b, instruction.imm) ,
            InstructionType.store: store(instruction.reg_a, instruction.reg_b, instruction.imm),
            InstructionType.jump: jump(instruction.reg_a, instruction.imm),
            InstructionType.branch_if_equal: branch_if_equal(instruction.reg_a, instruction.reg_b, instruction.imm),
            InstructionType.jump_and_link: jump_and_link(instruction.reg_a, instruction.reg_b),
            InstructionType.return_: return_(instruction.reg_a),
            InstructionType.add: add(instruction.reg_a, instruction.reg_b, instruction.reg_c),
            InstructionType.subtract: subtract(instruction.reg_a, instruction.reg_b, instruction.reg_c),
            InstructionType.add_immediate: add_immediate(instruction.reg_a, instruction.reg_b, instruction.imm),
            InstructionType.nand: nand(instruction.reg_a, instruction.reg_b, instruction.reg_c),
            InstructionType.multiply: multiply(instruction.reg_a, instruction.reg_b, instruction.reg_c)
        }[instruction.type_]

    def load(self, destination, base_address_register, offset):
        base_address = self.register_file.get(base_address_register)
        data = self.data_store.get_address(base_address + offset)
        self.register_file.set(destination, data)

    def store(self, source, base_address_register, offset):
        base_address = self.register_file.get(base_address_register)
        s = self.register_file.get(source)
        self.data_store.write_in_address(base_address + offset, s)

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
        self.register_file.set(destination, (s1 + s2) & MASK)

    def subtract(self, destination, source1, source2):
        s1 = self.register_file.get(source1)
        s2 = self.register_file.get(source2)
        self.register_file.set(destination, (s1 - s2) & MASK)

    def add_immediate(self, destination, source1, value):
        s1 = self.register_file.get(source1)
        self.register_file.set(destination, (s1 + value) & MASK)

    def nand(self, destination, source1, source2):
        s1 = self.register_file.get(source1)
        s2 = self.register_file.get(source2)
        self.register_file.set(destination, (~(s1 & s2) & MASK))
    
    def multiply(self, destination, source1, source2):
        res = 0
        s1 = self.register_file.get(source1)
        s2 = self.register_file.get(source2)
        while s2 != 0:
            res += s1
            res &= MASK
            s2 -= 1
        self.register_file.set(destination, res)
        

