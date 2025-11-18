from .subsystem import ServerSubsystem, SubsystemServer
from .level import LevelServer

@SubsystemServer
class ServerKVDatabase(ServerSubsystem):
    data = LevelServer.extraData

    def getData(self, key):
        return self.data.GetExtraData(key)
    
    def setData(self, key, value):
        self.data.SetExtraData(key, value)

    def removeData(self, key):
        self.data.SetExtraData(key, None)

    def clearData(self):
        self.data.CleanExtraData()

