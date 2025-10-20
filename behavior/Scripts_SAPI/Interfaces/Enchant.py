# coding=utf-8
# from typing import Union, Dict
import mod.server.extraServerApi as serverApi
from ..Enumerations import *

SComp = serverApi.GetEngineCompFactory()


class Enchantment(object):
    """
    This interface represents a specific leveled enchantment that is applied to an item.
    """

    def __init__(self, typeId, level):
        # type: (str, int) -> None
        self.__type = typeId
        self.__typeId = typeId
        self.__level = level
        self._id = -1
        for i in EnchantTypes:
            if EnchantTypes[i] == self.__typeId:
                self._id = i
                break

    def __eq__(self, value):
        # type: (Enchantment | str) -> bool
        if type(value) == str:
            return self.__type == value
        return self.__type == value.type and self.__level == value.level

    def __str__(self):
        data = {
            "typeId": self.__typeId,
            "level": self.__level
        }
        return "<Enchant> %s" % data
    
    @property
    def type(self):
        # type: () -> str
        return self.__type
    
    @type.setter
    def type(self, value):
        # type: (str) -> None
        self.__type = value

    @property
    def typeId(self):
        # type: () -> str
        return self.__typeId
    
    @typeId.setter
    def typeId(self, value):
        # type: (str) -> None
        self.__typeId = value

    @property
    def level(self):
        # type: () -> int
        return self.__level
    
    @level.setter
    def level(self, value):
        # type: (int) -> None
        self.__level = value
