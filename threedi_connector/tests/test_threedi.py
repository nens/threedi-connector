from threedi_connector import API

api = API()


def test_api_traversal():
    assert isinstance(api.foo.bar, API)
    assert api.foo.bar._cache == ['foo', 'bar']


def test_using_reserved_python_keywords():
    endpoint = api.foo._('for').bar
    assert isinstance(endpoint, API)
    assert endpoint._cache == ['foo', 'for', 'bar']


def test_http_methods():
    assert not callable(api.foo)  # smoke test
    assert callable(api.foo.get)
    assert callable(api.foo.post)
