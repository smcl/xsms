import ttk
import Tkinter
import style
from .message_actions_frame import MessageActionsFrame


# ideally this would subclass ttk.Frame and initialise it using super() but apparently
# ttk.Frame is an old style object ("class Frame:" vs "class Frame(object):" which
# super() doesn't play nice with :-/
class MessageFrame(object):
    def __init__(self, parent, modem, message, show_actions, reply_method):
        self.frame = ttk.Frame(parent)
        self.modem = modem

        ttk.Label(self.frame, text=message.sender, anchor="w").grid(row=0,column=0, sticky=Tkinter.W)
        ttk.Label(self.frame, text=message.date_received.strftime('%d/%m/%Y %H:%M'), anchor="e").grid(row=0,column=1)
        msg = style.Text(self.frame, 4, 35)
        msg.grid(row=1, column=0, columnspan=2)
        msg.insert("1.0", message.message)
        msg.config(state=Tkinter.DISABLED)

        if show_actions:
            MessageActionsFrame(self.frame, lambda: reply_method(message.sender)).grid(2, 0, 1)

        ttk.Separator(self.frame, orient=Tkinter.HORIZONTAL).grid(row=3, columnspan=2, sticky="ew", pady=5)

    def pack(self):
        self.frame.pack()
