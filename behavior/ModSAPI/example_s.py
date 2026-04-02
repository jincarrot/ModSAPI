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
            player = arg.sender
            loc = player.location
            a = world.structureManager.createFromWorld("test", player.dimension, loc, loc + (5, 5, 5))
            # world.structureManager.place(a, player.dimension, loc + (10, 0, 0))
            # world.structureManager.place(a, player.dimension, loc + (0, 0, 10), {"mirror": StructureMirrorAxis.XZ})
            # world.structureManager.place(a, player.dimension, loc + (0, 0, -10), {"mirror": StructureMirrorAxis.X})
            # world.structureManager.place(a, player.dimension, loc + (10, 0, -10), {"mirror": StructureMirrorAxis.Z})
            world.structureManager.place(a, player.dimension, loc + (10, 0, 10), {"rotation": StructureRotation.Rotate90})
            world.structureManager.place(a, player.dimension, loc + (10, 0, 5), {"rotation": StructureRotation.Rotate180})
            world.structureManager.place(a, player.dimension, loc + (5, 0, 5), {"rotation": StructureRotation.Rotate270})
        world.afterEvents.chatSend.subscribe(onChatSend)
