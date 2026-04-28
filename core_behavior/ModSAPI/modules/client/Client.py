import mod.client.extraClientApi as clientApi
from ClientEvents import *
from Player import *
from Screen import Screen

ClientSystem = clientApi.GetClientSystemCls()
CComp = clientApi.GetEngineCompFactory()

class Client(ClientSystem):
    """Client system of ModSAPI"""

    def __init__(self, namespace, systemName):
        ClientSystem.__init__(self, namespace, systemName)
        self.__localPlayer = ClientPlayer()
        self.__afterEvents = ClientAfterEvents(self)
        self.__screenManager = Screen()

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

    @property
    def screenManager(self):
        """Contains informations of player's screen."""
        return self.__screenManager
    
    @property
    def audioManager(self):
        pass

    def sendToServer(self, eventName, data):
        """Sends data to server. Server can listen to this data by subscribing to the event with the same name."""
        self.NotifyToServer("clientSendToServer", {"eventName": eventName, "data": data})

