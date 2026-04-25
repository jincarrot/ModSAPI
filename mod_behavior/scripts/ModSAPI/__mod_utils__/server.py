
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
        from ...config import ENTRY_PATH
        try:
            serverApi.ImportModule("%s.%s" % (BASE_PATH, ENTRY_PATH))
            print("[Info][ModSAPI] Load entry file '%s' successfully." % ENTRY_PATH)
        except Exception as e:
            print("[Error][ModSAPI] Load scripts failed! Cannot find entry file '%s'." % ENTRY_PATH)