from Tkinter import *
from MainMemory import MainMemory
from Cache import Cache
from Processor import Processor
from Assembler import Assembler

class GUI:
    
    def execute(self):
        print "HI"

    def progress(self):
        ret = self.processor.progress()
        if ret != False:
            self.update()
        else:
            self.progress_button.config(state='disabled')
            self.execute_button.config(state='disabled')

    def assemble(self):

        self.memory = MainMemory(64*1024, self.memory_access_time, 2)
        self.processor = Processor(self.memory, self.memory, self.start_address)
        self.instruction_store = self.memory
        self.data_store = self.memory

        code = self.code_box.get(1.0, END)
        self.code_box.delete(1.0, END)
        assembled_code = Assembler.assemble(code, self.start_address)
        self.code_box.insert(END, assembled_code)
        assembled_code = assembled_code.split("\n")
        curr_address = self.start_address
        for line in assembled_code:
            self.instruction_store.write_in_address(curr_address, line)
            curr_address += 2
        self.update()
        self.progress_button.config(state='normal')
        self.execute_button.config(state='normal')


    def update(self):
        self.no_of_cycles.set(self.processor.cycles)
        self.no_of_instrutions.set(self.processor.get_instruction_number())
        self.pc_label.set(self.processor.pc)
        for i in range(8):
            self.register_labels[i].set(self.processor.register_file.get(i))
        
    def prepare_data(self):
        print "Enter Start address : "
        self.start_address = int(raw_input())


        print "Main memory access time : "
        self.memory_access_time = int(raw_input())
        
        #print "Number of caches : "
        #caches = int(raw_input())
        #dprev = self.memory
        #self.dcaches = []

        #iprev = self.memory
        #self.icaches = []
        #for i in range(caches):
            #print "L" + str(i) + " Cache geometry : "
            #s,l,m = [ int(raw_input()) for j in range(3) ]
            #print "L" + str(i) + " hit cycles : "
            #hc = int(raw_input())

            #self.dcaches.append(Cache(s,l,m,1,3,hc,dprev))
            #self.icaches.append(Cache(s,l,m,1,3,hc,iprev))
            #dprev = self.dcaches[i]
            #iprev = self.icaches[i]
        #self.processor = Processor(dprev, iprev, self.start_address)
        #self.instruction_store = iprev
        #self.data_store = dprev

        
        
    def __init__(self):
        self.prepare_data()
        self.root = Tk()  # Ordinary window with title bar and decorations provided by window manager
        self.root.geometry("800x430")  # Set size of the displayed window
        self.root.wm_title("Memsim")

        # Begin menu bar
        menu = Menu(self.root)
        self.root.config(menu=menu)
        filemenu = Menu(menu)  # Define a menu element
        menu.add_cascade(label="File", menu=filemenu)
        filemenu.add_command(label="Exit", command=exit)
        #  End menu bar
        self.create_items()

    def create_items(self):
        self.code_box = Text(self.root)
        self.code_box.place(relx=1, x=-235, y=0, anchor=NE)

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
