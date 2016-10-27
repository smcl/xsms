# flake8: noqa
import ttk
import Tkinter
from datetime import datetime
from em73xx import SMS
import outbox
import style

def mailbox_frame(parent, messages):
    f = ttk.Frame(parent)

    r = 0
    for m in messages:
        ttk.Label(f, text=m.sender, anchor="w").grid(row=r,column=0, sticky=Tkinter.W)
        ttk.Label(f, text=m.date_received.strftime('%d/%m/%Y %H:%M'), anchor="e").grid(row=r,column=1)
        msg = style.Text(f, 4, 35)
        msg.grid(row=r+1, column=0, columnspan=2)
        msg.insert("1.0", m.message)
        msg.config(state=Tkinter.DISABLED)

        r = r + 2

    return f

def create_inbox_frame(parent, messages):
    return mailbox_frame(parent, messages)


def create_outbox_frame(parent, messages):
    return mailbox_frame(parent, messages)


# this is some nasty shit
def sendmsg(recipient, message, modem):
    if not recipient.strip() or not message.strip():
        return

    modem.sendSMS(str(recipient), str(message))
    outbox_messages = outbox.read()
    outbox_messages.append(
        SMS(-1, None, recipient, datetime.now(), message, True)
    )
    outbox.write(outbox_messages)

def create_compose_frame(parent, modem):
    f = ttk.Frame(parent)

    recipient_input = ttk.Entry(f, width=30)
    message_input = style.Text(f, 4, 30)
    send_button = ttk.Button(f, text="Send", command=lambda: sendmsg(recipient_input.get(), message_input.get("1.0", END), modem))

    # if we haven't initialised a device, we can't send anything
    if not modem:
        message_input.insert("1.0", "No modem initialised, start xsms with the --device switch if you want to send messages")
        recipient_input.config(state=Tkinter.DISABLED)
        message_input.config(state=Tkinter.DISABLED)
        send_button.config(state=Tkinter.DISABLED)

    recipient_input.pack(fill=Tkinter.X)
    message_input.pack(fill=Tkinter.X)
    send_button.pack(fill=Tkinter.X)

    return f


def launch_gui(inbox_messages, outbox_messages, modem):
    root = Tkinter.Tk()
    root.title("xsms")

    nb = ttk.Notebook(root)

    #style.configure(ttk.Style())
    #ttk.Style().theme_use("classic")

    inbox_frame = create_inbox_frame(nb, inbox_messages)
    outbox_frame = create_outbox_frame(nb, outbox_messages)
    compose_frame = create_compose_frame(nb, modem)

    nb.add(inbox_frame, text="Inbox")
    nb.add(outbox_frame, text="Sent")
    nb.add(compose_frame, text="Compose")

    nb.pack(expand=1, fill="both")

    root.mainloop()
