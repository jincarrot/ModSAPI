# coding=utf-8
import types
from mod.common.minecraftEnum import EntityComponentType
from ..Interfaces.Sources import *
from ..Interfaces.EntityOptions import *
from ..minecraft import *

ServerSystem = serverApi.GetServerSystemCls()
SComp = serverApi.GetEngineCompFactory()


class EventListener(object):
    """
    process event
    """

    def __init__(self, eventName, callback, options=None, detectFunc=None, valueName=None, wrapper=None, namespace=serverApi.GetEngineNamespace(), systemName=serverApi.GetEngineSystemName()):
        # type: (str, types.FunctionType, 0, types.FunctionType, str, 0, str, str) -> None
        global world
        self.__eventName = eventName
        self.__callback = callback
        self.__options = options
        self.__check = detectFunc
        self.__wrapper = wrapper
        self.__valueName = valueName
        if not world:
            world = getWorld()
        SComp.CreateItem(serverApi.GetLevelId()).GetUserDataInEvent(eventName)
        world.ListenForEvent(namespace, systemName, eventName, self, self.listen)

    @property
    def options(self):
        """options"""
        return self.__options

    def listen(self, data):
        if (self.__check and self.__check(self, data, self.__valueName)) or not self.__check:
            value = self.__wrapper(data)
            self.__callback(value)

    def unListen(self):
        world.UnListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), self.__eventName, self, self.listen)


class Events(object):

    def __init__(self):
        self.__eventName = None
        self._events = {}

    def _check(self, obj, data, valueName):
        pass

    def subscribe(self, callback, options=None):
        # type: (types.FunctionType, dict) -> None
        pass

    def unsubscribe(self, callback):
        event = self._events.get(id(callback), None) # type: EventListener
        if event:
            event.unListen()
        else:
            print("未监听此函数%s" % callback)


