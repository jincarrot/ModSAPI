import mod.client.extraClientApi as clientApi
import mod.server.extraServerApi as serverApi

def isServer():
    return clientApi.GetLocalPlayerId() == '-1'

class SubsystemManager:
    registeredSubsystems = []
    client = None
    server = None
    rawEngine = None
    rawSysName = None

    @staticmethod
    def getInst():
        return SubsystemManager.server if isServer() else SubsystemManager.client
    
    @staticmethod
    def createClientSystem(engine, sysName, clsPath):
        manager = SubsystemManager(
            clientApi.RegisterSystem(engine, sysName, clsPath),
            engine, sysName
        )
        manager.rawEngine = clientApi.GetEngineNamespace()
        manager.rawSysName = clientApi.GetEngineSystemName()
        SubsystemManager.client = manager
        return manager

    @staticmethod
    def createServerSystem(engine, sysName, clsPath):
        manager = SubsystemManager(
            serverApi.RegisterSystem(engine, sysName, clsPath),
            engine, sysName
        )
        manager.rawEngine = serverApi.GetEngineNamespace()
        manager.rawSysName = serverApi.GetEngineSystemName()
        SubsystemManager.server = manager
        return manager


    def __init__(self, system, engine, sysName):
        self.engine = engine
        self.sysName = sysName
        self.system = system
        self.subsystems = {}
        if isServer():
            from .levelServer import LevelServer
            LevelServer.game.AddTimer(0.1, lambda: self.appendAllSubsystems())
        else:
            from .levelClient import LevelClient
            LevelClient.game.AddTimer(0.1, lambda: self.appendAllSubsystems())

    def appendAllSubsystems(self):
        for subsystemCls in SubsystemManager.registeredSubsystems:
            self.addSubsystem(subsystemCls)


    def addSubsystem(self, subsystemCls):
        subSys = subsystemCls(self.system, self.engine, self.sysName)
        self.subsystems[subsystemCls.__name__] = subSys
        if hasattr(subSys, 'onInit'):
            subSys.onInit()
        print('[INFO] {} Subsystem "{}" has been initialized'.format('Server' if isServer() else 'Client', subSys.__class__.__name__))


    def getSubsystem(self, subsystemCls):
        # type: (object) -> 'Subsystem'
        return self.subsystems[subsystemCls.__name__]


    def removeSubsystem(self, subsystemCls):
        subSys = self.subsystems[subsystemCls.__name__]
        if hasattr(subSys, 'onDestroy'):
            subSys.onDestroy()
        del self.subsystems[subsystemCls.__name__]


    @staticmethod
    def registerSubsystem(subsystem):
        inst = SubsystemManager.getInst()
        if not inst:
            SubsystemManager.registeredSubsystems.append(subsystem)
        else:
            inst.addSubsystem(subsystem)


    @staticmethod
    def unregisterSubsystem(subsystem):
        SubsystemManager.registeredSubsystems.remove(subsystem)


def SubsystemClient(subsystemCls):
    """
    Decorator to auto register subsystem class
    """
    if not isServer():
        SubsystemManager.registerSubsystem(subsystemCls)
    return subsystemCls


def SubsystemServer(subsystemCls):
    """
    Decorator to auto register subsystem class
    """
    if isServer():
        SubsystemManager.registerSubsystem(subsystemCls)
    return subsystemCls


if 1 > 2:
    from mod.common.system.baseSystem import BaseSystem
    from mod.client.system.clientSystem import ClientSystem
    from mod.server.system.serverSystem import ServerSystem

def getSubsystemCls():
    return ServerSubsystem if isServer() else ClientSubsystem

