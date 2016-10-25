from .utils import read_messages
from .utils import write_messages


inbox_filename = "inbox.json"


def read():
    return read_messages(inbox_filename)


def write(messages):
    write_messages(inbox_filename, messages)
