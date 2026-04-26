# coding=utf-8
from ..EventBases import *
import mod.server.extraServerApi as serverApi
from ..core.SystemEvents import *

class ServerEventReceiveAfterEventSignal(Events):
    """
    Allows for registering an event handler that responds to inbound /scriptevent commands.
    """

    def __init__(self):
        Events.__init__(self)
        self.__eventName = "serverSendToClient"

    def _check(self, obj, data, valueName):
        # type: (EventListener, dict, str) -> bool
        if data['eventName'] == valueName:
            return True
        return False

    def subscribe(self, eventName, callback, options={}):
        # type: (str, types.FunctionType, dict) -> None
        """
        Registers a new ScriptEvent handler.
        """
        self._events[id(callback)] = EventListener(self.__eventName, callback, options, self._check, eventName, ServerEventReceiveAfterEvent, "ModSAPI", "system")
