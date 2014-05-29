__author__ = 'JordSti'


class SqException(Exception):
    pass


class GameClientException(SqException):
    pass

class GameServerException(SqException):
    pass

class GameException(SqException):
    pass