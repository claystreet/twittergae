#twittergae

**Provided by [Clay Street Online](http://www.claystreet.com) under an MIT License**

Developed for [Sooshi.com](https://www.sooshi.com)

On Twitter [@sooshicom](https://twitter.com/sooshicom)

### Overview

twittergae is a dirt simple interface to twitter for python apps running on GAE (Google App Engine).

### Send a tweet

```python
from twittergae.tweets import Tweets
#...

# Initialize with your twitter credentials
tweets = Tweets(TWITTER_API_KEY,
				TWITTER_API_SECRET_KEY,
				TWITTER_ACCESS_TOKEN,
				TWITTER_ACCESS_SECRET_TOKEN)
				
tweets.update('Hello Twitterverse from twittergae')
```

Note: subsequent examples won't show the required credential initialization

### Send a tweet with location info

```python
#...
tweets.update('Hello Twitterverse from twittergae',
              lat='28.669997',
			  long='-81.208120')
```

### Get tweet ID from the JSON response

```python
#...
response = tweets.update('Hello Twitterverse from twittergae')
if response.twitter:
    tweet_id = response.twitter['id_str']
```

Note:
The "response" is simply an urlfetch() response object with an additional
dict named "twitter" that contains the JSON response data

```python
#...
response = tweets.update('Hello Twitterverse from twittergae')
if response.status_code == 200:  # check the urlfetch() response object's status code
    pass  # Do whatever...
```

### Async tweet using async urlfetch()

```python
from twittergae.twitterapi import twitter_response
from twittergae.tweets import Tweets
#...
rpc = tweets.update('Hello Twitterverse from twittergae', async='rpc')
#...
# do other stuff
#...
response = twitter_response(rpc.get_result())
if response.twitter:
    tweet_id = response.twitter['id_str']
```

### Async tweet using tasklet friendly ndb context

```python
from twittergae.twitterapi import twitter_response
from twittergae.tweets import Tweets
#...
future = tweets.update('Hello Twitterverse from twittergae', async='ndb')
#...
# do other stuff
#...
response = twitter_response(future.get_result())
if response.twitter:
    tweet_id = response.twitter['id_str']
```

### Fetch a photo and tweet with media & coordinates... asychronously

```python
from twittergae.gae_send_request import send_request_ndb
from twittergae.twitterapi import twitter_response
from twittergae.tweets import Tweets
#...
photo_url = 'https://www.google.com/images/srpr/logo11w.png'
photo_future = send_request_ndb('GET', photo_url)
#...
# do other stuff
#...
photo_response = photo_future.get_result()
if photo_response.status_code == 200:
    tweet_future = tweets.update_with_media(
	    'Upload With Media from twittergae',
        media={
            'filename': 'logo11w.png',
            'mimetype': 'image/png',
            'encoding': 'binary',
            'data': photo_response.content,
        },
        lat='28.669997',
        long='-81.208120',
		async='ndb')
    #...
    # do other stuff
    #...
	tweet_response = twitter_response(tweet_future.get_result())
	if tweet_response.twitter:
	    tweet_id = tweet_response.twitter['id_str']
		# do whatever with the tweet response...
```

### A simple async search example...

```python
#...
search_future = tweets.search('sooshi', async='ndb')
#...
# do other stuff
#...
search_response = twitter_response(search_future.get_result())
```

### What's not supported

1. There's no support for obtaining credentials from a user
1. Only the core "tweet" related API methods are supported in the Tweets class

### What you can do

The Tweets class demonstrates how simple it would be to expand API
support to include TwitterTimeline() and other APIs.


Visit [Sooshi.com](https://www.sooshi.com) and post an Ad
the next time you have something to sell locally!

I hope you find this code useful!
