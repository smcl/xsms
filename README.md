# xsms

A simple SMS client written in Python + Tkinter which uses the em73xx library. Primary use is for xmonad and xmobar.

## TODO

* clean-up the UI, make it match the xmonad style I have and give inbox a scrollbar
* refresh the outbox when you have sent a message
* fill out the (TODO) sections below

## Install

Either retrieve from pypi using pip:

```
$ pip install xsms
```

or clone this repo, and install using `setup.py`:
```
$ git clone https://github.com/smcl/xsms
$ cd xsms
$ python setup.py install
```

Then you can either launch it standalone ...

```
$ python -m xsms --device=/dev/ttyACM0
```

... or add it to xmobarrc

```
      Run Com "/usr/bin/python" [ "python", "-m", "xsms", "--device", "/dev/ttyACM0", "--pin", "1234" ] "xsms" 600,
```

(TODO)

## Using

(TODO - do more than dump --help)

```
$ python -m xsms --help
usage: __main__.py [-h] [--device DEVICE] [--gui] [--pin PIN]
                   [--read_format READ_FORMAT] [--unread_format UNREAD_FORMAT]

xsms - an sms client for linux systems with an em73xx modem

optional arguments:
  -h, --help            show this help message and exit
  --device DEVICE       the modem device, like /dev/ttyACM0
  --gui                 show the SMS gui
  --pin PIN             the pin for the SMS
  --read_format READ_FORMAT
                        string to print if there are no unread messages
  --unread_format UNREAD_FORMAT
                        format string to print if there are unread messages

```

## Problems

If you've having a problem like the below...

```
$ python -m xsms --device /dev/ttyACM0 --pin 1234
Traceback (most recent call last):
  File "/usr/lib/python2.7/runpy.py", line 174, in _run_module_as_main
      "__main__", fname, loader, pkg_name)
  File "/usr/lib/python2.7/runpy.py", line 72, in _run_code
      exec code in run_globals
  File "/home/sean/dev/py/xsms/xsms/__main__.py", line 63, in <module>
      modem = Modem(args.device, pin=args.pin)
  File "/usr/local/lib/python2.7/dist-packages/em73xx-0.5-py2.7.egg/em73xx/modem.py", line 23, in __init__
module>
      self.device = serial.Serial(dev, bps, timeout=1)
  File "/usr/lib/python2.7/dist-packages/serial/serialutil.py", line 182, in __init__
      self.open()
  File "/usr/lib/python2.7/dist-packages/serial/serialposix.py", line 247, in open
      raise SerialException(msg.errno, "could not open port {}: {}".format(self._port, msg))
serial.serialutil.SerialException: [Errno 16] could not open port /dev/ttyACM0: [Errno 16] Device or resource busy: '/dev/ttyACM0'
```

... then it's possible that the ModemManager service is accessing the device already. Kill it off and retry:

```
$ sudo systemctl stop ModemManager
$ python -m xsms --device /dev/ttyACM0 --pin 1234
5
```
