# -*- coding: utf-8 -*-
# from typing import Union, Dict
from Entity import *
import mod.server.extraServerApi as serverApi
import mod.client.extraClientApi as clientApi
from ..decorators import *

SComp = serverApi.GetEngineCompFactory()
CComp = clientApi.GetEngineCompFactory()

CmdComp = SComp.CreateCommand(serverApi.GetLevelId())


class ScoreboardIdentity(object):
    """
    Contains an identity of the scoreboard item.
    """
    def __init__(self, scoreboard, entityId):
        # type: (ScoreboardObjective, str) -> None
        self.__id = scoreboard.id
        self.__name = scoreboard.displayName
        self.__entityId = entityId
        self.__type = "FakePlayer" if entityId == -1 else ("Player" if SComp.CreateEngineType(entityId).GetEngineTypeStr() == 'minecraft:player' else "Entity")
    
    @property
    def displayName(self):
        # type: () -> str
        return self.__name
    
    @property
    def id(self):
        # type: () -> str
        return self.__id
    
    @property
    def type(self):
        # type: () -> str
        return self.__type
    
    def getEntity(self):
        # type: () -> Entity
        return createEntity(self.__entityId)


class ScoreboardObjective(object):
    """
    Contains information about a scoreboard objective.
    """
    import Entity as en

    def __init__(self, id, name):
        # type: (str, str) -> None
        self.__id = id
        self.__name = name

    @property
    def id(self):
        # type: () -> str
        return self.__id
    
    @property
    def displayName(self):
        # type: () -> str
        return self.__name
    
    @property
    def isValid(self):
        scoreboards = SComp.CreateGame(serverApi.GetLevelId()).GetAllScoreboardObjects()
        for scoreboard in scoreboards:
            if scoreboard['name'] == self.__id:
                return True
        return False
    
    def addScore(self, participate, scoreToAdd):
        # type: (en.Entity | str, int) -> int
        """
        Adds a score to the given participant and objective.
        """
        CmdComp.SetCommand("scoreboard players add %s %s %s" % ("@s" if type(participate) != str else participate, self.__id, scoreToAdd), participate.id if type(participate) != str else None)
        return scoreToAdd
    
    def getParticipants(self):
        # type: () -> list[ScoreboardIdentity]
        datas = SComp.CreateGame(serverApi.GetLevelId()).GetAllPlayerScoreboardObjects()
        participants = []
        for playerData in datas:
            for scoreData in playerData['scoreList']:
                if {"name": self.__id} in scoreData:
                    participants.append({'playerId': playerData['playerId'], 'score': scoreData['value']})
                    break
        result = []
        for player in participants:
            result.append(ScoreboardIdentity(self, player['playerId']))
        return result


class Scoreboard(object):
    """
    Contains objectives and participants for the scoreboard.
    """

    @staticmethod
    def addObjective(objectiveId, displayName=""):
        # type: (str, str) -> ScoreboardObjective
        """
        Adds a new objective to the scoreboard.
        """
        CmdComp.SetCommand("scoreboard objectives add %s dummy %s" % (objectiveId, displayName))
        if displayName:
            return ScoreboardObjective(objectiveId, displayName)
        return ScoreboardObjective(objectiveId, objectiveId)
    
    @staticmethod
    def getObjective(objectiveId):
        # type: (str) -> ScoreboardObjective
        """
        Returns a specific objective (by id).
        """
        scores = SComp.CreateGame(serverApi.GetLevelId()).GetAllScoreboardObjects()
        displayName = ""
        for data in scores:
            if data['name'] == objectiveId:
                displayName = data['displayName']
        return ScoreboardObjective(objectiveId, displayName)
    
    def clearObjectiveAtDisplaySlot(self, displaySlotId):
        # type: (str) -> ScoreboardObjective
        """
        Clears the objective that occupies a display slot.

        Note: this method can return object only when try to clear sidebar
        """
        obj = self.getObjectiveAtDisplaySlot(displaySlotId)
        SComp.CreateCommand(serverApi.GetLevelId()).SetCommand("scoreboard objectives setdisplay %s" % displaySlotId.lower() if displaySlotId != "BelowName" else 'below_name')
        return obj
    
    @staticmethod
    def getObjectiveAtDisplaySlot(displaySlotId):
        # type: (str) -> ScoreboardObjective
        """
        Returns an objective that occupies the specified display slot.

        Note: this method can only get sidebar
        """
        if displaySlotId == 'Sidebar':
            scores = CComp.CreateGame(clientApi.GetLevelId()).GetAllScoreboardObjects()
            if len(scores):
                return ScoreboardObjective(scores[0]['name'], scores[0]['displayName'])
        return None
    
    @staticmethod
    def getObjectives():
        # type: () -> list[ScoreboardObjective]
        """
        Returns all defined objectives.
        """
        scores = SComp.CreateGame(serverApi.GetLevelId()).GetAllScoreboardObjects()
        result = []
        for data in scores:
            result.append(ScoreboardObjective(data['name'], data['displayName']))
        return result

