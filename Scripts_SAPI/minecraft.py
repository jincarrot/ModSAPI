# -*- coding: utf-8 -*-
import mod.server.extraServerApi as serverApi
import SAPI_S as SAPI

def getWorld():
    # type: () -> SAPI.World
    return serverApi.GetSystem("SAPI", "world")

def getSystem():
    # type: () -> SAPI.System
    return serverApi.GetSystem("SAPI", "system")

world = getWorld()
system = getSystem()