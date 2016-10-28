import Tkinter

# colors
bg_color = "black"
mid_color = "dimgrey"
fg_color = "grey"
bright_color = "white"

# fonts
headFont = ("Source Code Pro", 10, "bold")
bodyFont = ("Source Code Pro", 10)

# need to style the following:
# - Label
# - Text
# - Entry
# - Button
# - Notebook

xsms_style = "xsms"

# flake8: noqa
style_applied = False


def configure(style):
    style_applied = True

    # style.theme_create(xsms_style, parent="alt")

    # style.configure("TLabel", foreground=fg_color, background=bg_color)
    # style.configure("TEntry", foreground=fg_color, background=bg_color)
    # style.configure("TButton", foreground=fg_color, background=bg_color)
    # style.configure("TNotebook", foreground=fg_color, background=bg_color)
    # style.configure("TFrame", foreground=fg_color, background=bg_color)
    style.configure(".", foreground=fg_color, background=bg_color)
    # style.configure(".", relief="flat")

    # style the notebook tabs
    style.configure("TNotebook", background=bg_color)
    style.map("TNotebook.Tab",
              background=[("selected", mid_color)],
              foreground=[("selected", bright_color)])
    style.configure("TNotebook.Tab", background=bg_color, foreground=fg_color)

    # style.theme_use(xsms_style)


def Text(parent, height, width):
    if style_applied:
        return Tkinter.Text(parent,
                            height=height,
                            width=width,
                            bg=bg_color,
                            fg=fg_color)

    return Tkinter.Text(parent, height=height, width=width)
