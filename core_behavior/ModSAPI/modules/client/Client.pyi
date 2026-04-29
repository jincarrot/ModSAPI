import mod.client.extraClientApi as clientApi
from ClientEvents import *
from Player import *
from Screen import Screen
from Entity import ClientEntity
from Audio import Audio
from Particle import Particle
from ...interfaces.Vector import Vector3


ClientSystem = clientApi.GetClientSystemCls()

class Client(ClientSystem):
    """Client system of ModSAPI"""

    @property
    def localPlayer(self) -> ClientPlayer: ...

    @property
    def screen(self) -> Screen: ...

    @property
    def audio(self) -> Audio: ...

    @property
    def particle(self) -> Particle: ...

    @property
    def afterEvents(self) -> ClientAfterEvents:
        """Contains a set of events that are applicable to the entirety of this client side.
        Event callbacks are called in a deferred manner.
        Event callbacks are executed in read-write mode."""

    def sendToServer(self, eventName: str, data): 
        """Sends data to server. Server can listen to this data by subscribing to the event with the same name."""

    def getEntity(self, entityId: str) -> ClientEntity | None:
        """Gets an entity by its runtime identifier."""

    def spawnEntity(self, typeId: str, location: Vector3) -> ClientEntity:
        """
        Spawns a client-side entity of the given type at the given location. 
        Returns the runtime identifier of the spawned entity.
        """

    def getEntity(self, entityId: str) -> ClientEntity | None:
        """Gets an entity by its runtime identifier."""

    def spawnEntity(self, typeId: str, location: Vector3) -> ClientEntity:
        """
        Spawns a client-side entity of the given type at the given location. 
        Returns the runtime identifier of the spawned entity.
        """
    
    def spawnParticle(self, typeId: str, location: Vector3, options={}) -> Particle:
        """Spawns a particle effect."""
        