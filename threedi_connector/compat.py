"""
py2/py3 compatibility helpers
"""
import sys

PY2 = sys.version_info.major == 2

if PY2:
    from urllib import urlencode  # noqa
    from urlparse import urljoin  # noqa
    import urllib2 as urllib_request  # noqa
    from urllib2 import urlopen  # noqa
    basestring = basestring
else:  # it's py3 (or higher)
    from urllib.parse import urlencode  # noqa
    from urllib.parse import urljoin  # noqa
    import urllib.request as urllib_request  # noqa
    from urllib.request import urlopen  # noqa
    basestring = str
