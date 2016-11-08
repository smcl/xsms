# flake8: noqa
import ttk
import Tkinter
from datetime import datetime
from em73xx import SMS
import outbox
import style
from utils import VerticalScrolledFrame
from ui import UI
from .message_frame import MessageFrame

window_title= "xsms"
inbox_label = "Inbox"
sent_label = "Sent"
compose_label = "Compose"


class GUI(UI):

    def __init__(self, args):
        super(GUI, self).__init__(args)
        self.tab_id = {}

    def show(self):
        root = Tkinter.Tk()
        root.title(window_title)
        #style.configure(ttk.Style())

        self.nb = ttk.Notebook(root)

        # create frames
        self.inbox_frame = self.mailbox_frame(self.nb, self.refresh_messages(), True)
        self.outbox_frame = self.mailbox_frame(self.nb, outbox.read(), False)
        self.compose_frame = self.create_compose_frame(self.nb)

        # add frames as tabs to the notebook
        self.add_tab(inbox_label, self.inbox_frame)
        self.add_tab(sent_label, self.outbox_frame)
        self.add_tab(compose_label, self.compose_frame)

        # render the main window
        self.nb.pack(expand=1, fill="both")
        root.mainloop()

    def add_tab(self, name, frame):
        self.nb.add(frame, text=name)
        self.tab_id[name] = self.nb.tabs()[-1]

    def switch_tab(self, name):
        self.nb.select(self.tab_id[name])

    def mailbox_frame(self, parent, messages, show_actions):
        f = VerticalScrolledFrame(parent)
        self.populate_messages(f.interior, messages, show_actions)
        return f

    def populate_messages(self, parent, messages, show_actions):
        for m in messages:
            MessageFrame(parent, self.modem, m, show_actions, self.reply).pack()

    def reply(self, number):
        self.switch_tab(compose_label)
        self.recipient_input.delete(0, Tkinter.END)
        self.recipient_input.insert(0, number)

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
        self.populate_messages(self.outbox_frame, outbox.read(), False)

        # clear the compose frame
        self.message_input.delete("1.0", Tkinter.END)
        self.message_input.insert("1.0", "")
        self.recipient_input.delete(0, Tkinter.END)
        self.recipient_input.insert(0, "")
