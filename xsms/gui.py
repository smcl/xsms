from Tkinter import *

# i have no idea how ot call this
def derp(messages):
    root = Tk()
    header = Frame(root)
    r = 0
    for m in messages:
        Label(header, text=m.sender, anchor="w").grid(row=r,column=0, sticky=W)
        Label(header, text="2016-10-23 12:01", anchor="e").grid(row=r,column=1)
        msg = Text(header, height=4, width=35)
        msg.grid(row=r+1, column=0, columnspan=2)
        msg.insert("1.0", m.message)
        r = r + 2

    header.pack()

    mainloop()
