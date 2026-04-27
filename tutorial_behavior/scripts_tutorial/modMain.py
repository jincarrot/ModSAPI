# -*- coding: utf-8 -*-
from mod.common.mod import Mod
import mod.server.extraServerApi as serverApi
import mod.client.extraClientApi as clientApi
import config

class __PATH__:
    pass

BASE_PATH = __PATH__.__module__.split(".")[0]

@Mod.Binding(name="ModSAPI", version="1.0.0")
class ModSAPI(object):
    @Mod.InitServer()
    def ModSAPIServerInit(self):
        # =================== 不要动 =======================
        serverApi.RegisterSystem(config.NAMESPACE, config.SYSTEM_NAME_SERVER, "%s.ModSAPI.__mod_utils__.server.Server" % BASE_PATH)
        # ==================================================

    @Mod.InitClient()
    def ModSAPIClientInit(self):
        # =================== 不要动 =======================
        clientApi.RegisterSystem(config.NAMESPACE, config.SYSTEM_NAME_CLIENT, "%s.ModSAPI.__mod_utils__.client.Client" % BASE_PATH)
        # ==================================================
