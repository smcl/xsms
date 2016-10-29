import json
import os
import Tkinter
from em73xx import SMS


def get_xsms_folder():
    xsms_path = os.path.join(os.path.expanduser('~'), ".xsms")

    if not os.path.isdir(xsms_path):
        os.makedirs(xsms_path)

    return xsms_path


def read_messages(filename):
    messages_path = os.path.join(get_xsms_folder(), filename)

    messages = []

    if os.path.exists(messages_path):
        with open(messages_path) as messages_file:
            raw_messages = json.load(messages_file)

            for sms_json in raw_messages:
                messages.append(SMS.fromJson(sms_json))

    return messages


def write_messages(filename, messages):
    messages_path = os.path.join(get_xsms_folder(), filename)

    with open(messages_path, "w") as messages_file:
        messages_file.write(json.dumps([m.toJson() for m in messages]))


class VerticalScrolledFrame(Tkinter.Frame):
    """A pure Tkinter scrollable frame that actually works!

    * Use the 'interior' attribute to place widgets inside the scrollable frame
    * Construct and pack/place/grid normally
    * This frame only allows vertical scrolling

    """
    def __init__(self, parent, *args, **kw):
        Tkinter.Frame.__init__(self, parent, *args, **kw)

        # create a canvas object and a vertical scrollbar for scrolling it
        vscrollbar = Tkinter.Scrollbar(self, orient=Tkinter.VERTICAL)
        vscrollbar.pack(fill=Tkinter.Y, side=Tkinter.RIGHT,
                        expand=Tkinter.FALSE)
        canvas = Tkinter.Canvas(self, bd=0, highlightthickness=0,
                                yscrollcommand=vscrollbar.set)
        canvas.pack(side=Tkinter.LEFT, fill=Tkinter.BOTH, expand=Tkinter.TRUE)
        vscrollbar.config(command=canvas.yview)

        # reset the view
        canvas.xview_moveto(0)
        canvas.yview_moveto(0)

        # create a frame inside the canvas which will be scrolled with it
        self.interior = interior = Tkinter.Frame(canvas)
        interior_id = canvas.create_window(0, 0, window=interior,
                                           anchor=Tkinter.NW)

        # track changes to the canvas and frame width and sync them,
        # also updating the scrollbar
        def _configure_interior(event):
            # update the scrollbars to match the size of the inner frame
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            canvas.config(scrollregion="0 0 %s %s" % size)
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the canvas's width to fit the inner frame
                canvas.config(width=interior.winfo_reqwidth())
        interior.bind('<Configure>', _configure_interior)

        def _configure_canvas(event):
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the inner frame's width to fill the canvas
                canvas.itemconfigure(interior_id, width=canvas.winfo_width())
        canvas.bind('<Configure>', _configure_canvas)

        return
