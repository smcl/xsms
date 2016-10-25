import json
import os
from em73xx import SMS


def get_xsms_folder():
    xsms_path = os.path.join(os.path.expanduser('~'), ".xsms")

    if not os.path.isdir(xsms_path):
        os.makedirs(xsms_path)

    return xsms_path


def read_messages(filename):
    messages_path = os.path.join(get_xsms_folder(), filename)

    messages = []

    if os.path.exists(messages_path):
        with open(messages_path) as messages_file:
            raw_messages = json.load(messages_file)

            for sms_json in raw_messages:
                messages.append(SMS.fromJson(sms_json))

    return messages


def write_messages(filename, messages):
    messages_path = os.path.join(get_xsms_folder(), filename)

    with open(messages_path, "w") as messages_file:
        messages_file.write(json.dumps([m.toJson() for m in messages]))
