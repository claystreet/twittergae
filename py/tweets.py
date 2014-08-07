"""
Copyright (c) 2014 Clay Street Online LLC
http://www.claystreet.com

MIT License
http://opensource.org/licenses/MIT

Provides access to the twitter API from Google App Engine apps written in python.
"""

from twitterapi import TwitterApi, tbool

__all__ = [
    'Tweets',
]


class Tweets(TwitterApi):
    """
    Tweet related twitter API interface
    """

    # Send a tweet
    def update(self,
               status,  # The tweet text (140 twitter-count chars)
               in_reply_to_status_id=None,
               possibly_sensitive=None,
               lat=None,
               long=None,
               place_id=None,
               display_coordinates=None,
               trim_user=None,
               async=None):

        # Initialize the POST vars for this request
        api_vars = {
            'status': status,
        }
        if in_reply_to_status_id is not None:
            api_vars['in_reply_to_status_id'] = in_reply_to_status_id
        if possibly_sensitive is not None:
            api_vars['possibly_sensitive'] = tbool(possibly_sensitive)
        if lat is not None:
            api_vars['lat'] = lat
        if long is not None:
            api_vars['long'] = long
        if place_id is not None:
            api_vars['place_id'] = place_id
        if display_coordinates is not None:
            api_vars['display_coordinates'] = tbool(display_coordinates)
        if trim_user is not None:
            api_vars['trim_user'] = tbool(trim_user)

        url = self.api_base_url + 'statuses/update.json'
        return self.send_request('POST', url, post_vars=api_vars, async=async)


    # Send a tweet and upload a photo
    def update_with_media(self,
                          status,  # The tweet text (140 twitter-count chars)
                          media,  # A dict containing 'filename', 'mimetype', 'encoding', 'data'
                          in_reply_to_status_id=None,
                          possibly_sensitive=None,
                          lat=None,
                          long=None,
                          place_id=None,
                          display_coordinates=None,
                          async=None):

        # Initialize the POST vars for this request
        api_vars = {
            'status': status,
            'media[]': media,
        }
        if in_reply_to_status_id is not None:
            api_vars['in_reply_to_status_id'] = in_reply_to_status_id
        if possibly_sensitive is not None:
            api_vars['possibly_sensitive'] = tbool(possibly_sensitive)
        if lat is not None:
            api_vars['lat'] = lat
        if long is not None:
            api_vars['long'] = long
        if place_id is not None:
            api_vars['place_id'] = place_id
        if display_coordinates is not None:
            api_vars['display_coordinates'] = tbool(display_coordinates)

        url = self.api_base_url + 'statuses/update_with_media.json'
        return self.send_request('POST', url, post_vars=api_vars, async=async, multipart=True)


    # retweet
    def retweet(self,
                id,  # The tweet id
                trim_user=None,
                async=None):

        # Initialize the POST vars for this request
        api_vars = {}
        if trim_user is not None:
            api_vars['trim_user'] = tbool(trim_user)

        url = self.api_base_url + 'statuses/retweet/{:s}.json'.format(id)
        return self.send_request('POST', url, post_vars=api_vars, async=async)


    # Destroy a tweet
    def destroy(self,
                id,  # The tweet id
                trim_user=None,
                async=None):

        # Initialize the POST vars for this request
        api_vars = {}
        if trim_user is not None:
            api_vars['trim_user'] = tbool(trim_user)

        url = self.api_base_url + 'statuses/destroy/{:s}.json'.format(id)
        return self.send_request('POST', url, post_vars=api_vars, async=async)


    # Get the tweet with the specified id
    def show(self,
             id,  # numeric tweet id
             trim_user=None,
             include_my_retweet=None,
             include_entities=None,
             async=None):

        api_vars = {
            'id': id,
        }
        if trim_user is not None:
            api_vars['trim_user'] = tbool(trim_user)
        if include_my_retweet is not None:
            api_vars['include_my_retweet'] = tbool(include_my_retweet)
        if include_entities is not None:
            api_vars['include_entities'] = tbool(include_entities)

        url = self.api_base_url + 'statuses/show.json'
        return self.send_request('GET', url, query_vars=api_vars, async=async)


    # Get up to 100 tweet objects by id (a comma separated list of ids)
    def lookup(self,
             id,  # comma separated list of up to 100 tweet ids
             include_entities=None,
             trim_user=None,
             map=None,
             async=None):

        api_vars = {
            'id': id,
        }
        if include_entities is not None:
            api_vars['include_entities'] = tbool(include_entities)
        if trim_user is not None:
            api_vars['trim_user'] = tbool(trim_user)
        if map is not None:
            api_vars['map'] = tbool(map)

        url = self.api_base_url + 'statuses/lookup.json'
        return self.send_request('GET', url, query_vars=api_vars, async=async)


    # Return up to the 100 most recent retweets of a tweet
    def retweets(self,
                 id,  # numeric tweet id
                 count=None,
                 trim_user=None,
                 async=None):

        api_vars = {}
        if count is not None:
            api_vars['count'] = count
        if trim_user is not None:
            api_vars['trim_user'] = tbool(trim_user)

        url = self.api_base_url + 'statuses/retweets/{:s}.json'.format(id)
        return self.send_request('GET', url, query_vars=api_vars, async=async)


    # Return up to 100 user IDs of retweeters
    def retweeters(self,
                   id,  # numeric tweet id
                   cursor=None,
                   stringify_ids=None,
                   async=None):

        api_vars = {
            'id': id,
        }
        if cursor is not None:
            api_vars['cursor'] = cursor
        if stringify_ids is not None:
            api_vars['stringify_ids'] = tbool(stringify_ids)

        url = self.api_base_url + 'statuses/retweeters/ids.json'
        return self.send_request('GET', url, query_vars=api_vars, async=async)


    # Search for tweets
    def search(self,
               q,  # search query string (up to 500 chars)
               geocode=None,
               lang=None,
               locale=None,
               result_type=None,
               count=None,
               until=None,
               since_id=None,
               max_id=None,
               include_entities=None,
               callback=None,
               async=None):

        api_vars = {
            'q': q,
        }
        if geocode is not None:
            api_vars['geocode'] = geocode
        if lang is not None:
            api_vars['lang'] = lang
        if locale is not None:
            api_vars['locale'] = locale
        if result_type is not None:
            api_vars['result_type'] = result_type
        if count is not None:
            api_vars['count'] = count
        if until is not None:
            api_vars['until'] = until
        if since_id is not None:
            api_vars['since_id'] = since_id
        if max_id is not None:
            api_vars['max_id'] = max_id
        if include_entities is not None:
            api_vars['include_entities'] = tbool(include_entities)
        if callback is not None:
            api_vars['callback'] = callback

        url = self.api_base_url + 'search/tweets.json'
        return self.send_request('GET', url, query_vars=api_vars, async=async)
