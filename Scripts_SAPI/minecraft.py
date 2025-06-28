# -*- coding: utf-8 -*-
import mod.server.extraServerApi as serverApi
from SAPI_S import *

def getWorld():
    # type: () -> (World)
    return serverApi.GetSystem("SAPI", "World")

def getSystem():
    # type: () -> System
    return serverApi.GetSystem("SAPI", "System")

world = getWorld()
system = getSystem()