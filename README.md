# xsms

a simple SMS client for xmobar, which uses the em73xx library

## TODO

* make a tabbed interface - Inbox/Sent/Compose, self descriptive
* clean-up the UI, make it match the xmonad style I have and give inbox a scrollbar
* date time!
* maybe "derp" isn't the best name for the method initialising the UI - and does it need to be a separate module?

NOTE: NOT YET IN PYPI, ALL THIS IS JUST PLACEHOLDER DOCS!!

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

Then you can launch it standalone:
```
$ python -m xsms --device=/dev/ttyACM0
```

or add it to xmobar

(TODO)

## Using

(TODO)