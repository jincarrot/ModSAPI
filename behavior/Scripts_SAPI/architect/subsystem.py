import mod.client.extraClientApi as clientApi
import mod.server.extraServerApi as serverApi

isServer = clientApi.GetLocalPlayerId() == '-1'

class SubsystemManager:
    registeredSubsystems = []
    inst = None
    initialized = False

    @staticmethod
    def getInst():
        return SubsystemManager.inst
    
    @staticmethod
    def createClientSystem(engine, sysName, clsPath):
        return SubsystemManager(
            clientApi.RegisterSystem(engine, sysName, clsPath),
            engine, sysName
        )

    @staticmethod
    def createServerSystem(engine, sysName, clsPath):
        return SubsystemManager(
            serverApi.RegisterSystem(engine, sysName, clsPath),
            engine, sysName
        )


    def __init__(self, system, engine, sysName):
        self.engine = engine
        self.sysName = sysName
        self.system = system
        self.subsystems = {}

        # Initialize all registered subsystems
        for subsystemCls in SubsystemManager.registeredSubsystems:
            self.addSubsystem(subsystemCls)
        SubsystemManager.inst = self
        SubsystemManager.initialized = True


    def addSubsystem(self, subsystemCls):
        subSys = subsystemCls(self.system, self.engine, self.sysName)
        self.subsystems[subsystemCls] = subSys
        if hasattr(subSys, 'onInit'):
            subSys.onInit()


    def getSubsystem(self, subsystemCls):
        # type: (str) -> 'Subsystem'
        return self.subsystems[subsystemCls]


    def removeSubsystem(self, subsystemCls):
        subSys = self.subsystems[subsystemCls]
        if hasattr(subSys, 'onDestroy'):
            subSys.onDestroy()
        del self.subsystems[subsystemCls]


    @staticmethod
    def registerSubsystem(subsystem):
        if not SubsystemManager.initialized:
            SubsystemManager.registeredSubsystems.append(subsystem)
        else:
            SubsystemManager.getInst().addSubsystem(subsystem)


    @staticmethod
    def unregisterSubsystem(subsystem):
        SubsystemManager.registeredSubsystems.remove(subsystem)


def SubsystemClient(subsystemCls):
    """
    Decorator to auto register subsystem class
    """
    if not isServer:
        SubsystemManager.registerSubsystem(subsystemCls)
    return subsystemCls


def SubsystemServer(subsystemCls):
    """
    Decorator to auto register subsystem class
    """
    if isServer:
        SubsystemManager.registerSubsystem(subsystemCls)
    return subsystemCls


if 1 > 2:
    from mod.common.system.baseSystem import BaseSystem
    from mod.client.system.clientSystem import ClientSystem
    from mod.server.system.serverSystem import ServerSystem

def getSubsystemCls():
    if isServer:
        return ServerSubsystem
    else:
        return ClientSubsystem

class Subsystem:
    def __init__(self, system, engine, sysName):
        # type: (BaseSystem, str, str) -> 'None'
        self.system = system
        self.engine = engine
        self.sysName = sysName

    def getSystem(self):
        return self.system
    
    def getEngine(self):
        return self.engine
    
    def getSysName(self):
        return self.sysName
    
    def listen(self, eventName, handler):
        self.system.ListenForEvent(
            self.engine,
            self.sysName,
            eventName,
            self,
            handler
        )

    @classmethod
    def Listen(cls, eventName, handler):
        inst = SubsystemManager.getInst()
        subsystem = inst.getSubsystem(cls)
        if subsystem:
            subsystem.listen(eventName, handler)

    def unlisten(self, eventName, handler):
        self.system.UnListenForEvent(
            self.engine,
            self.sysName,
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