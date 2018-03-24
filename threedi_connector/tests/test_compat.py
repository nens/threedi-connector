from threedi_connector import compat


def test_compat_availability():
    """Test if all members are available."""
    compat.PY2
    compat.urljoin
    compat.urlencode
    compat.urllib_request
    compat.urlopen
    compat.basestring
