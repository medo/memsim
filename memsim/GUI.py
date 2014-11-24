from Tkinter import *
from MainMemory import MainMemory
from Cache import Cache
from Processor import Processor

class GUI:
    
    def print_hello(self):
        # lbl1["text"]= "Hello World"
        return

    def execute(self):
        print "HI"

    def progress(self):
        print "HH"

    def assemble(self):
        self.update()

    def update(self):
        self.no_of_cycles.set(self.processor.cycles)
        self.no_of_instrutions.set(self.processor.cycles)
        self.pc_label.set(self.processor.pc)
        for i in range(8):
            self.register_labels[i].set(self.processor.register_file.get(i))
        
    def prepare_data(self):
        print "Enter Start address : "
        self.start_address = int(raw_input())


        print "Main memory access time : "
        memory_access_time = int(raw_input())
        self.memory = MainMemory()
        
        print "Number of caches : "
        caches = int(raw_input())
        dprev = self.memory
        self.dcaches = []

        iprev = self.memory
        self.icaches = []
        for i in range(caches):
            print "L" + str(i) + " Cache geometry : "
            s,l,m = [ int(raw_input()) for j in range(3) ]
            print "L" + str(i) + " hit cycles : "
            hc = int(raw_input())
            print "L" + str(i) + " miss cycles : "
            mc = int(raw_input())

            self.dcaches.append(Cache(s,l,m,1,3,hc,mc,dprev))
            self.icaches.append(Cache(s,l,m,1,3,hc,mc,iprev))
            dprev = self.dcaches[i]
            iprev = self.icaches[i]
        self.processor = Processor(dprev, iprev, self.start_address)

        
        
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
        self.code_box = Text(self.root).place(relx=1, x=-235, y=0, anchor=NE)

        Button(self.root, text="Assemble", command=self.assemble).place(relx=1, x=-2, y=2, anchor=NE)

        Button(self.root, text="Execute", command=self.execute).place(relx=1, x=-2, y=32, anchor=NE)

        Button(self.root, text="Run Single Cycle", command=self.progress).place(relx=1, x=-90, y=2, anchor=NE)

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
