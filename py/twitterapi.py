"""
Copyright (c) 2014 Clay Street Online LLC
http://www.claystreet.com

MIT License
http://opensource.org/licenses/MIT

Base Twitter API class
"""

from gae_send_request import send_request, send_request_async, send_request_ndb
from oauth import OAuth1
import json

__all__ = [
    'tbool',
    'twitter_response',
    'TwitterApi',
]


def twitter_response(urlfetch_response):
    """
        Adds a 'twitter' member to the urlfetch_response object
        The 'twitter' member is a python dict of the decoded twitter json response
    """
    # If there's any content... (regardless of the status)
    if urlfetch_response.content:
        try:
            urlfetch_response.twitter = json.loads(urlfetch_response.content)
        except Exception:
            urlfetch_response.twitter = None
    return urlfetch_response


def tbool(val):
    # Ensures bool parameters are twitter/json friendly
    return str(val).lower()


class TwitterApi(object):
    """
    Base class for accessing the twitter 1.1 API
    """
    def __init__(self, consumer_key=None, consumer_secret_key=None, access_token=None, access_secret_token=None):
        self.oauth = OAuth1(consumer_key=consumer_key,
                            consumer_secret_key=consumer_secret_key,
                            access_token=access_token,
                            access_secret_token=access_secret_token)
        self.api_base_url = 'https://api.twitter.com/1.1/'

    def send_request(self, method, url, query_vars=None, post_vars=None, async=None, multipart=False):
        """
        Sends a twitter API request
        """

        method, url, payload, headers = self.oauth.init_request(method, url, query_vars=query_vars,
                                                                post_vars=post_vars, multipart=multipart)

        if async is True or async == 'rpc':
            return send_request_async(method, url, payload, headers)
        elif async == 'ndb':
            return send_request_ndb(method, url, payload, headers)
        else:
            return twitter_response(send_request(method, url, payload, headers))
