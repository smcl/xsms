import inbox


class TextUI(object):

    def __init__(self, modem):
        self.modem = modem

    def show(self, read_format, unread_format):
        messages = inbox.read()

        if self.modem:
            self.read_from_sim(messages)

        unread_count = len([m for m in messages if not m.read])

        if unread_count:
            print(unread_format % (unread_count))
        else:
            print(read_format)

    def read_from_sim(self, messages):
        for m in self.modem.getSMS():
            messages.append(m)

            # serialise inbox
            inbox.write(messages)

            # clear outstanding messages from SIM
            self.modem.deleteAllSMS()
