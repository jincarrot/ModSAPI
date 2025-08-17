# -*- coding: utf-8 -*-

from Classes.Entity import *
from Classes.WorldEvents import *
from Classes.Scoreboard import *
from Interfaces.Game import *
from Classes.Container import *
from scheduler import Scheduler

ServerSystem = serverApi.GetServerSystemCls()
comp = serverApi.GetEngineCompFactory()

class World(ServerSystem):

    def __init__(self, namespace, systemName):
        ServerSystem.__init__(self, namespace, systemName)
        self.__afterEvents = WorldAfterEvents()
        self.__beforeEvents = WorldBeforeEvents()
        self.__gameRules = GameRules()
        self.__scoreboard = Scoreboard()
        print("Scripts-API: world loaded")
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
            return Entity(id)
        else:
            return None
        
    @staticmethod
    def getTimeOfDay():
        """
        Returns the time of day. (In ticks, between 0 and 24000)
        """
        return SComp.CreateTime(serverApi.GetLevelId()).GetTime() % 24000

    def listen(self, eventName, callback):
        # type: (str, types.FunctionType) -> None
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

    def run(self, fn):
        return self._scriptScheduler.run(fn)

    def runTimeout(self, fn, ticks=1):
        return self._scriptScheduler.runTimer(fn, ticks)

    def runInterval(self, fn, ticks=1):
        return self._scriptScheduler.runTimer(fn, ticks, True)

    def clearTimeout(self, id):
        self._scriptScheduler.removeTask('SchedulerTask', id)

    def clearInterval(self, id):
        self._scriptScheduler.removeTask('SchedulerTask', id)

    def clearRun(self, id):
        self._scriptScheduler.removeTask('SchedulerTask', id)