# twium
Seleniumを使ったpython-twitter風ラッパー

## Usage
```python
import twium

api = twium.AltApi(
    username='screen_name',
    password='password',
    timeout=30,
    debug=True)

# tweet
api.tweet('some text')

# search
for tweet in api.search('some query'):
    print(tweet.text)
```
