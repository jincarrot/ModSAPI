# -*- coding: utf-8 -*-
# from typing import Union, Dict

from .events.signals.WorldEventSignals import *

class SystemAfterEvents(object):
    """
    Provides a set of events that fire within the broader scripting system within Minecraft.
    """

    @property
    def scriptEventReceive(self) -> ScriptEventCommandMessageAfterEventSignal:
        """Fires when a script event is received. This includes events sent by both the client and the server."""
    
    @property
    def clientEventRecieve(self) -> ClientEventReceiveAfterEventSignal: ...
