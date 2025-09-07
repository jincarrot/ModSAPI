# -*- coding: utf-8 -*-
# from typing import Union, Dict

from ..Events.EntityEventSignals import *
from ..Events.PlayerEventSignals import *
from ..Events.ProjectileEventSignals import *
import mod.server.extraServerApi as serverApi
import mod.client.extraClientApi as clientApi

SComp = serverApi.GetEngineCompFactory()
CComp = clientApi.GetEngineCompFactory()


class WorldAfterEvents(object):
    """
    Contains a set of events that are available across the scope of the World.
    """

    def __init__(self):
        self.__entityDie = EntityDieAfterEventSignal() #
        self.__effectAdd = EffectAddAfterEventSignal() #
        self.__entityHealthChanged = EntityHealthChangedAfterEventSignal() #
        self.__entityHitBlock = 0#EntityHitBlockAfterEventSignal()
        self.__entityHitEntity = EntityHitEntityAfterEventSignal() #
        self.__entityHurt = EntityHurtAfterEventSignal() #
        self.__entityLoad = 0#EntityLoadAfterEventSignal()
        self.__entityRemove = EntityRemoveAfterEventSignal() # 
        self.__entitySpawn = EntitySpawnAfterEventSignal() #
        self.__chatSend = ChatSendAfterEventSignal() #
        self.__itemUse = ItemUseAfterEventSignal() #
        self.__itemCompleteUse = ItemCompleteUseAfterEventSignal() #
        self.__projectileHitBlock = ProjectileHitBlockAfterEventSignal() #
        self.__projectileHitEntity = ProjectileHitEntityAfterEventSignal() #

    @property
    def entityDie(self):
        """
        Supports registering for an event that fires after an entity has died.
        """
        return self.__entityDie

    @property
    def effectAdd(self):
        """
        This event fires when an effect, like poisoning, is added to an entity.
        """
        return self.__effectAdd

    @property
    def entityHealthChanged(self):
        """
        This event fires when entity health changes in any degree.
        """
        return self.__entityHealthChanged

    @property
    def _entityHitBlock(self):
        """
        This event fires when entity health changes in any degree.
        """
        return self.__entityHitBlock

    @property
    def entityHurt(self):
        """
        This event fires when an entity is hurt (takes damage).
        """
        return self.__entityHurt
    
    @property
    def entityHitEntity(self):
        """
        This event fires when an entity hits (that is, melee attacks) another entity.
        """
        return self.__entityHitEntity

    @property
    def entitySpawn(self):
        """
        This event fires when an entity is spawned.
        """
        return self.__entitySpawn

    @property
    def entityRemove(self):
        """Fires when an entity is removed (for example, potentially unloaded, or removed after being killed)."""
        return self.__entityRemove
    
    @property
    def chatSend(self):
        """
        This event is triggered after a chat message has been broadcast or sent to players.
        """
        return self.__chatSend
    
    @property
    def itemUse(self):
        """
        This event fires when an item is successfully used by a player.
        """
        return self.__itemUse
    
    @property
    def itemCompleteUse(self):
        """
        This event fires when a chargeable item completes charging
        """
        return self.__itemCompleteUse

    @property
    def projectileHitBlock(self):
        """This event fires when a projectile hits a block."""
        return self.__projectileHitBlock
    
    @property
    def projectileHitEntity(self):
        """This event fires when a projectile hits an entity."""
        return self.__projectileHitEntity

class WorldBeforeEvents(object):
    """
    A set of events that fire before an actual action occurs. 
    In most cases, you can potentially cancel or modify the impending event. 
    
    Note that in before events any APIs that modify gameplay state will not function and will throw an error. (e.g., dimension.spawnEntity)
    """

    def __init__(self):
        self.__chatSend = ChatSendBeforeEventSignal()
        self.__entityHurt = EntityHurtBeforeEventSignal()

    @property
    def chatSend(self):
        """
        This event is triggered after a chat message has been broadcast or sent to players.
        """
        return self.__chatSend
    
    @property
    def entityHurt(self):
        """
        This event fires when an entity is hurt (takes damage).
        """
        return self.__entityHurt
    

