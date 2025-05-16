# -*- coding: utf-8 -*-

from Classes.Entity import *
from Classes.WorldEvents import *
from Interfaces.Game import *

ServerSystem = serverApi.GetServerSystemCls()
comp = serverApi.GetEngineCompFactory()

baseTypes = ("int", "float", "str", "list", "tuple", "dict", "bool", "NoneType")


class World(ServerSystem):

    def __init__(self, namespace, systemName):
        ServerSystem.__init__(self, namespace, systemName)
        self.__systemName = systemName
        self.__namespace = namespace
        self.__afterEvents = WorldAfterEvents()
        self.__beforeEvents = WorldBeforeEvents()
        self.__gameRules = GameRules()
        self.__scoreboard = Scoreboard()
        print("SAPI-world loaded")

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
        # type: () -> List[Player]
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
        # type: (dict) -> List[Player]
        """
        Returns a set of players based on a set of conditions defined via the EntityQueryOptions set of filter criteria.
        """
        options = EntityQueryOptions(options)
        players = []
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
        return Dimension(MinecraftDimensionTypes.index(dimensionId))


class System(ServerSystem):
    """
    A class that provides system-level events and functions.
    """

    def __init__(self, namespace, systemName):
        ServerSystem.__init__(self, namespace, systemName)

    def __getObj(self, data):
        info = {}
        attrs = dir(data)
        for attr in attrs:
            if attr.find("__") == 0:
                continue
            info[attr] = getattr(data, attr)
            if info[attr] and not (type(info[attr]).__name__ in baseTypes):
                info[attr] = self.__getObj(info[attr])
        return "Object %s" % type(data).__name__, info
