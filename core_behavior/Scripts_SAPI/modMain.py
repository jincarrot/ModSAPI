# -*- coding: utf-8 -*-

from mod.common.mod import Mod
import mod.server.extraServerApi as serverApi
import mod.client.extraClientApi as clientApi

from .architect.subsystem import SubsystemManager

def Destroy():
    from Utils.Expression import old
    import math
    math.sin = old.sin
    math.cos = old.cos
    math.pow = old.pow
    abs = old.abs
    max = old.max
    min = old.min


@Mod.Binding(name="Script_SAPI", version="0.0.1")
class Script_SAPI(object):
    @Mod.InitServer()
    def SAPI_ServerInit(self):
        serverApi.RegisterSystem("SAPI", "world",
                                 "Scripts_SAPI.SAPI_S.World")
        serverApi.RegisterSystem("SAPI", "system",
                                 "Scripts_SAPI.SAPI_S.System")
        SubsystemManager.createServerSystem('SAPI', 'Base', 'Scripts_SAPI.minecraft.SAPIS')

    @Mod.InitClient()
    def SAPI_ClientInit(self):
        clientApi.RegisterSystem("SAPI", "manager",
                                 "Scripts_SAPI.SAPI_C.Manager")
        SubsystemManager.createClientSystem('SAPI', 'SAPI_C', 'Scripts_SAPI.SAPI_C.SAPI_C')

    @Mod.DestroyServer()
    def SAPI_UtilsDestory(self):
        Destroy()
