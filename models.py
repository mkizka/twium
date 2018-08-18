class Status:

    def __init__(self, text, status_id, user=None):
        self.text = text
        self.user = user
        self.id = status_id


class User:

    def __init__(self, name, screen_name, user_id):
        self.name = name
        self.screen_name = screen_name
        self.user_id = user_id
