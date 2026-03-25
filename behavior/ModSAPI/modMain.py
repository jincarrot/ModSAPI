# -*- coding: utf-8 -*-
from mod.common.mod import Mod
import mod.server.extraServerApi as serverApi
import mod.client.extraClientApi as clientApi

# from .architect.subsystem import SubsystemManager

def Destroy():
    from utils.expression import old
    import math
    math.sin = old.sin
    math.cos = old.cos
    math.pow = old.pow
    abs = old.abs
    max = old.max
    min = old.min


@Mod.Binding(name="ModSAPI", version="1.0.0")
class ModSAPI(object):
    @Mod.InitServer()
    def ModSAPIServerInit(self):
        serverApi.RegisterSystem("ModSAPI", "world",
                                 "ModSAPI.modules.server.World.World")
        serverApi.RegisterSystem("ModSAPI", "modules",
                                 "ModSAPI.utils.modules.Modules")
        
        serverApi.RegisterSystem("Sample", "s",
                                 "ModSAPI.example_s.S")
        """serverApi.RegisterSystem("SAPI", "system",
                                 "Scripts_SAPI.SAPI_S.System")
        SubsystemManager.createServerSystem('SAPI', 'Base', 'Scripts_SAPI.minecraft.SAPIS')"""

    @Mod.InitClient()
    def ModSAPIClientInit(self):
        """ clientApi.RegisterSystem("SAPI", "manager", "Scripts_SAPI.SAPI_C.Manager")
        SubsystemManager.createClientSystem('SAPI', 'SAPI_C', 'Scripts_SAPI.SAPI_C.SAPI_C')"""

    @Mod.DestroyServer()
    def ModSAPIUtilsDestory(self):
        Destroy()
