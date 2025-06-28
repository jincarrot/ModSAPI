# -*- coding: utf-8 -*-

from mod.common.mod import Mod
import mod.server.extraServerApi as serverApi
import mod.client.extraClientApi as clientApi


@Mod.Binding(name="Script_SAPI", version="0.0.1")
class Script_SAPI(object):

    def __init__(self):
        pass

    @Mod.InitServer()
    def SAPI_ServerInit(self):
        serverApi.RegisterSystem("SAPI", "world",
                                 "Scripts_SAPI.SAPI_S.World")
        serverApi.RegisterSystem("SAPI", "system",
                                 "Scripts_SAPI.SAPI_S.System")
        serverApi.RegisterSystem("SAPI", "Base",
                                 "Scripts_SAPI.SAPI_S.SAPIS")

    @Mod.InitClient()
    def SAPI_ClientInit(self):
        clientApi.RegisterSystem("SAPI", "SAPI_C",
                                 "Scripts_SAPI.SAPI_C.SAPI_C")

