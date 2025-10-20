# coding=utf-8
import types
from mod.common.minecraftEnum import EntityComponentType
from ..Interfaces.Sources import *
from ..Interfaces.EntityOptions import *
from ..minecraft import *

ServerSystem = serverApi.GetServerSystemCls()
SComp = serverApi.GetEngineCompFactory()

eventListenData = {}


class EventManager(object):

    def __init__(self, eventName):
        self.__name = eventName
        self.callbacks = []

    def listen(self, data):
        for callback in self.callbacks:
            callback(data)

    def add(self, callback):
        self.callbacks.append(callback)

    def remove(self, callback):
        self.callbacks.remove(callback)

    @property
    def empty(self):
        # type: () -> bool
        return True if not len(self.callbacks) else False


class LisenerManager(object):
    """manage listener"""

    def __init__(self):
        self.__data = {}

    def get(self, eventName):
        # type: (str) -> EventManager
        if eventName not in self.__data:
            event = EventManager(eventName)
            self.__data[eventName] = event
        return self.__data[eventName]


listenerManager = LisenerManager()


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
        event = listenerManager.get(eventName)
        if event.empty:
            world.ListenForEvent(namespace, systemName, eventName, event, event.listen)
        event.add(self.listen)

    @property
    def options(self):
        """options"""
        return self.__options

    def listen(self, data):
        if (self.__check and self.__check(self, data, self.__valueName)) or not self.__check:
            value = self.__wrapper(data)
            self.__callback(value)

    def unListen(self):
        listenerManager.get(self.__wrapper.__name__).remove(self.listen)


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


