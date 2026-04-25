# -*- coding: utf-8 -*-
# from typing import List, Dict, Union
from ..Classes.Entity import *

class ExplosionOptions(object):
    """Additional configuration options for the @minecraft/server.Dimension.createExplosion method."""

    def __init__(self, data):
        # type: (dict) -> None
        self.__allowUnderwater = data.get("allowUnderwater", True)
        self.__breaksBlocks = data.get("breaksBlocks", SComp.CreateGame(serverApi.GetLevelId()).GetGameRulesInfoServer()['cheat_info']['mob_griefing'])
        self.__causesFire = data.get("causesFire", False)
        self.__source = data.get("source", Player(serverApi.GetPlayerList()[0]))

    @property
    def source(self):
        # type: () -> Entity
        """Optional source of the explosion."""
        return self.__source
    
    @source.setter
    def source(self, value):
        # type: (Entity) -> None
        self.__source = value

    @property
    def allowUnderwater(self):
        # type: () -> bool
        """Whether parts of the explosion also impact underwater."""
        return self.__allowUnderwater
    
    @allowUnderwater.setter
    def allowUnderwater(self, value):
        # type: (bool) -> None
        self.__allowUnderwater = value

    @property
    def breaksBlocks(self):
        # type: () -> bool
        """Whether the explosion will break blocks within the blast radius."""
        return self.__breaksBlocks

    @breaksBlocks.setter
    def breaksBlocks(self, value):
        # type: (bool) -> None
        self.__breaksBlocks = value

    @property
    def causesFire(self):
        # type: () -> bool
        """If true, the explosion is accompanied by fires within or near the blast radius."""
        return self.__causesFire
    
    @causesFire.setter
    def causesFire(self, value):
        # type: (bool) -> None
        self.__causesFire = value
