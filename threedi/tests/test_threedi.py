from threedi import (
    API,
)

api = API()


def test_smoke():
    assert isinstance(api.foo, API)
    assert isinstance(api.foo.bar, API)


def test_http_method():
    assert not isinstance(api.foo.get, API)
    assert not isinstance(api.foo.post, API)
