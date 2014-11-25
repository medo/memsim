import re
class Assembler:
    
    @staticmethod
    def assemble(program, start_address):
        program = program.split("\n")
        labels = {}
        curr_address = start_address
        supported_instructions = [ "LW", "SW", "JMP", "BEQ", "JALR", "RET", "ADD", "SUB", "ADDI", "NAND", "MUL", "HALT" ]
        new_program = []
        for line in program:
            line = re.sub(", +",",",line)
            line = re.sub(" +$","",line)
            line = re.sub(" +",",",line)
            l = line.split(",")
            _l = l[0]
            if _l not in supported_instructions:
                labels[_l] = curr_address
                new_program.append(",".join(l[1:]))
            else:
                new_program.append(",".join(l))
            curr_address += 2
        curr_address = start_address
        _new_program = []
        for line in new_program:
            l = line.split(",")
            if l[0] == "BEQ":
                if l[-1] in labels:
                    l[-1] = str(labels[l[-1]] - curr_address - 2)
            _new_program.append(",".join(l))
            curr_address += 2
        return "\n".join(_new_program)

