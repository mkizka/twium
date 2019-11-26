import datetime
from typing import Dict

import dateutil.parser


class Tweet:
    def __init__(self, tweet: dict):
        self.created_at: datetime.datetime = dateutil.parser.parse(tweet['created_at'])
        self.id: int = tweet['id']
        self.id_str: str = tweet['id_str']
        self.full_text: str = tweet['full_text']
        self.truncated: bool = tweet['truncated']
        self.display_text_range: list = tweet['display_text_range']
        self.entities: Dict[str, list] = tweet['entities']
        self.source: str = tweet['source']
        self.in_reply_to_status_id: int = tweet['in_reply_to_status_id']
        self.in_reply_to_status_id_str: str = tweet['in_reply_to_status_id_str']
        self.in_reply_to_user_id: int = tweet['in_reply_to_user_id']
        self.in_reply_to_user_id_str: str = tweet['in_reply_to_user_id_str']
        self.in_reply_to_screen_name: str = tweet['in_reply_to_screen_name']
        self.user_id: int = tweet['user_id']
        self.user_id_str: str = tweet['user_id_str']
        self.geo: dict = tweet['geo']
        self.coordinates = tweet['coordinates']
        self.place = tweet['place']
        self.contributors = tweet['contributors']
        self.is_quote_status: bool = tweet['is_quote_status']
        self.retweet_count: int = tweet['retweet_count']
        self.favorite_count: int = tweet['favorite_count']
        self.reply_count: int = tweet['reply_count']
        self.conversation_id: int = tweet['conversation_id']
        self.conversation_id_str: str = tweet['conversation_id_str']
        self.favorited: bool = tweet['favorited']
        self.retweeted: bool = tweet['retweeted']
        self.lang: str = tweet['lang']
        self.supplemental_language = tweet['supplemental_language']
        self.self_thread: dict = tweet.get('self_thread', None)
