# coding=utf-8
from typing import Callable
from ..EventBases import *
import mod.server.extraServerApi as serverApi
from ..core.SystemEvents import *

class ServerEventReceiveAfterEventSignal(Events):
    """
    Triggers when use ModSAPI.server.system.sendToClient.
    """

    def _check(self, obj, data, valueName):
        # type: (EventListener, dict, str) -> bool
        pass

    def subscribe(self, eventName, callback, options={}):
        # type: (str, Callable[[ServerEventReceiveAfterEvent], None], dict) -> None
        """
        Registers a new ScriptEvent handler.
        """
