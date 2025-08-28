# coding=utf-8
# from typing import Union, Dict
import mod.server.extraServerApi as serverApi
import mod.client.extraClientApi as clientApi

SComp = serverApi.GetEngineCompFactory()


class EffectType(object):
    """
    Represents a type of effect - like poison - that can be applied to an entity.
    """

    def __init__(self, name):
        self.__name = name

    def getName(self):
        # type: () -> str
        """
        Identifier name of this effect type.
        """
        return self.__name


class Effect(object):
    """
    Represents an effect - like poison - that has been added to an Entity.
    """

    def __init__(self, typeId, duration, amplifier=0):
        # type: (str, int, int) -> None
        self.__amplifier = amplifier
        self.__typeId = typeId
        self.__duration = duration
        self.__displayName = typeId

    def __str__(self):
        data = {
            "typeId": self.__typeId
        }
        return "<Effect> %s" % data

    @property
    def amplifier(self):
        # type: () -> int
        """
        Gets an amplifier that may have been applied to this effect.
        Sample values range typically from 0 to 4.
        Example: The effect 'Jump Boost II' will have an amplifier value of 1.
        """
        return self.__amplifier

    @property
    def displayName(self):
        # type: () -> str
        """
        Gets the player-friendly name of this effect.
        """
        return self.__displayName

    @property
    def duration(self):
        # type: () -> int
        """
        Gets the entire specified duration, in ticks, of this effect. There are 20 ticks per second.
        """
        return self.__duration

    @property
    def typeId(self):
        # type: () -> str
        """
        Gets the type id of this effect.
        """
        return self.__typeId
