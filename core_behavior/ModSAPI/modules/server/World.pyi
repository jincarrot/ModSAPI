import mod.server.extraServerApi as serverApi
import typing
from Entity import *
from Player import *
from WorldEvents import *
from Dimension import *
from Scoreboard import *
from ...interfaces.Game import *
from Container import *
from .managers.TickingAreaManager import *
from .managers.StructureManager import *

ServerSystem = serverApi.GetServerSystemCls()
comp = serverApi.GetEngineCompFactory()

class World(ServerSystem):

    @property
    def afterEvents(self) -> WorldAfterEvents:
        """
        Contains a set of events that are applicable to the entirety of the world.
        Event callbacks are called in a deferred manner.
        Event callbacks are executed in read-write mode.
        """

    @property
    def beforeEvents(self) -> WorldBeforeEvents:
        """
        Contains a set of events that are applicable to the entirety of the world.
        Event callbacks are called immediately.
        Event callbacks are executed in read-only mode.
        """

    @property
    def gameRules(self) -> GameRules:
        """
        The game rules that apply to the world.
        """

    @property
    def scoreboard(self) -> Scoreboard:
        """"""

    @property
    def tickingAreaManager(self) -> TickingAreaManager:
        """Manager for adding, removing and querying pack specific ticking areas."""

    @property
    def structureManager(self) -> StructureManager:
        """Returns the manager for @minecraft/server.Structure related APIs."""

    @staticmethod
    def getAllPlayers() -> list[Player]:
        """
        Returns an array of all active players within the world.
        """

    @staticmethod
    def getPlayers(options: EntityQueryOptions={}) -> list[Player]:
        """
        Returns a set of players based on a set of conditions defined via the EntityQueryOptions set of filter criteria.
        """

    @staticmethod
    def getDimension(dimensionId: str) -> Dimension:
        """
        Returns a dimension object.
        """

    @staticmethod
    def setDynamicProperty(identifier: str, value: any):
        """
        Sets a specified property to a value.
        """

    @staticmethod
    def getDynamicProperty(identifier) -> any:
        """
        Returns a property value.
        """
    
    @staticmethod
    def getDynamicPropertyIds() -> list[str]:
        """
        Gets a set of dynamic property identifiers that have been set in this world.
        """
    
    @staticmethod
    def getDynamicPropertyTotalByteCount() -> int:
        """
        Gets the total byte count of dynamic properties. 
        This could potentially be used for your own analytics to ensure you're not storing gigantic sets of dynamic properties.
        """
    
    @staticmethod
    def getEntity(id) -> Entity | None:
        """
        Returns an entity based on the provided id.
        """
        
    @staticmethod
    def getTimeOfDay() -> int:
        """
        Returns the time of day. (In ticks, between 0 and 24000)
        """
    
    @staticmethod
    def getAbsoluteTime() -> int:
        """
        Returns the absolute time since the start of the world.
        """
    
    @staticmethod
    def setTimeOfDay(timeOfDay: int):
        """
        Sets the time of day.
        """

    @staticmethod
    def setAbsoluteTime(absoluteTime: int):
        """Sets the world time."""

    def __stopMusic(self):
        """Stops any music tracks from playing."""
        self.BroadcastToAllClient("setMusicState", {"state": False})

    def sendMessage(self, message: str):
        """Sends a message to all players."""

    @staticmethod
    def getLootTableManager():
        """Returns a manager capable of generating loot from an assortment of sources."""
    