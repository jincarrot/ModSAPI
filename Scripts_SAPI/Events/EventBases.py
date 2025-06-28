# coding=utf-8
import types

from mod.common.minecraftEnum import EntityComponentType
from ..Interfaces.Sources import *

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
        # type: (str, types.FunctionType, 0, types.FunctionType, str, Wrapper) -> None
        self.__callback = callback
        self.__options = options
        self.__check = detectFunc
        self.__wrapper = wrapper
        self.__valueName = valueName
        world.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), eventName, self, self.listen)

    @property
    def options(self):
        """options"""
        return self.__options

    def listen(self, data):
        if self.__check(self, data, self.__valueName):
            value = self.__wrapper.wrap(data)
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

class EntityEvents(Events):

    def __init__(self):
        self.__eventName = None

    def __check(self, obj, data, valueName):
        # type: (EventListener, dict, str) -> bool
        options = obj.options
        if type(options) != dict:
            options = None
        else:
            options = EntityEventsOptions(options)
        if options:
            if options.entities:
                entityIds = []
                for entity in options.entities:
                    entityIds.append(entity.id)
                if data[valueName] not in entityIds:
                    return False
            if options.entityTypes:
                if SComp.CreateEngineType(data[valueName]).GetEngineTypeStr() not in options.entityTypes:
                    return False
        return True
                
    def subscribe(self, callback, options=None):
        EventListener(self.eventName, callback, options, self.__check, Wrapper(None))
