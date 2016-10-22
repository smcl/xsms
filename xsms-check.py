#!/usr/bin/python

"""
xsms-check.py

Script for xsms system - will connect to the modem using the em73xx package, find any new messages, archive them in the inbox, then delete them and notify xmobar how many new ones there were.
"""

import json
import time
import os
import sys
from em73xx import (
    Modem,
    SMS
)

device = sys.argv[1]
pin = sys.argv[2]

# fontawesome glyphs - empty/full envelopes
envelope = "\xef\x83\xa0"
envelope_empty = "\xef\x80\x83"

# initialise the device
if pin:
    em7345 = Modem(device, pin=pin)
else:
    em7345 = Modem(device)

xsms_path = os.path.join(os.path.expanduser('~'), ".xsms")
if not os.path.isdir(xsms_path):
    os.makedirs(xsms_path)

inbox_path = os.path.join(xsms_path, "inbox.json")

# read existing messages from inbox.json
inbox = []

if os.path.exists(inbox_path):
    with open(inbox_path) as inbox_file:
        raw_inbox = json.load(inbox_file)

        for sms_json in raw_inbox:
            inbox.append(SMS.fromJson(sms_json))

# retrieve new messages from the modem and add to the inbox
for m in em7345.getSMS():
    inbox.append(m)

# count any unread/new
unread_count = len([m for m in inbox if not m.read])

# serialise and save back into inbox.json
with open(inbox_path, "w") as inbox_file:
    inbox_file.write(json.dumps([m.toJson() for m in inbox]))

# clear the messages from the SIM
em7345.deleteAllSMS()

# finally print the summary so xmobar can pick it up
# note: assumes font-awesome is initialised as font #1
if unread_count:
    print("<fn=1>%s</fn> (%d)" % (envelope, unread_count))
else:
    print("<fn=1>%s</fn>" % (envelope_empty))
