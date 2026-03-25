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
        def test():
            print(serverApi.GetPlayerList())
            item = ItemStack("minecraft:stone", 1)
            # print(world.getAllPlayers())[0].container.addItem(item)
        system.runInterval(test, 40)
        def onChatSend(arg):
            # type: (ChatSendAfterEvent) -> None
            print(world.getAllPlayers())
            item = ItemStack(arg.message, 1)
            container = arg.sender.container
            container.addItem(item)
            existed = container.getItem(0)
            existed.setLore(["aaa1", "bbb2"])
            container.addItem(existed)
        world.afterEvents.chatSend.subscribe(onChatSend)
