import dateutil.parser


class Tweet:
    def __init__(self, tweet: dict):
        self.created_at = dateutil.parser.parse(tweet['created_at'])
        self.id = tweet['id']
        self.id_str = tweet['id_str']
        self.text = tweet['text']
        self.truncated = tweet['truncated']
        self.entities = tweet['entities']
        self.source = tweet['source']
        self.in_reply_to_status_id = tweet['in_reply_to_status_id']
        self.in_reply_to_status_id_str = tweet['in_reply_to_status_id_str']
        self.in_reply_to_user_id = tweet['in_reply_to_user_id']
        self.in_reply_to_user_id_str = tweet['in_reply_to_user_id_str']
        self.in_reply_to_screen_name = tweet['in_reply_to_screen_name']
        self.user_id = tweet['user_id']
        self.user_id_str = tweet['user_id_str']
        self.geo = tweet['geo']
        self.coordinates = tweet['coordinates']
        self.place = tweet['place']
        self.contributors = tweet['contributors']
        self.is_quote_status = tweet['is_quote_status']
        self.retweet_count = tweet['retweet_count']
        self.favorite_count = tweet['favorite_count']
        self.conversation_id = tweet['conversation_id']
        self.conversation_id_str = tweet['conversation_id_str']
        self.favorited = tweet['favorited']
        self.retweeted = tweet['retweeted']
        self.lang = tweet['lang']
        self.supplemental_language = tweet['supplemental_language']
