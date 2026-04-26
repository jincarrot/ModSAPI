import mod.client.extraClientApi as clientApi
from ClientEvents import *
from Player import *

ClientSystem = clientApi.GetClientSystemCls()
CComp = clientApi.GetEngineCompFactory()

class Client(ClientSystem):
    """Client system of ModSAPI"""

    def __init__(self, namespace, systemName):
        ClientSystem.__init__(self, namespace, systemName)
        self.__localPlayer = Player()
        self.__afterEvents = ClientAfterEvents(self)

    @property
    def localPlayer(self):
        """The local player."""
        return self.__localPlayer

    @property
    def afterEvents(self):
        """Contains a set of events that are applicable to the entirety of this client side.
        Event callbacks are called in a deferred manner.
        Event callbacks are executed in read-write mode."""
        return self.__afterEvents

