# coding=utf-8
from ...modules.server.Entity import *
from ...interfaces.Sources import *
from mod.common.minecraftEnum import *

class EntityDieAfterEvent(object):
    """
    Contains data related to the death of an entity in the game.
    """

    @property
    def damageSource(self):
        # type: () -> EntityDamageSource
        """
        If specified, provides more information on the source of damage that caused the death of this entity.
        """

    @property
    def deadEntity(self):
        # type: () -> Entity
        """
        Now-dead entity object.
        """

class EntityHurtAfterEvent(object):
    """
    Contains data related to the hurt of an entity in the game.
    """

    @property
    def damage(self):
        # type: () -> float
        """
        Describes the amount of damage caused.
        """
    
    @damage.setter
    def damage(self, value):
        # type: (float) -> None
        pass
    @property
    def damageSource(self):
        # type: () -> EntityDamageSource
        """
        Source information on the entity that may have applied this damage.
        """

    @property
    def hurtEntity(self):
        # type: () -> Entity
        """
        Entity that was hurt.
        """

class EntityHitEntityAfterEvent(object):
    """
    Contains information related to an entity hitting (melee attacking) another entity.
    """

    @property
    def damagingEntity(self):
        # type: () -> Entity
        """
        Entity that made a hit/melee attack.
        """

    @property
    def hitEntity(self):
        # type: () -> Entity
        """
        Entity that was hit by the attack.
        """

class EntitySpawnAfterEvent(object):
    """
    Contains data related to an entity spawning within the world.
    """
    
    @property
    def cause(self):
        # type: () -> str
        """None"""
    
    @property
    def entity(self):
        # type: () -> Entity 
        pass

class EntityLoadAfterEvent(object):
    """
    Contains data related to an entity loaded within the world. 
    
    This could happen when an unloaded chunk is reloaded, or when an entity changes dimensions.
    """
    
    @property
    def entity(self):
        # type: () -> Entity 
        """Contains data related to an entity loaded within the world. 
        This could happen when an unloaded chunk is reloaded, or when an entity changes dimensions."""

class EffectAddAfterEvent(object):
    """
    Contains information related to changes to an effect - like poison - being added to an entity.
    """

    @property
    def effect(self):
        # type: () -> Effect
        """
        Additional properties and details of the effect.
        """

    @property
    def entity(self):
        # type: () -> Entity
        """
        Entity that the effect is being added to.
        """

class EntityHealthChangedAfterEvent(object):
    """
    Contains information related to an entity when its health changes. 
    
    Warning: don't change the health of an entity in this event, or it will cause an infinite loop!
    """

    @property
    def entity(self):
        # type: () -> Entity
        """
        Entity whose health changed.
        """
    
    @property
    def oldValue(self):
        # type: () -> int
        """
        Old health value of the entity.
        """
    
    @property
    def newValue(self):
        # type: () -> Entity
        """
        New health value of the entity.
        """

class EntityRemoveAfterEvent(object):
    """
    Data for an event that happens when an entity is being removed from the world 
    (for example, the entity is unloaded because it is not close to players.)
    """

    @property
    def removedEntity(self):
        # type: () -> Entity
        """
        Reference to an entity that is being removed.
        """

class DataDrivenEntityTriggerAfterEvent(object):
    """
    Contains event registration related to firing of a data driven entity event - for example, the minecraft:ageable_grow_up event on a chicken.
    """

    @property
    def entity(self):
        # type: () -> Entity
        """
        Entity that the event triggered on.
        """
    
    @property
    def eventId(self):
        # type: () -> str
        """Name of the data driven event being triggered."""

    def getModifiers(self):
        pass


class EntityHurtBeforeEvent(object):
    """
    Contains data related to the hurt of an entity in the game.
    """

    @property
    def damage(self):
        # type: () -> int
        """
        Describes the amount of damage caused.
        """

    @damage.setter
    def damage(self, value):
        # type: (int) -> None
        pass

    @property
    def damageSource(self):
        # type: () -> EntityDamageCause
        """
        Source information on the entity that may have applied this damage.
        """

    @property
    def hurtEntity(self):
        # type: () -> Entity
        """
        Entity that was hurt.
        """

    @property
    def cancel(self):
        # type: () -> bool
        """returns whether the event is canceled."""
    
    @cancel.setter
    def cancel(self, value):
        # type: (bool) -> None
        pass

    @property
    def cancelKnock(self):
        # type: () -> None
        """Cancel the knockback of this damage."""
    
    @cancelKnock.setter
    def cancelKnock(self, value):
        # type: (bool) -> None
        pass
