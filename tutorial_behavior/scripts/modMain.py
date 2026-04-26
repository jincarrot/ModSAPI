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
        serverApi.RegisterSystem(config.NAMESPACE, config.SYSTEM_NAME, "%s.ModSAPI.__mod_utils__.server.Server" % BASE_PATH)
        # ==================================================

        serverApi.RegisterSystem("sample", "server", "scripts.example_use_modules_server.Server")
        """网易原生使用方法，先注册类"""

    @Mod.InitClient()
    def ModSAPIClientInit(self):
        pass
