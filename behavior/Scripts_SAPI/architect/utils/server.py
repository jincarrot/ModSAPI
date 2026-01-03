from ..level.server import LevelServer, compServer
from mod.common.minecraftEnum import EntityType

def runCommand(cmd, entityId):
    return LevelServer.command.SetCommand(cmd, entityId)

def motion(entityId, mot):
    if compServer.CreateEngineType(entityId).GetEngineType() == EntityType.Player:
        return compServer.CreateActorMotion(entityId).SetPlayerMotion(mot)
    else:
        return compServer.CreateActorMotion(entityId).SetMotion(mot)
    
def sound(entityId, sound):
    return LevelServer.command.SetCommand('playsound {} @a ~~1~ 2'.format(sound), entityId)

def particle(particle, pos):
    x, y, z = pos
    return LevelServer.command.SetCommand('particle {} {} {} {}'.format(particle, x, y, z))