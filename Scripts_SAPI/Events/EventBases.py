# coding=utf-8
import types
from mod.common.minecraftEnum import EntityComponentType
from ..Interfaces.Sources import *
from ..Interfaces.EntityOptions import *
from ..minecraft import *

ServerSystem = serverApi.GetServerSystemCls()
SComp = serverApi.GetEngineCompFactory()


class Wrapper(object):
    """
    wrapper
    """

    def __init__(self, T):
        self.__T = T

    def wrap(self, data):
        # type: (dict) -> 0
        return self.__T(data)


class EventListener(object):
    """
    process event
    """

    def __init__(self, eventName, callback, options=None, detectFunc=None, valueName=None, wrapper=None):
        # type: (str, types.FunctionType, 0, types.FunctionType, str, 0) -> None
        global world
        self.__callback = callback
        self.__options = options
        self.__check = detectFunc
        self.__wrapper = wrapper
        self.__valueName = valueName
        if not world:
            world = getWorld()
        world.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), eventName, self, self.listen)

    @property
    def options(self):
        """options"""
        return self.__options

    def listen(self, data):
        if (self.__check and self.__check(self, data, self.__valueName)) or not self.__check:
            value = self.__wrapper(data)
            self.__callback(value)


class Events(object):

    def __init__(self):
        self.__eventName = None

    def __check(self, obj, data, valueName):
        pass

    def subscribe(self, callback, options=None):
        # type: (types.FunctionType, dict) -> None
        pass

    def unsubscribe(self):
        pass


