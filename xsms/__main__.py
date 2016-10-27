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

from .gui import launch_gui

# system imports
import argparse

# there's gotta be a better way than a global...
modem = None

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


def print_unread_messages(read_format, unread_format, messages):
    unread_count = len([m for m in messages if not m.read])

    if unread_count:
        print(args.unread_format % (unread_count))
    else:
        print(args.read_format)


if __name__ == '__main__':
    args = get_args()

    # read existing inbox and outbox
    inbox_messages = inbox.read()
    outbox_messages = outbox.read()

    # retrieve new messages from the modem and add to the inbox
    if args.device:
        # initialise the device
        modem = Modem(args.device, pin=args.pin)

        for m in modem.getSMS():
            inbox_messages.append(m)

            # serialise inbox
            inbox.write(inbox_messages)

            # clear outstanding messages from SIM
            modem.deleteAllSMS()

    # decide whether to launch the GUI or just check + print unread
    if args.gui:
        launch_gui(inbox_messages, outbox_messages, modem)
    else:
        print_unread_messages(args.read_format, args.unread_format, inbox_messages)
