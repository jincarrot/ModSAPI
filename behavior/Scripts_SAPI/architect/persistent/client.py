from ..subsystem import ClientSubsystem, SubsystemClient
from ..level.client import LevelClient
from .common import DBSource

level = LevelClient.getInst()

dbName = 'clientKVDb'

@SubsystemClient
class ClientKVDatabase(ClientSubsystem, DBSource):
    conf = level.configClient
    data = conf.GetConfigData(dbName)

    def __init__(self, system, engine, sysName):
        ClientSubsystem.__init__(self, system, engine, sysName)
        DBSource.__init__(self)

    def getData(self, key):
        return self.data.get(key)
    
    def _save(self):
        self.conf.SetConfigData(dbName, self.data)
    
    def setData(self, key, value):
        self.data[key] = value
        self._save()

    def removeData(self, key):
        self.data.pop(key)
        self._save()

    def clearData(self):
        self.data = {}
        self._save()