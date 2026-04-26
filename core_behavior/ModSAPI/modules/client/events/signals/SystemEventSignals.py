# coding=utf-8
from ..EventBases import *
import mod.server.extraServerApi as serverApi
from ..core.SystemEvents import *

class ServerSendToClientAfterEventSignal(Events):
    """
    Allows for registering an event handler that responds to inbound /scriptevent commands.
    """

    def __init__(self):
        Events.__init__(self)
        self.__eventName = "serverSendToClient"

    def _check(self, obj, data, valueName):
        # type: (EventListener, dict, str) -> bool
        if data['eventName'] == obj.options['__eventName']:
            return True
        return False

    def subscribe(self, eventName, callback, options={}):
        # type: (str, types.FunctionType, dict) -> None
        """
        Registers a new ScriptEvent handler.
        """
        options['__eventName'] = eventName
        self._events[id(callback)] = EventListener(self.__eventName, callback, options, self._check, None, ServerSendToClientAfterEvent, "ModSAPI", "system")
