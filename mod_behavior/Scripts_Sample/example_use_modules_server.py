"""网易原生使用方法，适用于已有项目，需要将ModSAPI集成到现有项目中。"""

import mod.server.extraServerApi as serverApi
from ModSAPI.server.beta import *

ServerSystem = serverApi.GetServerSystemCls()

class Server(ServerSystem):
    def __init__(self, namespace, systemName):
        ServerSystem.__init__(self, namespace, systemName)

        self.ListenForEvent(
            serverApi.GetEngineNamespace(), 
            serverApi.GetEngineSystemName(), 
            "LoadServerAddonScriptsAfter", 
            self, self.main)
        """需要先监听LoadServerAddonScriptsAfter事件，待系统加载完毕后才能使用系统和模块。"""

    def main(self, data):
        def onChatSend(arg):
            # type: (ChatSendAfterEvent) -> None
            print("ChatSend event in 'example_use_modules_server', sender: %s" % str(arg.sender))
            
        world.afterEvents.chatSend.subscribe(onChatSend) # 监听事件

