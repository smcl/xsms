# system imports
import argparse

# local imports
from .gui import GUI
from .textui import TextUI


def get_args():
    parser = argparse.ArgumentParser(
        description="xsms - an sms client for linux systems with an em73xx",
        # epilog="some bullshit example usage"
    )

    # optional switches
    parser.add_argument('-d', '--device', action='store')
    parser.add_argument('-g', '--gui', action='store_true')

    # optional args
    parser.add_argument('-p', '--pin', action='store', default="")
    parser.add_argument('-r', '--read_format', action='store',
                        default="(empty)")
    parser.add_argument('-u', '--unread_format', action='store',
                        default="%d")

    return parser.parse_args()

def get_ui(args):
    if args.gui:
        return GUI(args)
    return TextUI(args)


if __name__ == '__main__':
    args = get_args()
    ui = get_ui(args)
    ui.show()
