# flake8: noqa
"""
__main__.py

Main launch script for xsms system. Has two distinct behaviours - will connect to the modem, download messages and merge into ~/.xsms/inbox.json then either

1. (if --check is supplied) print one of two strings to stdout, depending on if there are any unread messages
2. (otherwise) will launch a simple Tk app to send/receive SMS messages
"""

# system imports
from em73xx import Modem

# local imports
import inbox
import outbox
from .gui import GUI
from .textui import TextUI

# system imports
import argparse


def get_args():
    parser = argparse.ArgumentParser(
        description="xsms - an sms client for linux systems with an em73xx modem",
        # epilog="some bullshit example usage"
    )

    # optional switches
    parser.add_argument('-d', '--device', action='store')
    parser.add_argument('-g', '--gui', action='store_true')

    # optional args
    parser.add_argument('-p', '--pin', action='store', default="")
    parser.add_argument('-r', '--read_format', action='store', default="(empty)")
    parser.add_argument('-u', '--unread_format', action='store', default="%d")

    return parser.parse_args()


if __name__ == '__main__':
    args = get_args()

    # initialise the device
    if args.device:
        modem = Modem(args.device, pin=args.pin)
    else:
        modem = None

    # decide whether to launch the GUI or just check + print unread
    if args.gui:
        GUI(modem).show()
    else:
        TextUI(modem).show(args.read_format, args.unread_format)
