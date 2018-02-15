"""
Most of this is copied from: https://github.com/lizardsystem/lizard-connector
"""
import base64
import json
import sys

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


def get_authorization_headers(username, password):
    base64string = base64.b64encode('%s:%s' % (username, password))
    return {"Authorization": "Basic %s" % base64string}


def perform_request(url, data=None, headers={}, auth=None):
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
    Returns:
        a dictionary with the response.
    """
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
    resp = urlopen(request_obj)
    content = resp.read().decode('UTF-8')
    return content
    # return json.loads(content)


def post(url, data=None, headers={}, auth=None):
    """
    POST data to the api.
    Args:
        url (str): Lizard-api valid endpoint url.
        uuid (str): UUID of the object in the database you wish to store
                    data to.
        data (dict): Dictionary with the data to post to the api
    """
    return perform_request(url, data=data, headers=headers, auth=auth)


def get(url, params=None, headers={}, auth=None):
    if params:
        url = url + '?' + urlencode(params)
    return perform_request(url, headers=headers, auth=auth)
