# coding=utf-8

from ..EventBases import *
import mod.server.extraServerApi as serverApi
from ..core.WorldEvents import *

class ExplosionAfterEventSignal(Events):
    """
    Manages callbacks that are connected to when an explosion occurs.
    """

    def __init__(self):
        Events.__init__(self)
        self.__eventName = "ExplosionServerEvent"

    def subscribe(self, callback):
        # type: (types.FunctionType) -> None
        """
        Adds a callback that will be called when an explosion occurs.
        """
        
        self._events[id(callback)] = EventListener(self.__eventName, callback, None, None, None, ExplosionAfterEvent)

class ScriptEventCommandMessageAfterEventSignal(Events):
    """
    Allows for registering an event handler that responds to inbound /scriptevent commands.
    """

    def __init__(self):
        Events.__init__(self)
        self.__eventName = "GlobalCommandServerEvent"

    def _check(self, obj, data, valueName):
        pass

    def subscribe(self, callback, options=None):
        # type: (types.FunctionType, dict) -> None
        """
        Registers a new ScriptEvent handler.
        """
        
        self._events[id(callback)] = EventListener(self.__eventName, callback, options, self._check, None, ExplosionAfterEvent)


class ExplosionBeforeEventSignal(Events):
    """
    Manages callbacks that are connected to when an explosion occurs, as it impacts individual blocks.
    """

    def __init__(self):
        Events.__init__(self)
        self.__eventName = "ExplosionServerEvent"

    def subscribe(self, callback):
        # type: (types.FunctionType) -> None
        """
        Adds a callback that will be called when an explosion occurs, as it impacts individual blocks.
        """
        
        self._events[id(callback)] = EventListener(self.__eventName, callback, None, None, None, ExplosionBeforeEvent)
