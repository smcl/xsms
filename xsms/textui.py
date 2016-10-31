import inbox
from ui import UI


class TextUI(UI):

    def show(self):
        messages = inbox.read()

        if self.modem:
            self.read_from_sim(messages)

        unread_count = len([m for m in messages if not m.read])

        if unread_count:
            print(self.args.unread_format % (unread_count))
        else:
            print(self.args.read_format)

    def read_from_sim(self, messages):
        new_messages = self.modem.getSMS()

        if new_messages:
            messages.append(new_messages)
            inbox.append(messages)
            self.modem.deleteAllSMS()