class Subsystem:
    def __init__(self, system, engine, sysName):
        # type: (BaseSystem, str, str) -> 'None'
        self.system = system
        self.engine = engine
        self.sysName = sysName

    def onInit(self):
        pass

    def onDestroy(self):
        pass

    def getSystem(self):
        return self.system
    
    def getEngine(self):
        return self.engine
    
    def getSysName(self):
        return self.sysName
    
    def on(self, eventName, handler):
        self.system.ListenForEvent(
            self.engine,
            self.sysName,
            eventName,
            self,
            handler
        )

    def off(self, eventName, handler):
        self.system.UnListenForEvent(
            self.engine,
            self.sysName,
            eventName,
            self,
            handler
        )

    def listen(self, eventName, handler):
        manager = SubsystemManager.getInst()
        self.system.ListenForEvent(
            manager.rawEngine,
            manager.rawSysName,
            eventName,
            self,
            handler
        )

    def unlisten(self, eventName, handler):
        manager = SubsystemManager.getInst()
        self.system.UnListenForEvent(
            manager.rawEngine,
            manager.rawSysName,
            eventName,
            self,
            handler
        )

    def broadcast(self, eventName, eventData):
        self.system.BroadcastEvent(eventName, eventData)

    def onInit(self):
        pass

    def onDestroy(self):
        pass

class Location:
    def __init__(self, pos, dim):
        self.pos = pos
        self.dim = dim

class ServerSubsystem(Subsystem):
    def __init__(self, system, engine, sysName):
        # type: (ServerSystem, str, str) -> 'None'
        Subsystem.__init__(self, system, engine, sysName)

    def sendAllClients(self, eventName, eventData):
        self.system.BroadcastToAllClient(eventName, eventData)

    def sendClient(self, targetIds, eventName, eventData):
        if type(targetIds) == str:
            self.system.NotifyToClient(targetIds, eventName, eventData)
            return

        self.system.NotifyToMultiClients(targetIds, eventName, eventData)

    def spawnEntity(self, template, location, rot, isNpc=False, isGlobal=False):
        if type(template) == str:
            return self.system.CreateEngineEntityByTypeStr(template, location.pos, rot, dimensionId=location.dim, isNpc=isNpc, isGlobal=isGlobal)
        elif type(template) == dict:
            return self.system.CreateEngineEntityByNBT(template, location.pos, rot, dimensionId=location.dim, isNpc=isNpc, isGlobal=isGlobal)
        return None
        
    def destroyEntity(self, entityId):
        return self.system.DestroyEntity(entityId)
    
    def spawnItem(self, itemDict, location):
        return self.system.CreateEngineItemEntity(itemDict, dimensionId=location.dim, pos=location.pos)


class ClientSubsystem(Subsystem):
    def __init__(self, system, engine, sysName):
        # type: (ClientSystem, str, str) -> 'None'
        Subsystem.__init__(self, system, engine, sysName)

    def sendServer(self, eventName, eventData):
        self.system.NotifyToServer(eventName, eventData)

    def spawnEntity(self, typeStr, pos, rot):
        if type(typeStr) == str:
            return self.system.CreateClientEntityByTypeStr(typeStr, pos, rot)
        return None
    
    def destroyEntity(self, entityId):
        self.system.DestroyClientEntity(entityId)

    def createSfx(self, path, pos=None, rot=None, scale=None):
        return self.system.CreateEngineSfx(path, pos, rot, scale)
    
    def createParticle(self, path, pos):
        return self.system.CreateEngineParticle(path, pos)
    
    def createEffectBind(self, path, bindEntity, aniName):
        return self.system.CreateEngineEffectBind(path, bindEntity, aniName)
    
    def destroySfx(self, entityId):
        return self.system.DestroyEntity(entityId)


ScreenNode = clientApi.GetScreenNodeCls()
class UiSubsystem(ScreenNode, ClientSubsystem):
    def __init__(self, engine, system, params):
        manager = SubsystemManager.getInst()
        ScreenNode.__init__(self, engine, system, params)
        ClientSubsystem.__init__(self, manager.system, engine, system)

    ns = 'xxx_roninUi_xxx'
    inst = None

    @classmethod
    def defineUi(cls, uiDef):
        return clientApi.RegisterUI(
            cls.ns,
            cls.__name__,
            cls.__module__ + '.' + cls.__name__,
            uiDef
        )
    
    @classmethod
    def getOrCreate(cls, **params):
        if cls.inst:
            return cls.inst

        print(cls.ns, cls.__name__, params)
        ui = clientApi.CreateUI(cls.ns, cls.__name__, params)
        cls.inst = ui
        return ui