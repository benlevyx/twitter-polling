class TweetError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(message)

    def __str__(self):
        return 'TweetError: ' + self.message


class InsufficientTweetsError(TweetError):
    def __init__(self, message):
        super().__init__(message)

    def __str__(self):
        return 'InsufficientTweetsError: ' + self.message
