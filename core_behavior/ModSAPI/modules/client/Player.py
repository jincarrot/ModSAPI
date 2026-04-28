
import mod.client.extraClientApi as clientApi
CComp = clientApi.GetEngineCompFactory()

class ClientPlayer:

    def __init__(self):
        self.__id = clientApi.GetLocalPlayerId()
        self.__name = CComp.CreateName(self.__id).GetName()

    def __str__(self):
        data = {
            "id": self.__id,
            "name": self.__name
        }
        return "<ClientPlayer> %s" % data

    @property
    def id(self):
        """Runtime identifier of this player."""
        return self.__id
    
    @property
    def name(self):
        """Name of this player."""
        return self.__name
    