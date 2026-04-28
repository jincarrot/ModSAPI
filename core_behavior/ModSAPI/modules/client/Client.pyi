import mod.client.extraClientApi as clientApi
from ClientEvents import *
from Player import *
from Screen import Screen

ClientSystem = clientApi.GetClientSystemCls()

class Client(ClientSystem):
    """Client system of ModSAPI"""

    @property
    def localPlayer(self) -> ClientPlayer: ...

    @property
    def screen(self) -> Screen: ...

    @property
    def afterEvents(self) -> ClientAfterEvents:
        """Contains a set of events that are applicable to the entirety of this client side.
        Event callbacks are called in a deferred manner.
        Event callbacks are executed in read-write mode."""

    def sendToServer(self, eventName: str, data): ...
        