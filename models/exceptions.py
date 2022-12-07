class ServerConnectError(Exception):
    """
    Can not connect to server
    """

    def __init__(self, msg: str):
        self.msg = msg

    def __str__(self):
        return self.msg
