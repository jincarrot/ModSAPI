# -*- coding: utf-8 -*-
from mod.common.mod import Mod
import mod.server.extraServerApi as serverApi
import mod.client.extraClientApi as clientApi

# from .architect.subsystem import SubsystemManager


@Mod.Binding(name="ModSAPI", version="1.0.0")
class ModSAPI(object):
    @Mod.InitServer()
    def ModSAPIServerInit(self):
        serverApi.RegisterSystem("ModSAPI", "core", "ModSAPI.utils.core.CoreSystem")
        serverApi.RegisterSystem("ModSAPI", "world", "ModSAPI.modules.server.World.World")
        serverApi.RegisterSystem("ModSAPI", "system", "ModSAPI.modules.server.System.System")
        serverApi.RegisterSystem("ModSAPI", "modules", "ModSAPI.utils.modules.Modules")
        serverApi.RegisterSystem("ModSAPI", "enums", "ModSAPI.utils.enums.Enums")
        serverApi.RegisterSystem("ModSAPI", "components", "ModSAPI.utils.components.Components")
        
        """serverApi.RegisterSystem("SAPI", "system",
                                 "Scripts_SAPI.SAPI_S.System")
        SubsystemManager.createServerSystem('SAPI', 'Base', 'Scripts_SAPI.minecraft.SAPIS')"""

    @Mod.InitClient()
    def ModSAPIClientInit(self):
        clientApi.RegisterSystem("ModSAPI", "client", "ModSAPI.modules.client.Client.Client")
        clientApi.RegisterSystem("ModSAPI", "client_core", "ModSAPI.utils.client_core.Core")
        """ SubsystemManager.createClientSystem('SAPI', 'SAPI_C', 'Scripts_SAPI.SAPI_C.SAPI_C')"""

    @Mod.DestroyServer()
    def ModSAPIUtilsDestory(self):
        Destroy()
