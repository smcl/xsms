import ttk
import Tkinter


# as above, this should subclass ttk.Frame, but it doesn't due to ttk's
# use of old-style objects
class MessageActionsFrame(object):
    def __init__(self, parent, reply_method):
        self.frame = ttk.Frame(parent)

        reply_button = ttk.Button(self.frame, text="reply", width=4,
                                  command=reply_method)
        reply_button.pack(side=Tkinter.LEFT)
        # ttk.Button(self.frame, text="read", width=4).pack(side=Tkinter.LEFT)
        # ttk.Button(self.frame, text="del", width=3).pack(side=Tkinter.LEFT)

    def grid(self, row, col, colspan):
        self.frame.grid(row=row, column=col, columnspan=colspan)
