# coding=utf-8

class ServerEventReceiveAfterEvent:
    """
    Returns additional data about a /scriptevent command invocation.
    """

    def __init__(self, data):
        self.__id = data['eventName']
        self.__data = data['data']

    def __str__(self):
        data = {
            "id": self.__id
        }
        return "<ServerSendToClientAfterEvent> %s" % data
    
    @property
    def id(self):
        # type: () -> str
        """Identifier of this ScriptEvent command message."""
        return self.__id
    
    @property
    def data(self):
        return self.__data
    