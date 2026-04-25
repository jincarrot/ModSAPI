# -*- coding: utf-8 -*-
# from typing import Union, Dict
from Entity import *
import mod.server.extraServerApi as serverApi
from ...utils.system import systems
import ast

SComp = serverApi.GetEngineCompFactory()

CmdComp = SComp.CreateCommand(serverApi.GetLevelId())

class ScoreboardScoreInfo:
    """Contains a pair of a scoreboard participant and its respective score."""
    def __init__(self, participant, score):
        # type: (ScoreboardIdentity, int) -> None
        self.__participant = participant
        self.__score = score
    
    @property
    def participant(self):
        # type: () -> ScoreboardIdentity
        return self.__participant
    
    @property
    def score(self):
        # type: () -> int
        return self.__score

class ScoreboardIdentity(object):
    """
    Contains an identity of the scoreboard item.
    """
    def __init__(self, scoreboard, entityId, name=None):
        # type: (ScoreboardObjective, str, str) -> None
        self.__id = scoreboard.id
        self.__entityId = entityId
        self.__name = name
        entity = systems.world.getEntity(entityId)
        if entity and entity.isValid:
            self.__name = entity.nameTag
        if not self.__name:
            self.__name = entityId
        self.__type = "FakePlayer" if entityId == "-1" else ("Player" if SComp.CreateEngineType(entityId).GetEngineTypeStr() == 'minecraft:player' else "Entity")
    
    def __str__(self):
        data = {
            "id": self.__id,
            "name": self.__name,
            "type": self.__type
        }
        return "<ScoreboardIdentity> %s" % data
    
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
        # type: () -> Entity | None
        return createEntity(self.__entityId)


class ScoreboardObjective(object):
    """
    Contains information about a scoreboard objective.
    """

    def __init__(self, Id, name):
        # type: (str, str) -> None
        self.__id = Id
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
        # type: (Entity | str, int) -> int
        """
        Adds a score to the given participant and objective.
        """
        CmdComp.SetCommand("scoreboard players add %s %s %s" % ("@s" if type(participate) != str else participate, self.__id, scoreToAdd), participate.id if type(participate) != str else None)
        return scoreToAdd
    
    def getScore(self, participate):
        # type: (Entity | str | ScoreboardIdentity) -> int | None
        """Returns a specific score for a participant."""
        playerScores = comp.CreateGame(serverApi.GetLevelId()).GetAllPlayerScoreboardObjects()
        if isinstance(participate, ScoreboardIdentity):
            if participate.type == 'FakePlayer':
                participate = participate.displayName
            else:
                participate = participate.getEntity()

        if isinstance(participate, str):
            scores = systems.world.getDynamicProperty("scoreboard.%s" % self.__id)
            if not scores:
                return 0
            return scores.get(participate, 0)
        else:
            for playerScore in playerScores:
                if playerScore['playerId'] == participate.id:
                    for score in playerScore['scoreList']:
                        if score['name'] == self.__id:
                            return score['value']
                    return 0
            scores = systems.world.getDynamicProperty("scoreboard.%s" % self.__id)
            if not scores:
                return 0
            return scores.get(participate.id, 0)
    
    def getScores(self):
        # type: () -> list[ScoreboardScoreInfo]
        """Returns specific scores for this objective for all participants."""
        playerScores = comp.CreateGame(serverApi.GetLevelId()).GetAllPlayerScoreboardObjects()
        scores = systems.world.getDynamicProperty("scoreboard.%s" % self.__id)
        result = []
        for playerScore in playerScores:
            for score in playerScore['scoreList']:
                if score['name'] == self.__id:
                    result.append(ScoreboardScoreInfo(ScoreboardIdentity(self, playerScore['playerId']), score['value']))
                    break
        if scores:
            for key in scores:
                try:
                    float(key)
                    entity = systems.world.getEntity(key)
                    if entity and entity.isValid:
                        entityId = entity.id
                        result.append(ScoreboardScoreInfo(ScoreboardIdentity(self, entityId), scores[key]))
                except ValueError:
                    result.append(ScoreboardScoreInfo(ScoreboardIdentity(self, "-1", key), scores[key]))
        return result

    def getParticipants(self):
        # type: () -> list[ScoreboardIdentity]
        datas = SComp.CreateGame(serverApi.GetLevelId()).GetAllPlayerScoreboardObjects()
        participants = []
        for playerData in datas:
            for scoreData in playerData['scoreList']:
                if scoreData['name'] == self.__id:
                    participants.append({'playerId': playerData['playerId'], 'score': scoreData['value']})
                    break
        result = [] # type: list[ScoreboardIdentity]
        for player in participants:
            result.append(ScoreboardIdentity(self, player['playerId']))

        scores = systems.world.getDynamicProperty("scoreboard.%s" % self.__id)
        if scores:
            for key in scores:
                try:
                    float(key)
                    entity = systems.world.getEntity(key)
                    if entity and entity.isValid:
                        entityId = entity.id
                        if not entity.typeId == 'minecraft:player':
                            result.append(ScoreboardIdentity(self, entityId))
                except ValueError:
                    result.append(ScoreboardIdentity(self, "-1", key))
                    
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
        # type: (str) -> ScoreboardObjective | None
        """
        Returns a specific objective (by id).
        """
        scores = SComp.CreateGame(serverApi.GetLevelId()).GetAllScoreboardObjects()
        displayName = ""
        for data in scores:
            if data['name'] == objectiveId:
                displayName = data['displayName']
                break
        if displayName is None:
            return None
        if not displayName:
            displayName = objectiveId
        return ScoreboardObjective(objectiveId, displayName)
    
    def clearObjectiveAtDisplaySlot(self, displaySlotId):
        # type: (str) -> None
        """
        Clears the objective that occupies a display slot.

        Note: this method can return object only when try to clear sidebar
        """
        SComp.CreateCommand(serverApi.GetLevelId()).SetCommand("scoreboard objectives setdisplay %s" % displaySlotId.lower() if displaySlotId != "BelowName" else 'below_name')
    
    @staticmethod
    def getObjectives():
        # type: () -> list[ScoreboardObjective]
        """
        Returns all defined objectives.
        """
        scores = SComp.CreateGame(serverApi.GetLevelId()).GetAllScoreboardObjects()
        result = []
        for data in scores:
            result.append(ScoreboardObjective(data['name'], data['displayName'] if data['displayName'] else data['name']))
        return result

