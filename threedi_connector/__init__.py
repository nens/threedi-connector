import datetime
import json

from . import requests
from .compat import urljoin, basestring
from .decorators import authenticate_interactively, add_auth_creds_from_self
from .helpers import Credentials, get_credentials_interactively

HOST_STAGING = "https://staging.3di.lizard.net/"
HOST_PRODUCTION = "https://3di.lizard.net/"

DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%f"
DATETIME_FORMAT_WITH_Z = "%Y-%m-%dT%H:%M:%S.%fZ"
DATETIME_FORMAT_NO_MS = "%Y-%m-%dT%H:%M:%SZ"

# all the formats I can think of atm
DATETIME_FORMATS = [
    DATETIME_FORMAT,
    DATETIME_FORMAT_WITH_Z,

    # this one is in ``data_json``, which is hard to parse for now
    # DATETIME_FORMAT_NO_MS,
]


def deserialize_datetime(pairs, dt_formats=None):
    """Hook for json.load/json.loads to deserialize datetimes."""
    if dt_formats is None:
        dt_formats = DATETIME_FORMATS

    d = {}
    for k, v in pairs:
        if isinstance(v, basestring):
            # try to parse a possible datetime string
            for dt_format in dt_formats:
                try:
                    v = datetime.datetime.strptime(v, dt_format)
                    break
                except ValueError:
                    pass
        d[k] = v
    return d


# Inspiration by: https://sendgrid.com/blog/using-python-to-implement-a-fluent-interface-to-any-rest-api/  # noqa
class API(object):
    """
    3Di API interface
    """
    def __init__(self, cache=None, host=HOST_STAGING, version='v1'):
        # schema_url = urljoin(host, "api/v1/docs/")
        # endpoint_data = requests.get(
        #     schema_url, headers={'Accept': 'application/coreapi+json'}
        # )
        # if schema_url:
        #     self.endpoints = json.loads(endpoint_data)
        self.host = host
        self.base_url = self.host + 'api/{}/'.format(version)
        self._cache = cache or []
        self.__creds = None  # set by ``API.authenticate``

    # Build the cache, and handle special cases
    def _(self, name):
        # Enables method chaining
        new_api_obj = API(cache=self._cache+[name], host=self.host)
        # we need to pass on all information (like creds) to the new objects,
        # because they don't know anything about the 'parent' object, which is
        # kinda convoluted. TODO: maybe think of a better solution?
        new_api_obj._API__creds = self.__creds  # name mangling again...
        return new_api_obj

    def _build_url(self, append_slash=True):
        url = urljoin(self.base_url, "/".join(self._cache))
        if append_slash and not url.endswith('/'):
            url = url + '/'
        return url

    # Final method call
    def method(self):
        return self._cache

    @add_auth_creds_from_self
    @authenticate_interactively
    def get(self, params=None, headers=None, auth=None):
        """GET request."""
        url = self._build_url()
        return requests.get(url, params=params, headers=headers, auth=auth)

    @add_auth_creds_from_self
    @authenticate_interactively
    def post(self, data=None, headers=None, auth=None):
        """POST request."""
        url = self._build_url()
        return requests.post(url, data=data, headers=headers, auth=auth)

    @add_auth_creds_from_self
    @authenticate_interactively
    def options(self, params=None, headers=None, auth=None):
        """OPTIONS request."""
        url = self._build_url()
        return requests.options(url, params=params, headers=headers, auth=auth)

    @add_auth_creds_from_self
    @authenticate_interactively
    def head(self, params=None, headers=None, auth=None):
        """HEAD request."""
        url = self._build_url()
        return requests.head(url, params=params, headers=headers, auth=auth)

    def authenticate(self, username=None, password=None):
        """Set credentials to the API object so we don't have to ask anymore.
        """
        if username is None or password is None:
            creds = get_credentials_interactively()
        else:
            creds = Credentials(username, password)
        # name mangled for extra obfuscation, cuz why tf not
        self.__creds = creds

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
            host=HOST_STAGING,
            **sim_kwargs):
        self.sim_kwargs = sim_kwargs
        self.host = host
        self._api = API(host=host)
        self.info = None

    def authenticate(self, *args, **kwargs):
        """Just calls the API authentication."""
        self._api.authenticate(*args, **kwargs)

    def start(self):
        """Start the simulation."""
        info = self._api.calculation.start.post(data=self.sim_kwargs)
        self.info = json.loads(info)
        return self.info

    @classmethod
    def from_subgrid_id(cls, subgrid_id):
        raise NotImplementedError("boe")


class SimulationManager(object):
    """
    Manage saved states, queued simulations, etc.
    """
    def __init__(self, host=HOST_STAGING):
        self.host = host
        self._api = API(host=host)

    def authenticate(self, *args, **kwargs):
        """Just calls the API authentication."""
        self._api.authenticate(*args, **kwargs)

    @property
    def queued_tasks(self):
        """Show tasks in the queue."""
        data = self._api.startmachinetasks.get()
        return json.loads(data, object_pairs_hook=deserialize_datetime)

    @property
    def saved_states(self):
        data = self._api.threedimodelsavedstates.get()
        return json.loads(data, object_pairs_hook=deserialize_datetime)


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
