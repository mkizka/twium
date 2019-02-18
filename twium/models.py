class TwitterModel:
    pass


class Status(TwitterModel):

    def __init__(self, text, status_id, user=None):
        self.text = text
        self.user = user
        self.id = status_id


class User(TwitterModel):

    def __init__(self, name, screen_name, user_id):
        self.name = name
        self.screen_name = screen_name
        self.user_id = user_id


class Notify(TwitterModel):

    def __init__(self, activity_type, users=None, tweet=None):
        self.activity_type = activity_type
        self.tweet = tweet
        self.users = users
