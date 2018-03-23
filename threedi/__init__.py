from functools import wraps
import getpass
import json

from . import requests
from .compat import (
    urljoin,
    PY2,
)

if not PY2:
    raw_input = input

API_HOST_STAGING = "https://staging.3di.lizard.net/"
API_HOST_PRODUCTION = "https://3di.lizard.net/"

DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%f"


def get_credentials_interactively():
    username = raw_input("Username: ")
    password = getpass.getpass("Password: ")
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


def add_creds_from_self(func):
    @wraps(func)
    def func_wrapper(*args, **kwargs):
        pass
        # TODO
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
    def get(self, params=None, headers=None, auth=None):
        """GET request."""
        url = self._build_url()
        return requests.get(url, params=params, headers=headers, auth=auth)

    @authenticate_interactively
    def post(self, data=None, headers=None, auth=None):
        """POST request."""
        url = self._build_url()
        return requests.post(url, data=data, headers=headers, auth=auth)

    @authenticate_interactively
    def options(self, params=None, headers=None, auth=None):
        """OPTIONS request."""
        url = self._build_url()
        return requests.options(url, params=params, headers=headers, auth=auth)

    @authenticate_interactively
    def head(self, params=None, headers=None, auth=None):
        """HEAD request."""
        url = self._build_url()
        return requests.head(url, params=params, headers=headers, auth=auth)

    def set_credentials(self, username=None, password=None, interactive=True):
        """Set credentials to the API object so we don't have to ask anymore.
        """
        if interactive:
            username, password = get_credentials_interactively()

        # mangle them names for extra obfuscation
        self.__username = username
        self.__password = password
        raise NotImplementedError(
            "todo: make @authenticate_interactively aware of credentials")

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
            host=API_HOST_STAGING,
            **sim_kwargs):
        self.sim_kwargs = sim_kwargs
        self.host = host
        self._api = API(host=host)
        self._calc_endpoint = self._api.calculation.start
        self.info = None

    def start(self):
        """Start the simulation."""
        info = self._calc_endpoint.post(data=self.sim_kwargs)
        self.info = json.loads(info)
        return self.info

    @classmethod
    def from_subgrid_id(cls, subgrid_id):
        raise NotImplementedError("boe")


class SimulationManager(object):
    """
    Manage saved states, queued simulations, etc.
    """
    def __init__(self, host=API_HOST_STAGING):
        self.host = host
        self._api = API(host=host)
        self._tasks_endpoint = self._api.startmachinetasks
        self._saved_states_endpoint = self._api.threedimodelsavedstates

    @property
    def queued_tasks(self):
        """Show tasks in the queue."""
        data = self._tasks_endpoint.get()
        return json.loads(data)

    @property
    def saved_states(self):
        data = self._saved_states_endpoint.get()
        return json.loads(data)


def start_simulation(*args, **kwargs):
    """Start a Simulation and return the instance."""
    sim = Simulation(*args, **kwargs)
    sim.start()
    print("Simulation started.")
    return sim


# for testing purposes
TEST_KWARGS = {
    "organisation_uuid": "61f5a464c35044c19bc7d4b42d7f58cb",
    "model_slug": "v2_bergermeer-v2_bergermeer_bres_maalstop-55-784c561ecebf9433cd7beb8b6a22a14f2841cda4",
    "start": "2016-10-18T00:00",
    "end": "2016-10-18T00:30",
    "scenario_name": "test-lib (this result can be deleted)",
}
