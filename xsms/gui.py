# flake8: noqa
import ttk
from Tkinter import *
from datetime import datetime
from em73xx import SMS
import outbox

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


# this is some nasty shit
def sendmsg(recipient, message, modem):
    modem.sendSMS(str(recipient), str(message))
    outbox_messages = outbox.read()
    outbox_messages.append(
        SMS(-1, None, recipient, datetime.now(), message, True)
    )
    outbox.write(outbox_messages)

def create_compose_frame(parent, modem):
    f = ttk.Frame(parent)

    recipient_input = Entry(f, width=35)
    message_input = Text(f, height=4, width=35)
    send_button = Button(f, text="Send", command=lambda: sendmsg(recipient_input.get(), message_input.get("1.0", END), modem))

    # if we haven't initialised a device, we can't send anything
    if not modem:
        message_input.insert("1.0", "No modem initialised, start xsms with the --device switch if you want to send messages")
        recipient_input.config(state=DISABLED)
        message_input.config(state=DISABLED)
        send_button.config(state=DISABLED)



    recipient_input.pack(fill=X)
    message_input.pack(fill=X)
    send_button.pack()

    return f


def launch_gui(inbox_messages, outbox_messages, modem):
    root = Tk()
    root.title("xsms")

    nb = ttk.Notebook(root)

    inbox_frame = create_inbox_frame(nb, inbox_messages)
    outbox_frame = create_outbox_frame(nb, outbox_messages)
    compose_frame = create_compose_frame(nb, modem)

    nb.add(inbox_frame, text="Inbox")
    nb.add(outbox_frame, text="Sent")
    nb.add(compose_frame, text="Compose")

    nb.pack(expand=1, fill="both")

    root.mainloop()
