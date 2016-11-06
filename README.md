# xsms

A simple SMS client written in Python + Tkinter which uses the em73xx library. Originally written for my Thinkpad X250 (which uses this chip) it was mainly written for use with xmobar - with a text-mode summary so you can quickly see any unread messages, and a lightweight GUI to read and send messages.

## TODO

* clean-up the UI, make it match the xmonad style I have (using ttk style in xsms/style.py)
* reply, mark as [un]read, delete/archive functionality

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

## Using

Once xsms is installed you can either launch it standalone ...

```
$ python -m xsms --device=/dev/ttyACM0
```

... or add it to xmobarrc, like the below (which takes advantage of the ability to specify the font via <fn> tags to easily get some icons from Font Awesome):

```
  -- assumes you have Font Awesome installed and used here:
  -- additionalFonts = ["xft:FontAwesome-10"],
  Run Com "/usr/bin/python" [ "-m", "xsms", "-d", "/dev/ttyACM0", "-p", "1234", "-r", "<fn=1></fn>", "-u", "<fn=1></fn> %d" ] "xsms" 600,
```

This will result in an xmobar entry like the below:

![xsms-xmobar.png](xsms-xmobar.png?raw=true)

... and if you want to be able to click the icon to raise the GUI, you can:
```
  template = "%StdinReader% }{ ... stuff ... <action=`python -m xsms -g -d /dev/ttyACM0 -p 1234`>%xsms%</action> ... "
```

![xsms-inbox.png](xsms-inbox.png?raw=true)

For a quick reference of the switches and parameters supported, invoke `python -m xms --help`:
```
$ python -m xsms --help
usage: __main__.py [-h] [-d DEVICE] [-g] [-p PIN] [-r READ_FORMAT]
                   [-u UNREAD_FORMAT]

xsms - an sms client for linux systems with an em73xx modem

optional arguments:
  -h, --help            show this help message and exit
  -d DEVICE, --device DEVICE
  -g, --gui
  -p PIN, --pin PIN
  -r READ_FORMAT, --read_format READ_FORMAT
  -u UNREAD_FORMAT, --unread_format UNREAD_FORMAT
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

... then it's possible that the ModemManager service is accessing the device already. It's not currently possible to use em73xx together with the modem. You can kill it off and retry:

```
$ sudo systemctl stop ModemManager
$ python -m xsms --device /dev/ttyACM0 --pin 1234
5
```
