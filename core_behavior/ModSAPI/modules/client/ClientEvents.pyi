
from events.signals.SystemEventSignals import *

class ClientAfterEvents:
    """Client events of ModSAPI."""

    @property
    def serverEventReceive(self) -> ServerEventReceiveAfterEventSignal:
        """Event triggered when server sends data to client."""
    