# flake8: noqa
import ttk
import Tkinter
from datetime import datetime
from em73xx import SMS
import inbox
import outbox
import style
from utils import VerticalScrolledFrame

class GUI(object):

    def __init__(self, modem):
        self.modem = modem

    def show(self):
        root = Tkinter.Tk()
        root.title("xsms")
        nb = ttk.Notebook(root)

        #style.configure(ttk.Style())
        #ttk.Style().theme_use("classic")

        # create frames
        self.inbox_frame = self.mailbox_frame(nb, inbox.read())
        self.outbox_frame = self.mailbox_frame(nb, outbox.read())
        self.compose_frame = self.create_compose_frame(nb)

        # add frames to the notebook
        nb.add(self.inbox_frame, text="Inbox")
        nb.add(self.outbox_frame, text="Sent")
        nb.add(self.compose_frame, text="Compose")

        # render the main window
        nb.pack(expand=1, fill="both")
        root.mainloop()

    def mailbox_frame(self, parent, messages):
        f = VerticalScrolledFrame(parent)

        r = 0
        for m in messages:
            ttk.Label(f.interior, text=m.sender, anchor="w").grid(row=r,column=0, sticky=Tkinter.W)
            ttk.Label(f.interior, text=m.date_received.strftime('%d/%m/%Y %H:%M'), anchor="e").grid(row=r,column=1)
            msg = style.Text(f.interior, 4, 35)
            msg.grid(row=r+1, column=0, columnspan=2)
            msg.insert("1.0", m.message)
            msg.config(state=Tkinter.DISABLED)
            r = r + 2

        return f

    def create_compose_frame(self, parent):
        f = ttk.Frame(parent)

        self.recipient_input = ttk.Entry(f, width=30)
        self.message_input = style.Text(f, 4, 30)
        self.send_button = ttk.Button(f, text="Send", command=lambda: self.send(self.recipient_input.get(), self.message_input.get("1.0", Tkinter.END)))

        # if we haven't initialised a device, we can't send anything
        if not self.modem:
            self.message_input.insert("1.0", "No modem initialised, start xsms with the --device switch if you want to send messages")
            self.recipient_input.config(state=Tkinter.DISABLED)
            self.message_input.config(state=Tkinter.DISABLED)
            self.send_button.config(state=Tkinter.DISABLED)

        self.recipient_input.pack(fill=Tkinter.X)
        self.message_input.pack(fill=Tkinter.X)
        self.send_button.pack(fill=Tkinter.X)

        return f

    def send(self, recipient, message):
        if not recipient.strip() or not message.strip():
            return

        self.modem.sendSMS(str(recipient), str(message))

        # I know this ain't pretty
        outbox.append(
            SMS(-1, None, recipient, datetime.now(), message, True)
        )

        # clear the outbox frame
        for widget in self.outbox_frame.winfo_children():
            widget.destroy()

        # and refresh it with the new inbox
        self.populate_messages(self.outbox_frame, outbox.read())

        # clear the compose frame
        self.message_input.delete("1.0", Tkinter.END)
        self.message_input.insert("1.0", "")
        self.recipient_input.delete(0, Tkinter.END)
        self.recipient_input.insert(0, "")
