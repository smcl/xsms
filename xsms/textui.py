from ui import UI


class TextUI(UI):

    def show(self):
        messages = self.refresh_messages()
        unread_count = len([m for m in messages if not m.read])
        if unread_count:
            print(self.args.unread_format % (unread_count))
        else:
            print(self.args.read_format)
