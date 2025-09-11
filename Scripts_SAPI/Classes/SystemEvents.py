# -*- coding: utf-8 -*-
# from typing import Union, Dict

from ..Events.WorldEventSignals import *

import mod.server.extraServerApi as serverApi
import mod.client.extraClientApi as clientApi

SComp = serverApi.GetEngineCompFactory()
CComp = clientApi.GetEngineCompFactory()


class SystemAfterEvents(object):
    """
    Provides a set of events that fire within the broader scripting system within Minecraft.
    """

    def __init__(self):
        self.__scriptEventReceive = None

