from setuptools import setup

current_version = '0.3'

setup(
    name = 'xsms',
    packages = [ 'xsms' ], #, 'xsms.test' ],
    version = current_version,
    description = 'lightweight SMS reader/composer for systems with access to a Sierra em73xx modem (like the Thinkpad X250), with simple xmobar integration',
    author = 'Sean McLemon',
    author_email = 'sean.mclemon@gmail.com',
    url = 'https://github.com/smcl/xsms',
    download_url = 'https://github.com/smcl/xsms/tarball/%s' % (current_version),
    keywords = ['thinkpad', 'em7345', 'em73xx', 'sms', 'xmonad', 'xmobar'],
    classifiers = [],
    #test_suite='xsms.test.all',
    install_requires=[
        'unittest2',
        'em73xx'
    ],
    setup_requires=[
        'unittest2',
        'em73xx'
    ],

)
