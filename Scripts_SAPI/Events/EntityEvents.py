# coding=utf-8
from ..Classes.Entity import *
from ..Interfaces.Sources import *


class EntityDieAfterEvent(object):
    """
    Contains data related to the death of an entity in the game.
    """

    def __init__(self, data):
        temp = { "cause": data['cause'] }
        damagingEntity = data['attacker'] if data['attacker'] else None
        damagingProjectile = None
        if damagingEntity and SComp.CreateEntityComponent(damagingEntity).HasComponent(EntityComponentType.projectile):
            damagingProjectile = damagingEntity
            damagingEntity = SComp.CreateActorOwner(damagingProjectile).GetEntityOwner()
        if damagingEntity:
            temp['damagingEntity'] = createEntity(damagingEntity)
        if damagingProjectile:
            temp['damagingProjectile'] = createEntity(damagingProjectile)
        self.__damageSource = EntityDamageSource(temp)
        self.__deadEntity = createEntity(data['id'])

    def __str__(self):
        data = {
            "damageSource": str(self.__damageSource),
            "deadEntity": str(self.__deadEntity)
        }
        return "<EntityDieAfterEvent> %s" % data

    @property
    def damageSource(self):
        # type: () -> EntityDamageSource
        """
        If specified, provides more information on the source of damage that caused the death of this entity.
        """
        return self.__damageSource

    @property
    def deadEntity(self):
        # type: () -> Entity
        """
        Now-dead entity object.
        """
        return self.__deadEntity

class EntityHurtAfterEvent(object):
    """
    Contains data related to the hurt of an entity in the game.
    """

    def __init__(self, data):
        self.__data = data
        temp = { "cause": data['cause'] }
        damagingEntity = data['srcId'] if data['srcId'] else None
        damagingProjectile = data['projectileId']
        if damagingEntity:
            temp['damagingEntity'] = createEntity(damagingEntity)
        if damagingProjectile:
            temp['damagingProjectile'] = createEntity(damagingProjectile)
        self.__damage = data['damage']
        self.__damageSource = EntityDamageSource(temp)
        self.__hurtEntity = createEntity(data['entityId'])

    def __str__(self):
        data = {
            "damage": self.damage,
            "damageSource": str(self.damageSource),
            "hurtEntity": str(self.hurtEntity)
        }
        return "<EntityHurtAfterEvent> %s" % data

    @property
    def damage(self):
        # type: () -> float
        """
        Describes the amount of damage caused.
        """
        return self.__damage
    
    @damage.setter
    def damage(self, value):
        # type: (float) -> None
        self.__damage = value
        self.__data['damage'] = value

    @property
    def damageSource(self):
        # type: () -> EntityDamageSource
        """
        Source information on the entity that may have applied this damage.
        """
        return self.__damageSource

    @property
    def hurtEntity(self):
        # type: () -> Entity
        """
        Entity that was hurt.
        """
        return self.__hurtEntity

class EntityHitEntityAfterEvent(object):
    """
    Contains information related to an entity hitting (melee attacking) another entity.
    """

    def __init__(self, data):
        self.__damagingEntity = createEntity(data['srcId'] if 'cause' in data else data['playerId'])
        self.__hitEntity = createEntity(data['entityId'] if 'cause' in data else data['victimId'])

    def __str__(self):
        data = {
            "damagingEntity": str(self.__damagingEntity),
            "hitEntity": str(self.__hitEntity)
        }
        return "<EntityHurtAfterEvent> %s" % data


    @property
    def damagingEntity(self):
        # type: () -> Entity
        """
        Entity that made a hit/melee attack.
        """
        return self.__damagingEntity

    @property
    def hitEntity(self):
        # type: () -> Entity
        """
        Entity that was hit by the attack.
        """
        return self.__hitEntity

class EntitySpawnAfterEvent(object):
    """
    Contains data related to an entity spawning within the world.
    """

    def __init__(self, data):
        self.__cause = None
        self.__entity = createEntity(data['id'])
        if SComp.CreateEntityDefinitions(self.__entity.id).IsNaturallySpawned():
            self.__cause = 'Spawned'
    
    @property
    def cause(self):
        # type: () -> str
        """None"""
        return self.__cause
    
    @property
    def entity(self):
        # type: () -> Entity 
        return self.__entity

class EntityLoadAfterEvent(object):
    """
    Contains data related to an entity loaded within the world. 
    
    This could happen when an unloaded chunk is reloaded, or when an entity changes dimensions.
    """

    def __init__(self, data):
        self.__entity = createEntity(data['id'])
    
    @property
    def entity(self):
        # type: () -> Entity 
        """Contains data related to an entity loaded within the world. 
        This could happen when an unloaded chunk is reloaded, or when an entity changes dimensions."""
        return self.__entity

