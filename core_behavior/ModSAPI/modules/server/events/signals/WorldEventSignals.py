# coding=utf-8

from ..EventBases import *
import mod.server.extraServerApi as serverApi
from ..core.WorldEvents import *
from .....interfaces.EventOptions import ScriptEventMessageFilterOptions

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
        self.__eventName = "CustomCommandTriggerServerEvent"

    def _check(self, obj, data, valueName):
        # type: (EventListener, dict, str) -> bool
        namespaces = obj.options.get("namespaces", [])
        command = data['command']
        if command == 'scriptevent':
            messageId = data['args'][0]['value'] # type: str
            if len(messageId.split(":")) != 2 or messageId.split(":")[0] == "minecraft":
                data['return_failed'] = True
                data['return_msg_key'] = "标识符的命名空间必须有一个不是'minecraft:'"
                return False
            if not namespaces:
                return True
            else:
                if messageId.split(":")[0] in namespaces:
                    return True
            return False
        else:
            return False

    def subscribe(self, callback, options={}):
        # type: (types.FunctionType, ScriptEventMessageFilterOptions) -> None
        """
        Registers a new ScriptEvent handler.
        """
        
        self._events[id(callback)] = EventListener(self.__eventName, callback, options, self._check, None, ScriptEventCommandMessageAfterEvent)


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
