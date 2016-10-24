import json
import time
import os
import sys

from em73xx import SMS

def get_inbox_path():
    xsms_path = os.path.join(os.path.expanduser('~'), ".xsms")
    if not os.path.isdir(xsms_path):
        os.makedirs(xsms_path)

    inbox_path = os.path.join(xsms_path, "inbox.json")

    return inbox_path

def read_inbox():

    inbox_path = get_inbox_path()

    inbox = []

    if os.path.exists(inbox_path):
        with open(inbox_path) as inbox_file:
            raw_inbox = json.load(inbox_file)

            for sms_json in raw_inbox:
                inbox.append(SMS.fromJson(sms_json))

    return inbox

def write_inbox(inbox):
    inbox_path = get_inbox_path()

    # serialise and save back into inbox.json
    with open(inbox_path, "w") as inbox_file:
        inbox_file.write(json.dumps([m.toJson() for m in inbox]))
