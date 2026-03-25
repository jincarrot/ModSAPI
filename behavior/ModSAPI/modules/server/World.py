import mod.server.extraServerApi as serverApi

from Entity import *
from Player import *
from WorldEvents import *
from Dimension import *
from Scoreboard import *
from ...interfaces.Game import *
from Container import *
# from .architect.scheduler import Scheduler
from TickingAreaManager import *
# from decorators import *

ServerSystem = serverApi.GetServerSystemCls()
comp = serverApi.GetEngineCompFactory()

class World(ServerSystem):

    def __init__(self, namespace, systemName):
        ServerSystem.__init__(self, namespace, systemName)
        self.__afterEvents = WorldAfterEvents()
        self.__beforeEvents = WorldBeforeEvents()
        self.__gameRules = GameRules()
        self.__scoreboard = Scoreboard()
        self.__tickingAreaManager = TickingAreaManager()
        # print("ModSAPI: world loaded")

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

    @staticmethod
    def getAllPlayers():
        playerIds = serverApi.GetPlayerList()
        players = []
        for playerId in playerIds:
            players.append(Player(playerId))
        return players

    @staticmethod
    def getPlayers(options={}):
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
    
    @staticmethod
    def getEntity(id):
        if SComp.CreateGame(serverApi.GetLevelId()).IsEntityAlive(id):
            return createEntity(id)
        else:
            return None
        
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
    
    def listen(self, eventName, callback, namesapce=serverApi.GetEngineNamespace(), systemName=serverApi.GetEngineSystemName()):
        pass
    