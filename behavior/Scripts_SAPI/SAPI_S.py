# -*- coding: utf-8 -*-

from Classes.Entity import *
from Classes.WorldEvents import *
from Classes.Scoreboard import *
from Interfaces.Game import *
from Classes.Container import *
from scheduler import Scheduler
from decorators import *
import types

ServerSystem = serverApi.GetServerSystemCls()
comp = serverApi.GetEngineCompFactory()

class World(ServerSystem):

    def __init__(self, namespace, systemName):
        ServerSystem.__init__(self, namespace, systemName)
        self.__afterEvents = WorldAfterEvents()
        self.__beforeEvents = WorldBeforeEvents()
        self.__gameRules = GameRules()
        self.__scoreboard = Scoreboard()
        print("ModSAPI: world loaded")
        global world
        world = self

    @property
    def afterEvents(self):
        """
        Contains a set of events that are applicable to the entirety of the world.
        Event callbacks are called in a deferred manner.
        Event callbacks are executed in read-write mode.
        """
        return self.__afterEvents

    @property
    def beforeEvents(self):
        """
        Contains a set of events that are applicable to the entirety of the world.
        Event callbacks are called immediately.
        Event callbacks are executed in read-only mode.
        """
        return self.__beforeEvents

    @property
    def gameRules(self):
        """
        The game rules that apply to the world.
        """
        return self.__gameRules

    @property
    def scoreboard(self):
        return self.__scoreboard

    @staticmethod
    def getAllPlayers():
        # type: () -> list[Player]
        """
        Returns an array of all active players within the world.
        """
        playerIds = serverApi.GetPlayerList()
        players = []
        for playerId in playerIds:
            players.append(Player(playerId))
        return players

    @staticmethod
    def getPlayers(options=EntityQueryOptions):
        # type: (dict | EntityQueryOptions) -> list[Player]
        """
        Returns a set of players based on a set of conditions defined via the EntityQueryOptions set of filter criteria.
        """
        options = EntityQueryOptions(options) if type(options) == dict else options
        players = []
        playerIds = serverApi.GetPlayerList()
        if options.selfCheck():
            playerIds = serverApi.GetPlayerList()
            playerIds = options.check(playerIds)
            for playerId in playerIds:
                players.append(Player(playerId))
        return players

    @staticmethod
    def getDimension(dimensionId):
        # type: (str) -> Dimension
        """
        Returns a dimension object.
        """
        return Dimension(dimensionId)

    @staticmethod
    def setDynamicProperty(identifier, value):
        # type: (str, 0) -> None
        """
        Sets a specified property to a value.
        """
        SComp.CreateExtraData(serverApi.GetLevelId()).SetExtraData(identifier, value)

    @staticmethod
    def getDynamicProperty(identifier):
        # type: (str) -> 0
        """
        Returns a property value.
        """
        return SComp.CreateExtraData(serverApi.GetLevelId()).GetExtraData(identifier)
    
    @staticmethod
    def getDynamicPropertyIds():
        # type: () -> list[str]
        """
        Gets a set of dynamic property identifiers that have been set in this world.
        """
        data = SComp.CreateExtraData(serverApi.GetLevelId()).GetWholeExtraData()
        return data.keys()
    
    @staticmethod
    def getDynamicPropertyTotalByteCount():
        # type: () -> int
        """
        Gets the total byte count of dynamic properties. 
        This could potentially be used for your own analytics to ensure you're not storing gigantic sets of dynamic properties.
        """
        DataComp = SComp.CreateExtraData(serverApi.GetLevelId())
        data = DataComp.GetWholeExtraData()
        count = 0
        for key in data.keys():
            count += len(key)
            value = data[key]
            if type(value).__name__ == 'str':
                count += len(value)
            else:
                count += 8
        return count
    
    @staticmethod
    def getEntity(id):
        # type: (str) -> Entity | None
        """
        Returns an entity based on the provided id.
        """
        if SComp.CreateGame(serverApi.GetLevelId()).IsEntityAlive(id):
            return createEntity(id)
        else:
            return None
        
    @staticmethod
    def getTimeOfDay():
        """
        Returns the time of day. (In ticks, between 0 and 24000)
        """
        return SComp.CreateTime(serverApi.GetLevelId()).GetTime() % 24000
    
    @staticmethod
    def getAbsoluteTime():
        """
        Returns the absolute time since the start of the world.
        """
        return SComp.CreateTime(serverApi.GetLevelId()).GetTime()
    
    @staticmethod
    def setTimeOfDay(timeOfDay):
        # type: (int) -> None
        """
        Sets the time of day.
        """
        SComp.CreateTime(serverApi.GetLevelId()).SetTimeOfDay(timeOfDay)

    @staticmethod
    def setAbsoluteTime(absoluteTime):
        # type: (int) -> None
        """Sets the world time."""
        SComp.CreateTime(serverApi.GetLevelId()).SetTime(absoluteTime)

    def __stopMusic(self):
        """Stops any music tracks from playing."""
        self.BroadcastToAllClient("setMusicState", {"state": False})

    def sendMessage(self, message):
        # type: (str) -> None
        """Sends a message to all players."""
        SComp.CreateMsg(serverApi.GetLevelId()).SendMsg("服务器", message)

    @staticmethod
    def getLootTableManager():
        """Returns a manager capable of generating loot from an assortment of sources."""
        return
    
    def listen(self, eventName, callback, namesapce=serverApi.GetEngineNamespace(), systemName=serverApi.GetEngineSystemName()):
        # type: (str, types.FunctionType, str, str) -> None
        """
        listen for an event
        """
        pass
    
class System(ServerSystem):
    """
    A class that provides system-level events and functions.
    """

    _scriptScheduler = Scheduler()

    def __init__(self, namespace, systemName):
        ServerSystem.__init__(self, namespace, systemName)
        self._initScheduler()
        print("ModSAPI: system loaded")

    def _OnScriptTickServer(self):
        self._scriptScheduler.executeSequenceAsync()

    def _initScheduler(self):
        self.ListenForEvent(
            serverApi.GetEngineNamespace(),
            serverApi.GetEngineSystemName(),
            "OnScriptTickServer",
            self,
            self._OnScriptTickServer
        )

    def run(self, callback):
        # type: (types.FunctionType) -> int
        """
        Runs a specified function at the next available future time. 
        This is frequently used to implement delayed behaviors and game loops. 
        When run within the context of an event handler, this will generally run the code at the end of the same tick where the event occurred. 
        When run in other code (a system.run callout), this will run the function in the next tick. 
        
        Note, however, that depending on load on the system, running in the same or next tick is not guaranteed."""
        return self._scriptScheduler.run(callback)

    def runTimeout(self, callback, tickDelay=1):
        # type: (types.FunctionType, int) -> int
        """
        Runs a set of code at a future time specified by tickDelay.
        """
        return self._scriptScheduler.runTimer(callback, tickDelay)

    def runInterval(self, callback, tickInterval=1):
        # type: (types.FunctionType, int) -> int
        """
        Runs a set of code on an interval.
        """
        return self._scriptScheduler.runTimer(callback, tickInterval, True)

    def clearRun(self, runId):
        # type: (int) -> None
        """
        Cancels the execution of a function run that was previously scheduled via @minecraft/server.System.run.
        """
        self._scriptScheduler.removeTask('SchedulerTask', runId)
