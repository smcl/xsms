from .utils import read_messages
from .utils import write_messages


outbox_filename = "outbox.json"


def read():
    return read_messages(outbox_filename)


def append(message):
    new_outbox = read()
    new_outbox.append(message)
    write(new_outbox)


def write(messages):
    write_messages(outbox_filename, messages)
