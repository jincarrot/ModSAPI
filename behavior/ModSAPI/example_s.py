import mod.server.extraServerApi as serverApi
from server import *

ServerSystem = serverApi.GetServerSystemCls()

class S(ServerSystem):
    def __init__(self, namespace, systemName):
        ServerSystem.__init__(self, namespace, systemName)
        self.ListenForEvent(
            serverApi.GetEngineNamespace(), 
            serverApi.GetEngineSystemName(), 
            "LoadServerAddonScriptsAfter", 
            self, self.main)

    def main(self, data):
        def onChatSend(arg):
            # type: (ChatSendAfterEvent) -> None
            print(arg.sender.runCommand("kill @e").successCount)
        world.afterEvents.chatSend.subscribe(onChatSend)
        def a(arg):
            print(arg)
            print(arg.sourceEntity)
            print(arg.sourceType)
        #system.afterEvents.scriptEventReceive.subscribe(a)
