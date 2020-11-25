import tkinter as Tk


def fun_button1():
    s_button.set('You pressed button1')


def fun_button2():
    s_button.set('You pressed button2')


def fun_click(event):
    s_click.set('You clicked at position (%d, %d)' % (event.x, event.y))


def fun_entry():
    s_entry.set('You said: ' + E1.get())


def fun_scale(event):
    s_scale.set("Your favourite number is " + str(x_scale.get()))


def fun_listbox(event):
    s_listbox.set("Your favourite color is " + LB.get(LB.curselection()))


root = Tk.Tk()


# Define Tk variable
s_button = Tk.StringVar()
s_button.set('Information for button')
s_entry = Tk.StringVar()
s_scale = Tk.StringVar()
x_scale = Tk.DoubleVar()
s_click = Tk.StringVar()
s_listbox = Tk.StringVar()

# Define widgets
L_button = Tk.Label(root, textvariable=s_button)
B1 = Tk.Button(root, text='button1', command=fun_button1)
B2 = Tk.Button(root, text='button2', command=fun_button2)
L_entry = Tk.Label(root, text='Say something: ')
E1 = Tk.Entry(root)
B_entry = Tk.Button(root, text='Say', command=fun_entry)
L_show_entry = Tk.Label(root, textvariable=s_entry)
L_scale = Tk.Label(root, textvariable=s_scale)
S1 = Tk.Scale(root, variable=x_scale, command=fun_scale)
L_cilck = Tk.Label(root, textvariable=s_click)
LB = Tk.Listbox(root)
L_listbox = Tk.Label(root, textvariabl=s_listbox)
for i, color in enumerate(["red", "blue", "yello", "orange", "green", "purple"]):
    LB.insert(i, color)
LB.bind('<Double-Button-1>', fun_listbox)

F1 = Tk.Frame(root, width=200, height=100)
F1.bind("<Button-1>", fun_click)  # "<Button-1>" refers to the mouse

# Place widgets
L_button.pack()
B1.pack(fill=Tk.X)
B2.pack(fill=Tk.X)
L_entry.pack()
E1.pack()
L_show_entry.pack()
B_entry.pack(fill=Tk.X)
L_scale.pack()
S1.pack()
F1.pack()
F1.focus_set()  # This activates the keyboard
L_cilck.pack()
L_listbox.pack()
LB.pack()

B_quit = Tk.Button(root, text='Quit', command=root.quit)
B_quit.pack(fill=Tk.X)

root.mainloop()
