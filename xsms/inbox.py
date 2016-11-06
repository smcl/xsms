from .utils import read_messages
from .utils import write_messages


inbox_filename = "inbox.json"


def read():
    return read_messages(inbox_filename)


def append(messages):
    new_inbox = read()
    new_inbox += messages
    write(new_inbox)


def write(messages):
    write_messages(inbox_filename, messages)
