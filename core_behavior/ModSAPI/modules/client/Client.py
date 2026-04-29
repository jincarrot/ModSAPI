import mod.client.extraClientApi as clientApi
from ClientEvents import *
from Player import *
from Screen import Screen
from Entity import ClientEntity
from Audio import Audio
from Particle import Particle
from ...interfaces.Vector import Vector3

ClientSystem = clientApi.GetClientSystemCls()
CComp = clientApi.GetEngineCompFactory()

class Client(ClientSystem):
    """Client system of ModSAPI"""

    def __init__(self, namespace, systemName):
        ClientSystem.__init__(self, namespace, systemName)
        self.__localPlayer = ClientPlayer()
        self.__afterEvents = ClientAfterEvents(self)
        self.__screen = Screen()
        self.__audio = Audio()

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
    def screen(self):
        """Contains informations of player's screen."""
        return self.__screen
    
    @property
    def audio(self):
        """Contains operations related to audio."""
        return self.__audio

    def sendToServer(self, eventName, data):
        """Sends data to server. Server can listen to this data by subscribing to the event with the same name."""
        self.NotifyToServer("clientSendToServer", {"eventName": eventName, "data": data})

    def getEntity(self, entityId):
        """Gets an entity by its runtime identifier."""
        entity = ClientEntity(entityId)
        if not entity.isValid:
            return entity
        
    def spawnEntity(self, typeId, location):
        """
        Spawns a client-side entity of the given type at the given location. 
        Returns the runtime identifier of the spawned entity.
        """
        return self.getEntity(self.CreateClientEntityByTypeStr(typeId, location.getTuple()))
    
    def spawnParticle(self, typeId, location, options={}):
        """Spawns a particle effect."""
        location = Vector3(location)
        parId = CComp.CreateParticleSystem(clientApi.GetLevelId()).Create(typeId, location.getTuple())
        return Particle(parId)

