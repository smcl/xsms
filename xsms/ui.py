from em73xx import Modem


class UI(object):
    def __init__(self, args):
        # initialise the device
        if args.device:
            self.modem = Modem(args.device, pin=args.pin)
        else:
            self.modem = None
        self.args = args
