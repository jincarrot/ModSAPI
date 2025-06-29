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
            temp['damagingEntity'] = Entity(damagingEntity)
        if damagingProjectile:
            temp['damagingProjectile'] = Entity(damagingProjectile)
        self.__damageSource = EntityDamageSource(temp)
        self.__deadEntity = Entity(data['id'])

    def __str__(self):
        data = {
            "damageSource": str(self.__damageSource),
            "deadEntity": str(self.__deadEntity)
        }
        return "<EntityDieAfterEvent> %s" % data

    @property
    def damageSource(self):
        # type: () -> EntityDamageCause
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
    Contains data related to the death of an entity in the game.
    """

    def __init__(self, data):
        temp = { "cause": data['cause'] }
        damagingEntity = data['srcId'] if data['srcId'] else None
        damagingProjectile = data['projectileId']
        if damagingEntity:
            temp['damagingEntity'] = Entity(damagingEntity)
        if damagingProjectile:
            temp['damagingProjectile'] = Entity(damagingProjectile)
        self.__damage = data['damage']
        self.__damageSource = EntityDamageSource(temp)
        self.__hurtEntity = Entity(data['entityId'])

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


class EntitySpawnAfterEvent(object):
    """
    Contains data related to an entity spawning within the world.
    """

    def __init__(self, data):
        self.__cause = None
        self.__entity = Entity(data['entityId'])
    
    @property
    def cause(self):
        # type: () ->str
        return self.__cause
    
    @property
    def entity(self):
        # type: () -> Entity 
        return self.__entity
