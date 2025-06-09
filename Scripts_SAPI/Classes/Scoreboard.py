# -*- coding: utf-8 -*-
# from typing import Union, Dict
import mod.server.extraServerApi as serverApi
import mod.client.extraClientApi as clientApi

SComp = serverApi.GetEngineCompFactory()
CComp = clientApi.GetEngineCompFactory()

CmdComp = SComp.CreateCommand(serverApi.GetLevelId())


class ScoreboardIdentity(object):
    """
    Contains an identity of the scoreboard item.
    """
    def __init__(self, scoreboard):
        # type: (ScoreboardObjective) -> None
        self.__id = scoreboard.id
        self.__name = scoreboard.displayName


class ScoreboardObjective(object):
    """
    Contains information about a scoreboard objective.
    """
    import Entity as en

    def __init__(self, id, name):
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
    

