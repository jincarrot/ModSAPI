
from events.signals.SystemEventSignals import *

class ClientAfterEvents:
    """Client events of ModSAPI."""

    @property
    def serverSendToClient(self) -> ServerSendToClientAfterEventSignal:
        """Event triggered when server sends data to client."""
    