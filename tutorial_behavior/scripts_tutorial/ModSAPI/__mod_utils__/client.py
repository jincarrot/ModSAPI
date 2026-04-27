"""Don't modify this file."""
import mod.client.extraClientApi as clientApi

ClientSystem = clientApi.GetClientSystemCls()

class ModSAPILoadException(Exception):

    def __init__(self, *args):
        super().__init__(*args)

class Client(ClientSystem):
    """Main system of ModSAPI loader."""

    def __init__(self, namespace, systemName):
        ClientSystem.__init__(self, namespace, systemName)
        self.ListenForEvent(
            clientApi.GetEngineNamespace(), 
            clientApi.GetEngineSystemName(), 
            "LoadClientAddonScriptsAfter", 
            self, self.main)
    
    def main(self, data):
        from ...ModSAPI.client.beta import client
        if not client:
            raise ModSAPILoadException("Cannot get systems from ModSAPI! Make sure you have loaded the core pack.")
        from ...modMain import BASE_PATH
        from ...config import ENTRY_PATH_CLIENT
        try:
            if not ENTRY_PATH_CLIENT:
                return
            clientApi.ImportModule("%s.%s" % (BASE_PATH, ENTRY_PATH_CLIENT))
            print("[Info][ModSAPI][Client] Load entry file '%s' successfully." % ENTRY_PATH_CLIENT)
        except Exception as e:
            print("[Error][ModSAPI][Client] Load scripts failed! Cannot find entry file '%s'." % ENTRY_PATH_CLIENT)