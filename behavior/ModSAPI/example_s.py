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
        print(world)
        def onChatSend(arg):
            item = ItemStack(arg.message, 1)
            container = arg.sender.container
            container.addItem(item)
            existed = container.getItem(0)
            existed.setLore(["aaa1", "bbb2"])
            container.addItem(existed)
        world.afterEvents.chatSend.subscribe(onChatSend)
