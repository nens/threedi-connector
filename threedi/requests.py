"""
Most of this is copied from: https://github.com/lizardsystem/lizard-connector
"""
import base64
import json

from .compat import (
    urlencode,
    urllib_request,
    urlopen,
)


def get_authorization_headers(username, password):
    """
    Basic authentication, see this recipe:
    http://www.voidspace.org.uk/python/articles/authentication.shtml
    """
    creds = '%s:%s' % (username, password)
    # PY3 expects bytes, thus we need to do ``encode()``
    bytes_like = creds.encode()
    base64string = base64.b64encode(bytes_like)
    return {"Authorization": "Basic %s" % base64string}


def perform_request(url, data=None, headers=None, auth=None, method=None):
    """
    GETs parameters from the Lizard api or POSTs data to the Lizard api.
    Defaults to GET request. Turns into a POST request if data is provided.
    Args:
        url (str): full query url: should be of the form:
                   [base_url]/api/v2/[endpoint]/?[query_key]=[query_value]&
                       ...
        data (dict): data in a list or dictionary format.
        auth (tuple): A tuple containing (username, password) for basic
            authentication.
        method (str): HTTP method
    Returns:
        HTTP response
    """
    if headers is None:
        headers = {}

    if auth:
        username, password = auth
        auth_header = get_authorization_headers(username, password)
        headers.update(auth_header)

    if data:
        headers['content-type'] = "application/json"
        request_obj = urllib_request.Request(
            url,
            headers=headers,
            data=json.dumps(data).encode('utf-8'),
        )
    else:
        request_obj = urllib_request.Request(url, headers=headers)

    if method is not None:
        assert method in ['HEAD', 'DELETE', 'OPTIONS', 'GET', 'POST'], \
            "Unknown method: %s" % method
        request_obj.get_method = lambda: method

    resp = urlopen(request_obj)
    return resp


def post(url, data=None, headers=None, auth=None):
    """
    POST data to the api.
    Args:
        url (str): Lizard-api valid endpoint url.
        uuid (str): UUID of the object in the database you wish to store
                    data to.
        data (dict): Dictionary with the data to post to the api
    """
    resp = perform_request(url, data=data, headers=headers, auth=auth)
    content = resp.read().decode('UTF-8')
    return content


def get(url, params=None, headers=None, auth=None):
    if params:
        url = url + '?' + urlencode(params)
    resp = perform_request(url, headers=headers, auth=auth)
    content = resp.read().decode('UTF-8')
    return content


def options(url, params=None, headers=None, auth=None):
    if params:
        url = url + '?' + urlencode(params)
    resp = perform_request(url, headers=headers, auth=auth, method='OPTIONS')
    content = resp.read().decode('UTF-8')
    return content


def head(url, params=None, headers=None, auth=None):
    # TODO: head should not return body, but the headers, we should wrap
    # things in an object or something
    if params:
        url = url + '?' + urlencode(params)
    resp = perform_request(url, headers=headers, auth=auth, method='HEAD')
    return resp
    # content = resp.read().decode('UTF-8')
    # return content
