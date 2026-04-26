# coding=utf-8

class ServerSendToClientAfterEvent(object):
    """
    Returns additional data about a /scriptevent command invocation.
    """

    def __init__(self, data): ...

    @property
    def id(self):
        # type: () -> str
        """Identifier of this ScriptEvent command message."""
    
    @property
    def data(self) -> any:
        """Data that send from server."""
    