# -*- coding: utf-8 -*-
# from typing import Union, Dict

from ..Events.EntityEventSignals import *
from ..Events.PlayerEventSignals import *
from ..Events.ProjectileEventSignals import *
from ..Events.BlockEventSignals import *
from ..Events.WorldEventSignals import *

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
        self.__entityLoad = EntityLoadAfterEventSignal()
        self.__entityRemove = EntityRemoveAfterEventSignal() # 
        self.__entitySpawn = EntitySpawnAfterEventSignal() #
        self.__chatSend = ChatSendAfterEventSignal() #
        self.__itemUse = ItemUseAfterEventSignal() #
        self.__itemCompleteUse = ItemCompleteUseAfterEventSignal() #
        self.__projectileHitBlock = ProjectileHitBlockAfterEventSignal() #
        self.__projectileHitEntity = ProjectileHitEntityAfterEventSignal() #
        self.__blockExplode = BlockExplodeAfterEventSignal()
        self.__explosion = ExplosionAfterEventSignal()
        self.__itemStartUseOn = ItemStartUseOnAfterEventSignal()
        self.__playerDimensionChange = PlayerDimensionChangeAfterEventSignal()
        self.__playerJoin = PlayerJoinAfterEventSignal()
        self.__playerLeave = PlayerLeaveAfterEventSignal()
        self.__playerSpawn = PlayerSpawnAfterEventSignal()
        self.__playerInventoryItemChange = PlayerInventoryItemChangeAfterEventSignal()
        self.__playerBreakBlock = PlayerBreakBlockAfterEventSignal()
        self.__playerPlaceBlock = PlayerPlaceBlockAfterEventSignal()

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
    def entityLoad(self):
        """
        Fires when an entity is loaded.
        """
        return self.__entityLoad

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

    @property
    def itemStartUseOn(self):
        """This event fires when a chargeable item starts charging."""
        return self.__itemStartUseOn
    
    @property
    def blockExplode(self):
        """This event fires for each BlockLocation destroyed by an explosion. 
        It is fired after the blocks have already been destroyed."""
        return self.__blockExplode
    
    @property
    def explosion(self):
        """This event is fired after an explosion occurs."""
        return self.__explosion
    
    @property
    def playerDimensionChange(self):
        """Fires when a player moved to a different dimension."""
        return self.__playerDimensionChange
    
    @property
    def playerJoin(self):
        """
        This event fires when a player joins a world. 
        
        See also playerSpawn for another related event you can trap for when a player is spawned the first time within a world.
        """
        return self.__playerJoin

    @property
    def playerLeave(self):
        """This event fires when a player leaves a world."""
        return self.__playerLeave

    @property
    def playerSpawn(self):
        """
        This event fires when a player spawns or respawns. 
        
        Note that an additional flag within this event will tell you whether the player is spawning right after join vs. a respawn.
        """
        return self.__playerSpawn

    @property
    def playerInventoryItemChange(self):
        """This event fires when an item gets added or removed to the player's inventory."""
        return self.__playerInventoryItemChange
    
    @property
    def playerBreakBlock(self):
        """This event fires for a block that is broken by a player."""
        return self.__playerBreakBlock
    
    @property
    def playerPlaceBlock(self):
        """This event fires for a block that is placed by a player."""
        return self.__playerPlaceBlock
    
class WorldBeforeEvents(object):
    """
    A set of events that fire before an actual action occurs. 
    In most cases, you can potentially cancel or modify the impending event. 
    
    Note that in before events any APIs that modify gameplay state will not function and will throw an error. (e.g., dimension.spawnEntity)
    """

    def __init__(self):
        self.__chatSend = ChatSendBeforeEventSignal()
        self.__entityHurt = EntityHurtBeforeEventSignal()
        self.__explosion = ExplosionBeforeEventSignal()
        self.__playerInteractWithEntity = PlayerInteractWithEntityBeforeEventSignal()
        self.__playerBreakBlock = PlayerBreakBlockBeforeEventSignal()

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
    
    @property
    def explosion(self):
        """This event is fired before an explosion occurs."""
        return self.__explosion
    
    @property
    def playerInteractWithEntity(self):
        """This event fires when a player interacts with an entity."""
        return self.__playerInteractWithEntity
        
    @property
    def playerBreakBlock(self):
        """This event fires for a block that is broking by a player."""
        return self.__playerBreakBlock
