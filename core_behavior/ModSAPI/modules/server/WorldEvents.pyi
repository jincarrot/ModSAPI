# -*- coding: utf-8 -*-
# stub file for world events container classes

from ...events.signals.EntityEventSignals import *
from ...events.signals.PlayerEventSignals import *
from ...events.signals.ProjectileEventSignals import *
from ...events.signals.BlockEventSignals import BlockExplodeAfterEventSignal
from ...events.signals.WorldEventSignals import *

import mod.server.extraServerApi as serverApi
import mod.client.extraClientApi as clientApi

class WorldAfterEvents:
    """
    Contains a set of events that are available across the scope of the World.
    """

    @property
    def dataDrivenEntityTrigger(self) -> DataDrivenEntityTriggerEventSignal:
        """
        This event is fired when an entity event has been triggered that will update the component definition state of an entity.
        """
        ...

    @property
    def entityDie(self) -> EntityDieAfterEventSignal:
        """
        Supports registering for an event that fires after an entity has died.
        """
        ...

    @property
    def effectAdd(self) -> EffectAddAfterEventSignal:
        """
        This event fires when an effect, like poisoning, is added to an entity.
        """
        ...

    @property
    def entityHealthChanged(self) -> EntityHealthChangedAfterEventSignal:
        """
        This event fires when entity health changes in any degree.
        """
        ...

    @property
    def _entityHitBlock(self) -> int:
        """
        This event fires when entity health changes in any degree.
        """
        ...

    @property
    def entityHurt(self) -> EntityHurtAfterEventSignal:
        """
        This event fires when an entity is hurt (takes damage).
        """
        ...

    @property
    def entityHitEntity(self) -> EntityHitEntityAfterEventSignal:
        """
        This event fires when an entity hits (that is, melee attacks) another entity.
        """
        ...

    @property
    def entitySpawn(self) -> EntitySpawnAfterEventSignal:
        """
        This event fires when an entity is spawned.
        """
        ...

    @property
    def entityLoad(self) -> EntityLoadAfterEventSignal:
        """
        Fires when an entity is loaded.
        """
        ...

    @property
    def entityRemove(self) -> EntityRemoveAfterEventSignal:
        """Fires when an entity is removed (for example, potentially unloaded, or removed after being killed)."""
        ...

    @property
    def chatSend(self) -> ChatSendAfterEventSignal:
        """
        This event is triggered after a chat message has been broadcast or sent to players.
        """
        ...

    @property
    def itemUse(self) -> ItemUseAfterEventSignal:
        """
        This event fires when an item is successfully used by a player.
        """
        ...

    @property
    def itemCompleteUse(self) -> ItemCompleteUseAfterEventSignal:
        """
        This event fires when a chargeable item completes charging
        """
        ...

    @property
    def projectileHitBlock(self) -> ProjectileHitBlockAfterEventSignal:
        """This event fires when a projectile hits a block."""
        ...

    @property
    def projectileHitEntity(self) -> ProjectileHitEntityAfterEventSignal:
        """This event fires when a projectile hits an entity."""
        ...

    @property
    def itemStartUseOn(self) -> ItemStartUseOnAfterEventSignal:
        """This event fires when a chargeable item starts charging."""
        ...

    @property
    def blockExplode(self) -> BlockExplodeAfterEventSignal:
        """This event fires for each BlockLocation destroyed by an explosion.
        It is fired after the blocks have already been destroyed."""
        ...

    @property
    def explosion(self) -> ExplosionAfterEventSignal:
        """This event is fired after an explosion occurs."""
        ...

    @property
    def playerDimensionChange(self) -> PlayerDimensionChangeAfterEventSignal:
        """Fires when a player moved to a different dimension."""
        ...

    @property
    def playerJoin(self) -> PlayerJoinAfterEventSignal:
        """
        This event fires when a player joins a world.

        See also playerSpawn for another related event you can trap for when a player is spawned the first time within a world.
        """
        ...

    @property
    def playerLeave(self) -> PlayerLeaveAfterEventSignal:
        """This event fires when a player leaves a world."""
        ...

    @property
    def playerSpawn(self) -> PlayerSpawnAfterEventSignal:
        """
        This event fires when a player spawns or respawns.

        Note that an additional flag within this event will tell you whether the player is spawning right after join vs. a respawn.
        """
        ...

    @property
    def playerInventoryItemChange(self) -> PlayerInventoryItemChangeAfterEventSignal:
        """This event fires when an item gets added or removed to the player's inventory."""
        ...

    @property
    def playerBreakBlock(self) -> PlayerBreakBlockAfterEventSignal:
        """This event fires for a block that is broken by a player."""
        ...

    @property
    def playerPlaceBlock(self) -> PlayerPlaceBlockAfterEventSignal:
        """This event fires for a block that is placed by a player."""
        ...


class WorldBeforeEvents:
    """
    A set of events that fire before an actual action occurs.
    In most cases, you can potentially cancel or modify the impending event.

    Note that in before events any APIs that modify gameplay state will not function and will throw an error. (e.g., dimension.spawnEntity)
    """
    def __init__(self) -> None: ...

    @property
    def chatSend(self) -> ChatSendBeforeEventSignal:
        """
        This event is triggered after a chat message has been broadcast or sent to players.
        """
        ...

    @property
    def entityHurt(self) -> EntityHurtBeforeEventSignal:
        """
        This event fires when an entity is hurt (takes damage).
        """
        ...

    @property
    def explosion(self) -> ExplosionBeforeEventSignal:
        """This event is fired before an explosion occurs."""
        ...

    @property
    def playerInteractWithEntity(self) -> PlayerInteractWithEntityBeforeEventSignal:
        """This event fires when a player interacts with an entity."""
        ...

    @property
    def playerBreakBlock(self) -> PlayerBreakBlockBeforeEventSignal:
        """This event fires for a block that is breaking by a player."""
        ...