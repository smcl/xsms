# flake8: noqa
import ttk
from Tkinter import *


def mailbox_frame(parent, messages):
    f = ttk.Frame(parent)

    r = 0
    for m in messages:
        Label(f, text=m.sender, anchor="w").grid(row=r,column=0, sticky=W)
        Label(f, text=m.date_received, anchor="e").grid(row=r,column=1)
        msg = Text(f, height=4, width=35)
        msg.grid(row=r+1, column=0, columnspan=2)
        msg.insert("1.0", m.message)
        msg.config(state=DISABLED)

        r = r + 2

    return f

def create_inbox_frame(parent, messages):
    return mailbox_frame(parent, messages)


def create_outbox_frame(parent, messages):
    return mailbox_frame(parent, messages)


def create_compose_frame(parent):
    f = ttk.Frame(parent)
    return f


def launch_gui(inbox_messages, outbox_messages):
    root = Tk()
    root.title("xsms")

    nb = ttk.Notebook(root)

    inbox_frame = create_inbox_frame(nb, inbox_messages)
    outbox_frame = create_outbox_frame(nb, outbox_messages)
    compose_frame = create_compose_frame(nb)

    nb.add(inbox_frame, text="Inbox")
    nb.add(outbox_frame, text="Sent")
    nb.add(compose_frame, text="Compose")

    nb.pack(expand=1, fill="both")

    root.mainloop()
