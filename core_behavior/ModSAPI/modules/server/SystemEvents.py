# -*- coding: utf-8 -*-
# from typing import Union, Dict

from .events.signals.WorldEventSignals import *

import mod.server.extraServerApi as serverApi
import mod.client.extraClientApi as clientApi

SComp = serverApi.GetEngineCompFactory()
CComp = clientApi.GetEngineCompFactory()


class SystemAfterEvents(object):
    """
    Provides a set of events that fire within the broader scripting system within Minecraft.
    """

    def __init__(self):
        self.__scriptEventReceive = ScriptEventCommandMessageAfterEventSignal()
        self.__clientEventReceive = ClientEventReceiveAfterEventSignal()

    @property
    def scriptEventReceive(self):
        """Fires when a script event is received. This includes events sent by both the client and the server."""
        return self.__scriptEventReceive
    
    @property
    def clientEventRecieve(self):
        return self.__clientEventReceive
