import json
import math
import time

import requests

from models import Tweet

MAX_SEARCH_COUNT = 100


class SearchManager:
    def __init__(self, session: requests.Session):
        self.session = session

    def search(self, word, count=MAX_SEARCH_COUNT):
        result = []
        cursor = ''
        for i in range(math.ceil(count / MAX_SEARCH_COUNT)):
            response = self.session.get(
                f"https://api.twitter.com/2/search/adaptive.json"
                f"?include_want_retweets=1"
                f"&include_ext_alt_text=true"
                f"&count={count if count < MAX_SEARCH_COUNT else MAX_SEARCH_COUNT}"
                f"&query_source=typed_query"
                f"&tweet_search_mode=live"
                f"&q={word}"
                f"&cursor={cursor}"
            )
            response.raise_for_status()
            response_json = json.loads(response.text)

            last_timeline_content = response_json['timeline']['instructions'][0]['addEntries']['entries'][-1]['content']
            if 'operation' in last_timeline_content.keys():
                cursor = last_timeline_content['operation']['cursor']['value']

            count -= MAX_SEARCH_COUNT
            result += list(map(lambda j: Tweet(j), response_json['globalObjects']['tweets'].values()))

            time.sleep(1)
        return sorted(result, key=lambda tweet: tweet.created_at, reverse=True)
