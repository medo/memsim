from Tkinter import *

root = Tk()  # Ordinary window with title bar and decorations provided by window manager
root.geometry("800x380")  # Set size of the displayed window


def callback():
    print "called the callback!"

# TODO: delete the print hello method and the callback() once you link the GUI with the backend
def print_hello():
    # lbl1["text"]= "Hello World"
    return

# Begin menu bar
menu = Menu(root)
root.config(menu=menu)

filemenu = Menu(menu)  # Define a menu element
menu.add_cascade(label="File", menu=filemenu)
filemenu.add_command(label="New", command=callback)
filemenu.add_command(label="Open...", command=callback)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=callback)

helpmenu = Menu(menu)
menu.add_cascade(label="Help", menu=helpmenu)
helpmenu.add_command(label="About...", command=callback)

#  End menu bar

codeTextBox = Text(root).place(relx=1, x=-235, y=0, anchor=NE)  # text area positioning and naming

button_execute = Button(root, text="Execute", command=print_hello)
button_execute.place(relx=1, x=-2, y=2, anchor=NE)

button_single_cycle = Button(root, text="Run Single Cycle", command=print_hello)
button_single_cycle.place(relx=1, x=-70, y=2, anchor=NE)


label_number_of_cycles = Label(root, text="No. Of Cycles:")
label_number_of_cycles.place(relx=1, x=-140, y=70, anchor=NE)

textlabel_number_of_cycles = Label(root, text="zero")
textlabel_number_of_cycles.place(relx=1, x=-50, y=70, anchor=NE)


label_instruction_number = Label(root, text="Inst. No.:")
label_instruction_number.place(relx=1, x=-140, y=100, anchor=NE)

textlabel_instruction_number = Label(root, text="zero")
textlabel_instruction_number.place(relx=1, x=-50, y=100, anchor=NE)


label_register_zero = Label(root, text="R0:")
label_register_zero.place(relx=1, x=-140, y=130, anchor=NE)

textlabel_register_zero = Label(root, text="zero")
textlabel_register_zero.place(relx=1, x=-50, y=130, anchor=NE)


label_register_one = Label(root, text="R1:")
label_register_one.place(relx=1, x=-140, y=160, anchor=NE)

textlabel_register_one = Label(root, text="zero")
textlabel_register_one.place(relx=1, x=-50, y=160, anchor=NE)


label_register_two = Label(root, text="R2:")
label_register_two.place(relx=1, x=-140, y=190, anchor=NE)

textlabel_register_two = Label(root, text="zero")
textlabel_register_two.place(relx=1, x=-50, y=190, anchor=NE)


label_register_three = Label(root, text="R3:")
label_register_three.place(relx=1, x=-140, y=220, anchor=NE)

textlabel_register_three = Label(root, text="zero")
textlabel_register_three.place(relx=1, x=-50, y=220, anchor=NE)


label_register_four = Label(root, text="R4:")
label_register_four.place(relx=1, x=-140, y=250, anchor=NE)

textlabel_register_four = Label(root, text="zero")
textlabel_register_four.place(relx=1, x=-50, y=250, anchor=NE)


label_register_five = Label(root, text="R5:")
label_register_five.place(relx=1, x=-140, y=280, anchor=NE)

textlabel_register_five = Label(root, text="zero")
textlabel_register_five.place(relx=1, x=-50, y=280, anchor=NE)


label_register_six = Label(root, text="R6:")
label_register_six.place(relx=1, x=-140, y=310, anchor=NE)

textlabel_register_six = Label(root, text="zero")
textlabel_register_six .place(relx=1, x=-50, y=310, anchor=NE)


label_register_seven = Label(root, text="R7:")
label_register_seven.place(relx=1, x=-140, y=340, anchor=NE)

textlabel_register_seven = Label(root, text="zero")
textlabel_register_seven.place(relx=1, x=-50, y=340, anchor=NE)


mainloop()

root.mainloop()  # program stays in loop until we close the window