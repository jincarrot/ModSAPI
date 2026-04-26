"""Don't modify this file."""
import mod.server.extraServerApi as serverApi

ServerSystem = serverApi.GetServerSystemCls()

class ModSAPILoadException(Exception):

    def __init__(self, *args):
        super().__init__(*args)

class Server(ServerSystem):
    """Main system of ModSAPI loader."""

    def __init__(self, namespace, systemName):
        ServerSystem.__init__(self, namespace, systemName)
        self.ListenForEvent(
            serverApi.GetEngineNamespace(), 
            serverApi.GetEngineSystemName(), 
            "LoadServerAddonScriptsAfter", 
            self, self.main)
    
    def main(self, data):
        from ...ModSAPI.server.beta import world
        if not world:
            raise ModSAPILoadException("Cannot get systems from ModSAPI! Make sure you have loaded the core pack.")
        from ...modMain import BASE_PATH
        from ...config import ENTRY_PATH_SERVER
        try:
            if not ENTRY_PATH_SERVER:
                return
            serverApi.ImportModule("%s.%s" % (BASE_PATH, ENTRY_PATH_SERVER))
            print("[Info][ModSAPI] Load entry file '%s' successfully." % ENTRY_PATH_SERVER)
        except Exception as e:
            print("[Error][ModSAPI] Load scripts failed! Cannot find entry file '%s'." % ENTRY_PATH_SERVER)