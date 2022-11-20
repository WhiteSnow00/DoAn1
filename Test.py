from tkinter import *
from tkinter import ttk

# Create an instance of tkinter frame
win= Tk()

# Set the size of the tkinter window
win.geometry("700x350")

# Add a Treeview widget and set the selection mode
tree= ttk.Treeview(win, column=("c1", "c2"), show='headings', height= 8, selectmode="browse")
tree.column("#1", anchor=CENTER, stretch= NO)
tree.heading("#1", text="Fname")
tree.column("#2", anchor=CENTER, stretch=NO)
tree.heading("#2", text="Lname")

# Insert the data in Treeview widget
tree.insert('', 'end', text= "1",values=('Alex', 'M'))
tree.insert('', 'end', text="2",values=('Belinda','Cross'))
tree.insert('', 'end', text="3",values=('Ravi','Malviya'))
tree.insert('', 'end', text="4",values=('Suresh','Rao'))
tree.insert('', 'end', text="5",values=('Amit','Fernandiz'))
tree.insert('', 'end', text= "6",values=('Raghu','Sharma'))
tree.insert('', 'end',text= "7",values=('David','Nash'))
tree.insert('', 'end',text= "8",values=('Ethan','Plum'))
tree.insert('', 'end', text= "9", values=('Janiece','-'))

# Adding a vertical scrollbar to Treeview widget
treeScroll = ttk.Scrollbar(win)
treeScroll.configure(command=tree.yview)
tree.configure(yscrollcommand=treeScroll.set)
treeScroll.pack(side= RIGHT, fill= BOTH)
tree.pack()

win.mainloop()