class EffectAddAfterEvent(object):
    """
    Contains information related to changes to an effect - like poison - being added to an entity.
    """

    def __init__(self, data):
        self.__effect = Effect(data['effectName'], data['effectDuration'], data['effectAmplifier'])
        self.__entity = createEntity(data['entityId'])

    def __str__(self):
        data = {
            "effect": str(self.__effect),
            "entity": str(self.__entity)
        }
        return "<EffectAddAfterEvent> %s" % data

    @property
    def effect(self):
        # type: () -> Effect
        """
        Additional properties and details of the effect.
        """
        return self.__effect

    @property
    def entity(self):
        # type: () -> Entity
        """
        Entity that the effect is being added to.
        """
        return self.__entity

class EntityHealthChangedAfterEvent(object):
    """
    Contains information related to an entity when its health changes. 
    
    Warning: don't change the health of an entity in this event, or it will cause an infinite loop!
    """

    def __init__(self, data):
        self.__newValue = data['to']
        self.__entity = createEntity(data['entityId'])
        self.__oldValue = data['from']

    def __str__(self):
        data = {
            "entity": str(self.__entity)
        }
        return "<EntityHealthChangedAfterEvent> %s" % data

    @property
    def entity(self):
        # type: () -> Entity
        """
        Entity whose health changed.
        """
        return self.__entity
    
    @property
    def oldValue(self):
        # type: () -> int
        """
        Old health value of the entity.
        """
        return self.__oldValue
    
    @property
    def newValue(self):
        # type: () -> Entity
        """
        New health value of the entity.
        """
        return self.__newValue

class EntityRemoveAfterEvent(object):
    """
    Data for an event that happens when an entity is being removed from the world 
    (for example, the entity is unloaded because it is not close to players.)
    """

    def __init__(self, data):
        self.__removedEntity = createEntity(data['id'])

    def __str__(self):
        data = {
            "removedEntity": str(self.__removedEntity)
        }
        return "<EntityRemoveAfterEvent> %s" % data

    @property
    def removedEntity(self):
        # type: () -> Entity
        """
        Reference to an entity that is being removed.
        """
        return self.__removedEntity

class DataDrivenEntityTriggerAfterEvent(object):
    """
    Contains event registration related to firing of a data driven entity event - for example, the minecraft:ageable_grow_up event on a chicken.
    """

    def __init__(self, data):
        self.__eventId = data['eventName']
        self.__entity = createEntity(data['entityId'])

    def __str__(self):
        data = {
            "entity": str(self.__entity),
            "eventId": self.__eventId
        }
        return "<DataDrivenEntityTriggerAfterEvent> %s" % data

    @property
    def entity(self):
        # type: () -> Entity
        """
        Entity that the event triggered on.
        """
        return self.__entity
    
    @property
    def eventId(self):
        # type: () -> str
        """Name of the data driven event being triggered."""
        return self.__eventId

    def getModifiers(self):
        pass


class EntityHurtBeforeEvent(object):
    """
    Contains data related to the hurt of an entity in the game.
    """

    def __init__(self, data):
        self.__data = data
        temp = { "cause": data['cause'] , "customTag": data['customTag']}
        damagingEntity = data['srcId'] if data['srcId'] else None
        damagingProjectile = data['projectileId']
        if damagingEntity:
            temp['damagingEntity'] = createEntity(damagingEntity)
        if damagingProjectile:
            temp['damagingProjectile'] = createEntity(damagingProjectile)
        self.__damage = data['damage']
        self.__damageSource = EntityDamageSource(temp)
        self.__hurtEntity = createEntity(data['entityId'])

    def __str__(self):
        data = {
            "damage": self.damage,
            "damageSource": str(self.damageSource),
            "hurtEntity": str(self.hurtEntity)
        }
        return "<EntityHurtAfterEvent> %s" % data

    @property
    def damage(self):
        # type: () -> int
        """
        Describes the amount of damage caused.
        """
        return self.__damage

    @damage.setter
    def damage(self, value):
        # type: (int) -> None
        self.__damage = value
        self.__data['damage'] = value

    @property
    def damageSource(self):
        # type: () -> EntityDamageCause
        """
        Source information on the entity that may have applied this damage.
        """
        return self.__damageSource

    @property
    def hurtEntity(self):
        # type: () -> Entity
        """
        Entity that was hurt.
        """
        return self.__hurtEntity

    @property
    def cancel(self):
        # type: () -> bool
        """returns whether the event is canceled."""
        return self.__data['cancel']
    
    @cancel.setter
    def cancel(self, value):
        # type: (bool) -> None
        self.__data['damage'] = 0
        self.__data['knock'] = False
        self.__data['ignite'] = False

    @property
    def cancelKnock(self):
        # type: () -> None
        """Cancel the knockback of this damage."""
        return self.__data['knock']
    
    @cancelKnock.setter
    def cancelKnock(self, value):
        # type: (bool) -> None
        self.__data['knock'] = value
