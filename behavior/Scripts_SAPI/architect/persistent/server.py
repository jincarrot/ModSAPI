from ..subsystem import ServerSubsystem, SubsystemServer
from ..level.server import LevelServer
from .common import DBSource

@SubsystemServer
class ServerKVDatabase(ServerSubsystem, DBSource):
    data = LevelServer.extraData

    def __init__(self, system, engine, sysName):
        ServerSubsystem.__init__(self, system, engine, sysName)
        DBSource.__init__(self)

    def getData(self, key):
        return self.data.GetExtraData(key)
    
    def setData(self, key, value):
        self.data.SetExtraData(key, value, autoSave=False)
        self.data.SaveExtraData()

    def removeData(self, key):
        self.data.SetExtraData(key, None)
        self.data.SaveExtraData()

    def clearData(self):
        self.data.CleanExtraData()