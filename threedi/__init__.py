from functools import wraps
import getpass
import json
import sys

from . import requests

if sys.version_info.major < 3:
    # py2
    from urllib import urlencode
    from urlparse import urljoin
    import urllib2 as urllib_request
    from urllib2 import urlopen
else:
    # py3
    from urllib.parse import urlencode
    from urllib.parse import urljoin
    import urllib.request as urllib_request
    from urllib.request import urlopen


API_HOST_STAGING = "https://staging.3di.lizard.net/"
API_HOST_PRODUCTION = "https://3di.lizard.net/"


def get_credentials_interactively():
    username = raw_input("Username: ")
    password = getpass.getpass()
    return username, password


def authenticate_interactively(func):
    """
    Require authentication as default, and ask via stdin for username/pw
    if it isn't supplied. Authentication can still be disabled by passing
    ``use_auth=False``.
    """
    @wraps(func)
    def func_wrapper(*args, **kwargs):
        """
        Wraps a HTTP method function

        This wrapper introduces the following extra kwargs:
            use_auth (bool): enable or disable authentication completely.
                Default: True
        """
        use_auth = kwargs.pop('use_auth', True)
        if use_auth:
            auth = kwargs.get('auth')
            if not auth:
                kwargs['auth'] = get_credentials_interactively()
        return func(*args, **kwargs)
    return func_wrapper


# Inspiration by: https://sendgrid.com/blog/using-python-to-implement-a-fluent-interface-to-any-rest-api/  # noqa
class API(object):
    """
    3Di API interface
    """
    def __init__(self, cache=None, host=API_HOST_STAGING, version='v1'):
        # schema_url = urljoin(host, "api/v1/docs/")
        # endpoint_data = requests.get(
        #     schema_url, headers={'Accept': 'application/coreapi+json'}
        # )
        # if schema_url:
        #     self.endpoints = json.loads(endpoint_data)
        self.host = host
        self.base_url = self.host + 'api/{}/'.format(version)
        self._cache = cache or []

    # Build the cache, and handle special cases
    def _(self, name):
        # Enables method chaining
        return API(cache=self._cache+[name], host=self.host)

    def _build_url(self, append_slash=True):
        url = urljoin(self.base_url, "/".join(self._cache))
        if append_slash and not url.endswith('/'):
            url = url + '/'
        return url

    # Final method call
    def method(self):
        return self._cache

    @authenticate_interactively
    def get(self, params=None, headers={}, auth=None):
        """GET request."""
        url = self._build_url()
        return requests.get(url, params=params, headers=headers, auth=auth)

    @authenticate_interactively
    def post(self, data=None, headers={}, auth=None):
        """POST request."""
        url = self._build_url()
        return requests.post(url, data=data, headers=headers, auth=auth)

    # Reflection
    def __getattr__(self, name):
        return self._(name)

    # Called with the object is deleted
    # def __del__(self):
    #     print('Deleting Myself')


class Simulation(object):
    """
    Run and track a simulation using the 3Di API.
    """
    def __init__(
            self,
            # model_slug,
            # organisation_uuid,
            # start,
            # end,
            # scenario_name,
            # email=None,
            # result_uuid=None,
            # rain_events=None,
            # wind_events=None,
            # breaches=None,
            # save_states=None,
            # use_saved_state=None,
            # store_results=None,
            **sim_kwargs):
        self.sim_kwargs = sim_kwargs
        self._api = API()
        self._calc_endpoint = self._api.calculation.start
        self._tasks = self._api.startmachinetasks
        self.info = None

    def start(self):
        info = self._calc_endpoint.post(data=self.sim_kwargs)
        self.info = json.loads(info)
        return self.info

    def tasks_in_queue(self):
        data = self._tasks.get()
        return json.loads(data)


def start_simulation(*args, **kwargs):
    """Start a Simulation and return the instance."""
    sim = Simulation(*args, **kwargs)
    sim.start()
    return sim


# for testing purposes
TEST_KWARGS = {
    "organisation_uuid": "61f5a464c35044c19bc7d4b42d7f58cb",
    "model_slug": "v2_bergermeer-v2_bergermeer_bres_maalstop-55-784c561ecebf9433cd7beb8b6a22a14f2841cda4",
    "start": "2016-10-18T00:00",
    "end": "2016-10-18T00:30",
    "scenario_name": "test-lib (this result can be deleted)",
}
