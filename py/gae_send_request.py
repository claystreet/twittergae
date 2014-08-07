"""
Copyright (c) 2014 Clay Street Online LLC
http://www.claystreet.com

MIT License
http://opensource.org/licenses/MIT

Three simple functions to send HTTP requests from a GAE App
"""

from google.appengine.api import urlfetch
from google.appengine.ext import ndb

__all__ = [
    'send_request',
    'send_request_async',
    'send_request_ndb',
]


def send_request(method, url, payload=None, headers=None, **kwargs):
    """
        Sends a request synchronously via urlfetch.fetch()
        Returns the urlfetch Response object
        To get the urlfetch Response object with the twitter json response data initialized:
            response = twitter_response(response)
    """
    if headers is None:
        headers = {}

    return urlfetch.fetch(url=url, method=method, payload=payload, headers=headers, **kwargs)


def send_request_async(method, url, payload=None, headers=None, **kwargs):
    """
        Sends a request asynchronously via urlfetch.create_rpc() & urlfetch.make_fetch_call()
        Returns the urlfetch rpc object
            To get the urlfetch Response object:
                response = rpc.get_result()
            To get the urlfetch Response object with the twitter json response data initialized:
                response = twitter_response(rpc.get_result())
    """

    if headers is None:
        headers = {}

    rpc = urlfetch.create_rpc()
    return urlfetch.make_fetch_call(rpc, url=url, method=method, payload=payload, headers=headers, **kwargs)


@ndb.tasklet
def send_request_ndb(method, url, payload=None, headers=None, **kwargs):
    """
        Sends a request asynchronously via ndb's tasklet friendly urlfetch()
        Returns an ndb Future
            To get the urlfetch Response object:
                response = future.get_result()
            To get the urlfetch Response object with the twitter json response data initialized:
                response = twitter_response(future.get_result())
    """
    if headers is None:
        headers = {}

    ctx = ndb.get_context()
    result = yield ctx.urlfetch(url=url, method=method, payload=payload, headers=headers, **kwargs)
    raise ndb.Return(result)
