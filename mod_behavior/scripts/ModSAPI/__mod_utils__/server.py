
import mod.server.extraServerApi as serverApi

ServerSystem = serverApi.GetServerSystemCls()

class Server(ServerSystem):
    def __init__(self, namespace, systemName):
        ServerSystem.__init__(self, namespace, systemName)

        self.ListenForEvent(
            serverApi.GetEngineNamespace(), 
            serverApi.GetEngineSystemName(), 
            "LoadServerAddonScriptsAfter", 
            self, self.main)
    
    def main(self, data):
        from ...modMain import BASE_PATH
        from ...config import INDEX_PATH
        serverApi.ImportModule("%s.%s" % (BASE_PATH, INDEX_PATH))