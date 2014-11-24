import re
from InstructionType import InstructionType
from Instruction import Instruction
class InstructionParser:
    
    @staticmethod
    def parse(line):
        reg_a = -1
        reg_b = -1
        reg_c = -1
        imm = -1
        type_ = ""

        if re.match("(LW|SW),([^, ]+),([^, ]+),([^, ]+)", line):
            m = re.match("(LW|SW),([^, ]+),([^, ]+),([^, ]+)", line)
            type_ = InstructionParser.get_type(m.group(1))
            reg_a = int(m.group(2))
            reg_b = int(m.group(3))
            imm = int(m.group(4))
        elif re.match("(JMP),([^, ]+),([^, ]+)",line):
            m = re.match("(JMP),([^, ]+),([^, ]+)",line)
            type_ = InstructionParser.get_type(m.group(1))
            reg_a = int(m.group(2))
            imm = int(m.group(3))
        elif re.match("(BEQ|ADDI),([^, ]+),([^, ]+),([^, ]+)",line):
            m = re.match("(BEQ|ADDI),([^, ]+),([^, ]+),([^, ]+)",line)
            type_ = InstructionParser.get_type(m.group(1))
            reg_a = int(m.group(2))
            reg_b = int(m.group(3))
            imm = int(m.group(4))
        elif re.match("(JALR),([^, ]+),([^, ]+)",line):
            m = re.match("(JALR),([^, ]+),([^, ]+)",line)
            type_ = InstructionParser.get_type(m.group(1))
            reg_a = int(m.group(2))
            reg_b = int(m.group(3))
        elif re.match("(RET),([^, ]+)",line):
            m = re.match("(RET),([^, ]+)",line)
            type_ = InstructionParser.get_type(m.group(1))
            reg_a = int(m.group(2))
        elif re.match("(ADD|SUB|ADDI|NAND|MUL),([^, ]+),([^, ]+),([^, ]+)",line):
            m = re.match("(ADD|SUB|ADDI|NAND|MUL),([^, ]+),([^, ]+),([^, ]+)",line)
            type_ = InstructionParser.get_type(m.group(1))
            reg_a = int(m.group(2))
            reg_b = int(m.group(3))
            reg_c = int(m.group(4))
        inst = Instruction(type_)
        inst.set_reg_a(reg_a)
        inst.set_reg_b(reg_b)
        inst.set_reg_c(reg_c)
        inst.set_imm(imm)
        return inst
    
    @staticmethod
    def get_type(command):
        return {
            "LW": InstructionType.load,
            "SW": InstructionType.store,
            "JMP": InstructionType.jump,
            "BEQ": InstructionType.branch_if_equal,
            "JALR": InstructionType.jump_and_link,
            "RET": InstructionType.return_,
            "ADD": InstructionType.add,
            "SUB": InstructionType.subtract,
            "ADDI": InstructionType.add_immediate,
            "NAND": InstructionType.nand,
            "MUL": InstructionType.multiply
        }[command]
