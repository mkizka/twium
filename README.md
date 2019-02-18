# twium
Seleniumを使ったpython-twitter風ラッパー

## Install
```bash
pip install git+https://github.com/Compeito/twium
```

## Usage
```python
import twium
api = twium.AltApi()

# login
api.auth('username', 'password')
api.write_cookies('path/to/cookie.json')

# or use cookie
api.load_cookies('path/to/cookie.json')


# methods
api.tweet('hogehoge')
api.del_tweet(123)
api.favorite(123)
api.retweet(123)
api.follow('hogehoge')
api.unfollow('hogehoge')


# get tweets
for tweet in api.search('some query'):
    print(tweet.text)

for tweet in api.timeline():
    print(tweet.text)
```
