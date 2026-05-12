# -*- coding: utf-8 -*-
from mod.common.mod import Mod
import mod.server.extraServerApi as serverApi
import mod.client.extraClientApi as clientApi
from .config import Namespace


@Mod.Binding(name="ModSAPI", version="1.0.0")
class ModSAPI(object):
    @Mod.InitServer()
    def ModSAPIServerInit(self):
        basePath = self.__class__.__module__.split(".")[0]
        serverApi.RegisterSystem(Namespace, "core", "%s.utils.core.CoreSystem" % basePath)
        serverApi.RegisterSystem(Namespace, "world", "%s.modules.server.World.World" % basePath)
        serverApi.RegisterSystem(Namespace, "system", "%s.modules.server.System.System" % basePath)
        serverApi.RegisterSystem(Namespace, "modules", "%s.utils.modules.Modules" % basePath)
        serverApi.RegisterSystem(Namespace, "enums", "%s.utils.enums.Enums" % basePath)
        serverApi.RegisterSystem(Namespace, "components", "%s.utils.components.Components" % basePath)
        
        """serverApi.RegisterSystem("SAPI", "system",
                                 "Scripts_SAPI.SAPI_S.System")
        SubsystemManager.createServerSystem('SAPI', 'Base', 'Scripts_SAPI.minecraft.SAPIS')"""

    @Mod.InitClient()
    def ModSAPIClientInit(self):
        basePath = self.__class__.__module__.split(".")[0]
        clientApi.RegisterSystem(Namespace, "client", "%s.modules.client.Client.Client" % basePath)
        clientApi.RegisterSystem(Namespace, "client_core", "%s.utils.client_core.Core" % basePath)
        """ SubsystemManager.createClientSystem('SAPI', 'SAPI_C', 'Scripts_SAPI.SAPI_C.SAPI_C')"""

    @Mod.DestroyServer()
    def ModSAPIUtilsDestory(self):
        pass
