class Instruction:
    
    def __init__(self, type_):
        self.type_ = type_
        self.reg_a = -1
        self.reg_b = -1
        self.reg_c = -1
        self.imm = -1
    
    def set_reg_a(self, reg_a):
        self.reg_a = reg_a

    def set_reg_b(self, reg_b):
        self.reg_b = reg_b

    def set_reg_c(self, reg_c):
        self.reg_c = reg_c

    def set_imm(self, imm):
        self.imm = imm
