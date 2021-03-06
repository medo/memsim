from InstructionType import InstructionType
from FunctionalUnit import FunctionalUnit
from RegisterFile import RegisterFile
from InstructionParser import InstructionParser
from ReservationStations import ReservationStations
from RegisterStat import RegisterStat
from InstructionProgress import InstructionProgress
from ReorderBuffer import ReorderBuffer
import pdb
class Processor:

    NUMBER_OF_REGISTERS = 8

    def __init__(self, data_store, instruction_store, start_address, number_of_ways, reservation_stations_types, reservation_station_cycles, reorder_buffer_size):
        self.data_store = data_store
        self.instruction_store = instruction_store
        self.cycles = 0
        self.stopped = False
        self.register_file = RegisterFile(self.NUMBER_OF_REGISTERS)
        self.pc = start_address
        self.start_address = start_address
        self.instructions_count = 0
        self.number_of_ways = number_of_ways
        self.register_stat = RegisterStat(self.NUMBER_OF_REGISTERS)
        self.reorder_buffer = ReorderBuffer(reorder_buffer_size)
        self.reservation_stations = ReservationStations(reservation_stations_types, reservation_station_cycles, self.reorder_buffer, self)
        self.read_more_instructions = True
        self.mispredictions = 0
        self.predections = 0

    def progress(self):
        #pdb.set_trace()
        if self.stopped: return False
        self.cycles += 1
        common_data_bus_empty = True
        can_commit = True
        any_change = False
        # Update Reservation Stations
        for i in self.reservation_stations.entries.keys():
            for j in range(len(self.reservation_stations.entries[i])):
                reservation_station = self.reservation_stations.entries[i][j]
                if reservation_station.busy:
                    any_change = True
                    if reservation_station.progress == InstructionProgress.issue:
                        if reservation_station.type_ in [ FunctionalUnit.load, FunctionalUnit.store ]:
                            if reservation_station.qj == -1: # Ready to calculate address
                                reservation_station.address += reservation_station.vj
                                reservation_station.progress = InstructionProgress.execute
                                reservation_station.start()
                        elif reservation_station.operation in [InstructionType.return_, InstructionType.jump_and_link ]:
                            if reservation_station.qj == -1: # Ready to calculate address
                                reservation_station.address = reservation_station.vj
                                reservation_station.progress = InstructionProgress.execute
                                reservation_station.start()
                        elif reservation_station.operation == InstructionType.jump:
                            if reservation_station.qj == -1: # Ready to calculate address
                                reservation_station.address += reservation_station.pc + reservation_station.vj + 2
                                reservation_station.progress = InstructionProgress.execute
                                reservation_station.start()
                        elif reservation_station.qj == -1 and reservation_station.qk == -1:
                            if reservation_station.operation == InstructionType.branch_if_equal:
                                self.predections += 1
                                if reservation_station.address < 0:
                                    reservation_station.predicted_taken = True
                                    self.reorder_buffer.clear_after((reservation_station.get_reorder_buffer().get_id() + 1) % self.reorder_buffer.get_size())
                                    self.set_pc(self.pc + 2 + reservation_station.address)
                                else:
                                    reservation_station.predicted_taken = False
                            reservation_station.progress = InstructionProgress.execute
                            reservation_station.start()
                            reservation_station.progress_single_cycle()
                    elif reservation_station.progress == InstructionProgress.execute:
                        reservation_station.progress_single_cycle()
                        if reservation_station.finished():
                            reservation_station.execute()
                            reservation_station.progress = InstructionProgress.write
                            if reservation_station.operation == InstructionType.branch_if_equal:
                                if reservation_station.result == 0 ^ reservation_station.predicted_taken:
                                    self.inc_mispredictions()
                                    self.reorder_buffer.clear_after(reservation_station.get_reorder_buffer().get_id())
                                    self.set_pc(reservation_station.pc + 2)
                                else:
                                    reservation_station.get_reorder_buffer().clear()
                                    reservation_station.clear()
                    elif reservation_station.progress == InstructionProgress.write:
                        if common_data_bus_empty:
                            common_data_bus_empty = False
                            b = reservation_station.get_reorder_buffer().get_id()
                            for q in self.reservation_stations.entries.keys():
                                for w in range(len(self.reservation_stations.entries[q])):
                                    tmp = self.reservation_stations.entries[q][w]
                                    if tmp.qj == b:
                                        tmp.vj = reservation_station.result
                                        tmp.qj = -1
                            for q in self.reservation_stations.entries.keys():
                                for w in range(len(self.reservation_stations.entries[q])):
                                    tmp = self.reservation_stations.entries[q][w]
                                    if tmp.qk == b:
                                        tmp.vk = reservation_station.result
                                        tmp.qk = -1
                            rob = reservation_station.get_reorder_buffer()
                            rob.value = reservation_station.result
                            rob.set_ready(True)
                            if self.reorder_buffer.get_head() is reservation_station.get_reorder_buffer():
                                can_commit = False
                            reservation_station.clear()

        if self.reorder_buffer.get_head().is_ready() and can_commit:
            any_change = True
            rob = self.reorder_buffer.get_head()
            d = rob.dest
            self.register_file.set(d, rob.value)
            rob.clear()
            if self.register_stat.get(d) == rob.get_id():
                self.register_stat.clear(d)
            self.reorder_buffer.inc_head()
        
        #pdb.set_trace()
        # Issue new instructions
        if self.read_more_instructions:
            any_change = True
            for i in range(self.number_of_ways):
                inst = self.instruction_store.get_address(self.pc)[1]
                instruction = InstructionParser.parse(inst)
                if instruction.type_ == InstructionType.halt:
                    self.read_more_instructions = False
                    break
                if self.can_issue(instruction):
                    self.instructions_count += 1
                    print "\nIssuing : " + inst
                    self.issue(instruction)
                    self.pc += 2
                else:
                    break

        print "\nReservation Stations :"
        print self.reservation_stations

        print "Reorder Buffers :"
        print self.reorder_buffer

        print "\nRegister Status :"
        print self.register_stat


        if not any_change:
            self.stopped = True
            print ""
            print "Data Cache : "
            self.data_store.print_logs(0)
            print ""
            print "Instructions Count : " + str(self.instructions_count)
            print ""
            print "Number of mispredictions : " + str(self.mispredictions)
            print ""
            print "Number of predictions : " + str(self.predections)
        

    def execute_all(self): 
        while self.progress() != False:
            pass

    def can_issue(self, instruction):
        return self.reservation_stations.can_hold(self.get_functional_unit(instruction)) and not self.reorder_buffer.is_full()

    def issue(self, instruction):
        functional_unit = self.get_functional_unit(instruction)
        current_rob = self.reorder_buffer.get_current_empty()
        current_reservation_station = self.reservation_stations.get(functional_unit)
        if self.register_stat.busy(instruction.rs):
            h = self.register_stat.get(instruction.rs)
            if self.reorder_buffer.get(h).is_ready():
                current_reservation_station.vj = self.reorder_buffer.get(h).value
                current_reservation_station.qj = -1
            else:
                current_reservation_station.qj = h
        else:
            current_reservation_station.vj = self.register_file.get(instruction.rs)
            current_reservation_station.qj = -1

        current_reservation_station.set_busy(True)
        current_reservation_station.dest = current_rob.get_id()
        current_reservation_station.operation = instruction.type_
        current_reservation_station.pc = self.get_pc()
        current_rob.type_ = functional_unit
        current_rob.dest = instruction.rd
        current_rob.set_ready(False)
        current_rob.set_empty(False)
        current_rob.reservation_station = current_reservation_station

        if functional_unit in [ FunctionalUnit.add, FunctionalUnit.mult, FunctionalUnit.logical, FunctionalUnit.store ] or instruction.type_ == InstructionType.jump_and_link:
            if current_reservation_station.operation == InstructionType.add_immediate:
                current_reservation_station.vk = instruction.imm
                current_reservation_station.qk = -1
            elif current_reservation_station.operation == InstructionType.branch_if_equal:
                current_reservation_station.address = instruction.imm
            else:
                if self.register_stat.busy(instruction.rt):
                    h = self.register_stat.get(instruction.rt)
                    if self.reorder_buffer.get(h).is_ready():
                        current_reservation_station.vk = self.reorder_buffer.get(h).value
                        current_reservation_station.qk = -1
                    else:
                        current_reservation_station.qk = h
                else:
                    current_reservation_station.vk = self.register_file.get(instruction.rt)
                    current_reservation_station.qk = -1

        if functional_unit in [ FunctionalUnit.load ] :
            current_reservation_station.address = instruction.imm
            self.register_stat.set(instruction.rd, current_rob.get_id())
        elif functional_unit in [ FunctionalUnit.store ]:
            current_reservation_station.address = instruction.imm
        elif functional_unit in [ FunctionalUnit.branches ]:
            if instruction.type_ == InstructionType.jump:
                current_reservation_station.address = instruction.imm
        elif functional_unit in [ FunctionalUnit.add, FunctionalUnit.mult, FunctionalUnit.logical ] and current_reservation_station.operation != InstructionType.branch_if_equal:
            self.register_stat.set(instruction.rd, current_rob.get_id())

        current_reservation_station.progress = InstructionProgress.issue

    def execute_instruction(self, instruction):
        if instruction.type_ == InstructionType.store: self.store(instruction.reg_a, instruction.reg_b, instruction.imm)
        if instruction.type_ == InstructionType.jump: self.jump(instruction.reg_a, instruction.imm)
        if instruction.type_ == InstructionType.branch_if_equal: self.branch_if_equal(instruction.reg_a, instruction.reg_b, instruction.imm)
        if instruction.type_ == InstructionType.jump_and_link: self.jump_and_link(instruction.reg_a, instruction.reg_b)
        if instruction.type_ == InstructionType.return_: self.return_(instruction.reg_a)

    def get_functional_unit(self, instruction):
        if instruction.type_ == InstructionType.load : return FunctionalUnit.load
        if instruction.type_ == InstructionType.store: return FunctionalUnit.store
        if instruction.type_ == InstructionType.jump: return FunctionalUnit.branches
        if instruction.type_ == InstructionType.branch_if_equal: return FunctionalUnit.add
        if instruction.type_ == InstructionType.jump_and_link: return FunctionalUnit.branches
        if instruction.type_ == InstructionType.return_: return FunctionalUnit.branches
        if instruction.type_ == InstructionType.add: return FunctionalUnit.add
        if instruction.type_ == InstructionType.subtract: return FunctionalUnit.add
        if instruction.type_ == InstructionType.add_immediate: return FunctionalUnit.add
        if instruction.type_ == InstructionType.nand: return FunctionalUnit.logical
        if instruction.type_ == InstructionType.multiply: return FunctionalUnit.mult
        if instruction.type_ == InstructionType.halt: return FunctionalUnit.halt

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
        s1 = self.register_file.get(address_register)
        self.pc = s1

    def return_(self, source):
        self.pc = self.register_file.get(source)

    def get_instruction_number(self):
        return (self.pc - self.start_address) / 2

    def get_pc(self):
        return self.pc

    def set_pc(self, value):
        self.pc = value

    def inc_mispredictions(self):
        self.mispredictions += 1
