
from events.signals.SystemEventSignals import *

class ClientAfterEvents:
    """Client events of ModSAPI."""

    def __init__(self, clientSystem):
        self.__onServerSendToClient = ServerSendToClientAfterEventSignal()

    @property
    def serverSendToClient(self):
        """Event triggered when server sends data to client."""
        return self.__onServerSendToClient