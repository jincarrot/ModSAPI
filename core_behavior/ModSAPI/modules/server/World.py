import mod.server.extraServerApi as serverApi

from Entity import *
from Player import *
from WorldEvents import *
from Dimension import *
from Scoreboard import *
from ...interfaces.Game import *
from Container import *
# from .architect.scheduler import Scheduler
from managers.TickingAreaManager import *
from managers.StructureManager import *
# from decorators import *
from ...utils.system import systems

ServerSystem = serverApi.GetServerSystemCls()
comp = serverApi.GetEngineCompFactory()
core = systems.core

class World(ServerSystem):

    def __init__(self, namespace, systemName):
        ServerSystem.__init__(self, namespace, systemName)
        self.__entities = {} # type: dict[str, Entity]
        self.__afterEvents = WorldAfterEvents()
        self.__beforeEvents = WorldBeforeEvents()
        self.__gameRules = GameRules()
        self.__scoreboard = Scoreboard()
        self.__tickingAreaManager = TickingAreaManager()
        self.__structureManager = StructureManager()

    @property
    def afterEvents(self):
        return self.__afterEvents

    @property
    def beforeEvents(self):
        return self.__beforeEvents

    @property
    def gameRules(self):
        return self.__gameRules

    @property
    def scoreboard(self):
        return self.__scoreboard

    @property
    def tickingAreaManager(self):
        return self.__tickingAreaManager

    @property
    def structureManager(self):
        return self.__structureManager

    @staticmethod
    def getAllPlayers():
        playerIds = serverApi.GetPlayerList()
        players = []
        for playerId in playerIds:
            if playerId in core.entities:
                player = core.entities[core.entities.index(playerId)]
                players.append(player)
            else:
                player = Player(playerId)
                core.entities.append(player)
                players.append(player)
        return players

    @staticmethod
    def getPlayers(options={}):
        options = EntityQueryOptions(options) if type(options) == dict else options
        players = []
        playerIds = serverApi.GetPlayerList()
        if options.selfCheck():
            playerIds = options.check(playerIds)
            for playerId in playerIds:
                players.append(systems.core.entities[systems.core.entities.index(playerId)])
        return players

    @staticmethod
    def getDimension(dimensionId):
        return Dimension(dimensionId)

    @staticmethod
    def setDynamicProperty(identifier, value):
        SComp.CreateExtraData(serverApi.GetLevelId()).SetExtraData(identifier, value)

    @staticmethod
    def getDynamicProperty(identifier):
        return SComp.CreateExtraData(serverApi.GetLevelId()).GetExtraData(identifier)
    
    @staticmethod
    def getDynamicPropertyIds():
        data = SComp.CreateExtraData(serverApi.GetLevelId()).GetWholeExtraData()
        return data.keys()
    
    @staticmethod
    def getDynamicPropertyTotalByteCount():
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
    
    def getEntity(self, id):
        if id in core.entities:
            return core.entities[core.entities.index(id)]
        
    @staticmethod
    def getTimeOfDay():
        return SComp.CreateTime(serverApi.GetLevelId()).GetTime() % 24000
    
    @staticmethod
    def getAbsoluteTime():
        return SComp.CreateTime(serverApi.GetLevelId()).GetTime()
    
    @staticmethod
    def setTimeOfDay(timeOfDay):
        SComp.CreateTime(serverApi.GetLevelId()).SetTimeOfDay(timeOfDay)

    @staticmethod
    def setAbsoluteTime(absoluteTime):
        SComp.CreateTime(serverApi.GetLevelId()).SetTime(absoluteTime)

    def __stopMusic(self):
        self.BroadcastToAllClient("setMusicState", {"state": False})

    def sendMessage(self, message):
        SComp.CreateMsg(serverApi.GetLevelId()).SendMsg("服务器", message)

    @staticmethod
    def getLootTableManager():
        return
    