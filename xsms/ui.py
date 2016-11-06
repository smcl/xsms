import inbox
from em73xx import Modem


class UI(object):
    def __init__(self, args):
        if args.device:
            self.modem = Modem(args.device, pin=args.pin)
        else:
            self.modem = None
        self.args = args

    def refresh_messages(self):
        messages = inbox.read()

        if self.modem:
            new_messages = self.modem.getSMS()
            messages += new_messages
            if new_messages:
                inbox.append(new_messages)
                self.modem.deleteAllSMS()

        return messages
