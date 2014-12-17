from Tkinter import *
from MainMemory import MainMemory
from Cache import Cache
from Processor import Processor
from Assembler import Assembler
from FunctionalUnit import FunctionalUnit

class GUI:
    
    def execute(self):
        self.processor.execute_all()
        self.progress_button.config(state='disabled')
        self.execute_button.config(state='disabled')
        self.update()

    def progress(self):
        ret = self.processor.progress()
        if ret != False:
            self.update()
        else:
            self.progress_button.config(state='disabled')
            self.execute_button.config(state='disabled')

    def assemble(self):

        self.memory = MainMemory(64*1024, self.memory_access_time, self.cache_block_size)
        
        iprev = self.memory
        dprev = self.memory
        for i in reversed(range(self.cache_levels)):
            d = self.caches[i]
            iprev = Cache(d[0],d[1],d[2],d[3],d[4],d[5],iprev)
            dprev = Cache(d[0],d[1],d[2],d[3],d[4],d[5],dprev)
        
        self.processor = Processor(dprev, iprev, self.start_address,self.no_of_ways,self.types,self.cycles,self.no_of_rob)
        self.instruction_store = iprev
        self.data_store = dprev

        code = self.code_box.get(1.0, END)
        self.code_box.delete(1.0, END)
        assembled_code = Assembler.assemble(code, self.start_address)
        self.code_box.insert(END, assembled_code)
        assembled_code = assembled_code.split("\n")
        curr_address = self.start_address
        for line in assembled_code:
            if line != "":
                self.memory.write_in_address(curr_address, line)
                curr_address += 2

        data = self.data_box.get(1.0, END).split("\n")
        for d in data:
            if d != "":
                dd = d.split(" ")
                self.memory.write_in_address(int(dd[0]), dd[1])

        self.update()
        self.progress_button.config(state='normal')
        self.execute_button.config(state='normal')


    def update(self):
        self.no_of_cycles.set(self.processor.cycles)
        self.no_of_instrutions.set(self.processor.get_instruction_number())
        self.pc_label.set(self.processor.pc)
        for i in range(8):
            self.register_labels[i].set(self.processor.register_file.get(i))
        self.data_box.delete(1.0, END)
        memory = self.memory.get_memory()
        for key in sorted(memory.keys()):
            if memory[key] != "":
                self.data_box.insert(END, str(key) + " " + str(memory[key]) + "\n")

    def prepare_data(self):
        print "Enter Start address : "
        self.start_address = int(raw_input())


        print "Main memory access time : "
        self.memory_access_time = int(raw_input())
        self.memory_access_time = 2
        
        print "Number of caches : "
        self.cache_levels = int(raw_input())
        self.cache_levels = 0
        
        if self.cache_levels > 0:
            print "Enter cache line size : "
            self.cache_block_size = int(raw_input())/2
        else:
            self.cache_block_size = 1

        self.caches = []
        for i in range(self.cache_levels):
            print "L" + str(i) + " Cache size : "
            s = int(raw_input())
            print "L" + str(i) + " associativity level : "
            m = int(raw_input())
            print "L" + str(i) + " hit cycles : "
            hc = int(raw_input())
            print "L" + str(i) + " Write through(0), Write Back(1) :"
            wh = int(raw_input())
            print "L" + str(i) + " Write allocate(2), Write arround(3) :"
            wm = int(raw_input())
            self.caches.append([s,self.cache_block_size,m,wh,wm,hc])

        print "Function units space seperated ( ADD, MULT, LOGICAL, BRANCHES, LOAD, STORE ) : "
        s = raw_input().split(" ")
        self.types = [ self.map_unit_to_id(i) for i in s ]

        self.cycles = {}
        for i in [ "ADD", "MULT", "LOGICAL", "BRANCHES", "LOAD", "STORE" ]:
            print "Cycles for %s :" % i
            self.cycles[self.map_unit_to_id(i)] = int(raw_input())

        print "No of ways :"
        self.no_of_ways = int(raw_input())

        print "No. of ROB :"
        self.no_of_rob = int(raw_input())
        
    
    def map_unit_to_id(self, str_):
        if str_ == "ADD":
            return FunctionalUnit.add
        elif str_ == "MULT":
            return FunctionalUnit.mult
        elif str_ == "LOGICAL":
            return FunctionalUnit.logical
        elif str_ == "BRANCHES":
            return FunctionalUnit.branches
        elif str_ == "LOAD":
            return FunctionalUnit.load
        elif str_ == "STORE":
            return FunctionalUnit.store

    def __init__(self):
        self.prepare_data()
        self.root = Tk()  # Ordinary window with title bar and decorations provided by window manager
        self.root.geometry("800x630")  # Set size of the displayed window
        self.root.wm_title("Memsim")

        # Begin menu bar
        menu = Menu(self.root)
        self.root.config(menu=menu)
        filemenu = Menu(menu)  # Define a menu element
        menu.add_cascade(label="File", menu=filemenu)
        filemenu.add_command(label="Exit", command=exit)
        #  End menu bar
        self.create_items()

    def paste(self ,event):
        text = self.code_box.selection_get(selection='CLIPBOARD')
        self.code_box.insert('insert', text)

    def copy(self, event=None):
        self.code_box.clipboard_clear()
        text = self.code_box.get("sel.first", "sel.last")
        self.code_box.clipboard_append(text)

    def create_items(self):
        self.code_box = Text(self.root)
        self.code_box.place(relx=1, x=-235, y=0, anchor=NE)

        self.data_box = Text(self.root)
        self.data_box.place(relx=1, x=-235, y=400, anchor=NE)
        self.data_box.config(height = 10)

        self.assemble_button = Button(self.root, text="Assemble", command=self.assemble)
        self.assemble_button.place(relx=1, x=-2, y=2, anchor=NE)

        self.execute_button = Button(self.root, text="Execute", command=self.execute)
        self.execute_button.place(relx=1, x=-2, y=32, anchor=NE)
        self.execute_button.config(state='disabled')

        self.progress_button = Button(self.root, text="Run Single Cycle", command=self.progress)
        self.progress_button.place(relx=1, x=-90, y=2, anchor=NE)
        self.progress_button.config(state='disabled')

        Label(self.root, text="No. Of Cycles:").place(relx=1, x=-140, y=70, anchor=NE)
        
        self.no_of_cycles = StringVar()
        self.no_of_cycles.set("zero")
        Label(self.root, textvariable=self.no_of_cycles).place(relx=1, x=-50, y=70, anchor=NE)


        Label(self.root, text="Inst. No.:").place(relx=1, x=-140, y=100, anchor=NE)
        
        self.no_of_instrutions = StringVar()
        self.no_of_instrutions.set("zero")
        Label(self.root, textvariable=self.no_of_instrutions).place(relx=1, x=-50, y=100, anchor=NE)


        Label(self.root, text="PC:").place(relx=1, x=-140, y=130, anchor=NE)
        

        self.pc_label = StringVar()
        self.pc_label.set("zero")
        Label(self.root, textvariable=self.pc_label).place(relx=1, x=-50, y=130, anchor=NE)

        self.register_labels = []
        for i in range(8):
            Label(self.root, text="R"+str(i)+":").place(relx=1, x=-140, y=160 + i*30, anchor=NE)
            
            tmp = StringVar()
            tmp.set("zero")
            Label(self.root, textvariable=tmp).place(relx=1, x=-50, y=160 + i*30, anchor=NE)
            self.register_labels.append(tmp)

        mainloop()

        self.root.mainloop()  # program stays in loop until we close the window

if __name__ == "__main__":
    GUI()
