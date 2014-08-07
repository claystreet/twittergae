"""
Copyright (c) 2014 Clay Street Online LLC
http://www.claystreet.com

MIT License
http://opensource.org/licenses/MIT

Performs simple OAuth1 HTTP header initialization
Note:
   Doesn't account for corner cases such as duplicate parameter names etc.
   BUT many services such as twitter don't support this anyway
"""

import hashlib
import hmac
import base64
import time

import string
import random

__all__ = [
    'random_token',
    'percent_encode',
    'percent_encode_dict',
    'OAuth1',
]


ASCII_DIGITS = string.ascii_letters + string.digits

rand = random.SystemRandom()

def random_token(length):
    """ Returns a random alphanumeric string of "length" chars """
    return ''.join([rand.choice(ASCII_DIGITS) for _ in range(length)])


dont_percent_encode = dict.fromkeys(bytearray(ASCII_DIGITS + '-._~'), True)

def percent_encode(utf8_str):
    """ Percent (URL) encodes everything except alphanumeric, dash, period, underscore, and tilde """
    if not utf8_str:
        return utf8_str
    byte_str = bytearray(utf8_str, 'utf-8')
    return ''.join(map(lambda x: chr(x) if x in dont_percent_encode else '%{:02X}'.format(x), byte_str))


def percent_encode_dict(idict):
    """ Returns a dict with all keys and values in idict percent encoded
    """
    if not idict:
        return {}

    return { percent_encode(name): percent_encode(str(val)) for name, val in idict.iteritems() }


class OAuth1(object):
    """
    Provides the ability to send an OAuth 1.0 HTTP request

    Initializes the 'Authorization' header from the request parameters.

    Initialization requires:
        consumer_key, consumer_secret_key = Application/Developer keys
            Identify the application/developer requesting access to an OAuth1 service.
            Assigned by an OAuth1 service to an application/developer

        access_token, access_secret_token
            Access tokens granted to the application by a user of an OAuth1 service.
            The user may be the application/developer itself or the application may be granted
            access tokens (with a certain level of privilege) by another user
    """
    def __init__(self, consumer_key=None, consumer_secret_key=None, access_token=None, access_secret_token=None):
        self.consumer_key = None
        self.consumer_secret_key = None
        self.access_token = None
        self.access_secret_token = None

        self.oauth_version = '1.0'
        self.signature_method = 'HMAC-SHA1'

        self.__call__(consumer_key=consumer_key,
                      consumer_secret_key=consumer_secret_key,
                      access_token=access_token,
                      access_secret_token=access_secret_token)

    def __call__(self, consumer_key=None, consumer_secret_key=None, access_token=None, access_secret_token=None):
        if consumer_key is not None:
            self.consumer_key = consumer_key
        if consumer_secret_key is not None:
            self.consumer_secret_key = consumer_secret_key
        if access_token is not None:
            self.access_token = access_token
        if access_secret_token is not None:
            self.access_secret_token = access_secret_token


    def init_request(self, method, url, query_vars=None, post_vars=None, headers=None, multipart=False):
        """
        Initializes an OAuth1 HTTP request given:
            method = HTTP method
            url = Base URL WITHOUT query string parameters
            query_vars = A dict of query string variables (name/value pairs not percent encoded... just the raw values)
            post_vars = A dict of post variables (name/value pairs not percent encoded... just the raw values)
            headers = Optional HTTP headers... the OAuth 'Authorization' header WILL be inserted after making this call

        Returns:
            method = HTTP method
            url = The request URL with percent encoded query string params
            payload = The POST payload (percent encoded and ready to POST), None if not a POST request
            headers = The HTTP headers including the OAuth 'Authorization' header
        """
        method = method.upper()  # ensure uppercase

        # All the auth params except the signature
        auth_header_params = {
            'oauth_consumer_key': self.consumer_key,
            'oauth_nonce': random_token(42),
            'oauth_timestamp': str(int(time.time())),
            'oauth_signature_method': self.signature_method,
            'oauth_version': self.oauth_version,
            'oauth_token': self.access_token,
        }
        if hasattr(self, 'test_nonce'):
            auth_header_params['oauth_nonce'] = self.test_nonce
        if hasattr(self, 'test_timestamp'):
            auth_header_params['oauth_timestamp'] = self.test_timestamp

        # Percent encoded copies of the request params
        enc_query_vars = percent_encode_dict(query_vars)
        if not multipart:
            enc_post_vars = percent_encode_dict(post_vars)
        else:
            enc_post_vars = post_vars  # no encoding with multipart
        enc_auth_header_params = percent_encode_dict(auth_header_params)

        auth_signature_params = {}
        auth_signature_params.update(enc_query_vars)
        if not multipart:
            auth_signature_params.update(enc_post_vars)
        auth_signature_params.update(enc_auth_header_params)

        signature_str = '&'.join([
            method,
            percent_encode(url),
            percent_encode(
                '&'.join([name + '=' + auth_signature_params[name] for name in sorted(auth_signature_params.keys())])
            )
        ]).encode('utf-8')

        signing_key = '&'.join([
            percent_encode(self.consumer_secret_key or ''),
            percent_encode(self.access_secret_token or '')
        ])

        oauth_signature = base64.b64encode(hmac.new(signing_key, signature_str, hashlib.sha1).digest())

        auth_header_params['oauth_signature'] = percent_encode(oauth_signature)

        auth_header = ', '.join(['{:}="{:}"'.format(name, auth_header_params[name])
                                 for name in sorted(auth_header_params.keys())])

        if headers is None:
            headers = {}
        headers['Authorization'] = 'OAuth ' + auth_header

        if query_vars:
            url += '?' + '&'.join([name + '=' + val for name, val in enc_query_vars.iteritems()])

        if post_vars:
            if not multipart:
                payload = '&'.join([name + '=' + val for name, val in enc_post_vars.iteritems()])
            else:
                boundary_str = '=====' + random_token(42) + '====='
                headers['Content-Type'] = 'multipart/form-data; boundary=' + boundary_str

                boundary_str = '--' + boundary_str
                param_template = boundary_str + '\r\nContent-Disposition: form-data; name="{:}"\r\n\r\n{:}\r\n'
                data_template = ''.join([
                    boundary_str,
                    '\r\nContent-Disposition: form-data; name="{:}"; filename="{:}"\r\n',
                    'Content-Type: {:}\r\n',
                    'Content-Transfer-Encoding: {:}\r\n\r\n',
                ])
                payload_data = []

                for name, val in enc_post_vars.iteritems():
                    # If an ordinary parameter...
                    if not isinstance(val, dict):
                        payload_data.append(param_template.format(name, val))
                    # If a data parameter...
                    else:
                        if 'filename' in val:
                            fname = val['filename']
                        else:
                            fname = ''

                        if 'mimetype' in val:
                            mimetype = val['mimetype']
                        else:
                            mimetype = 'image/jpeg'

                        if 'encoding' in val:
                            encoding = val['encoding']
                        else:
                            encoding = 'binary'

                        # The multipart header
                        payload_data.append(data_template.format(name, fname, mimetype, encoding))

                        # Append the data
                        payload_data.append(val['data'])
                        payload_data.append('\r\n')

                payload_data.append(boundary_str + '--')
                payload = ''.join(payload_data)

        else:
            payload = None

        return method, url, payload, headers
