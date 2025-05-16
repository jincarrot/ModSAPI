# coding=utf-8

import types
from EventBases import *
from ..Interfaces.EntityOptions import *
import mod.server.extraServerApi as serverApi


class EntityDieAfterEventSignal(EntityEvents):
    """
    Supports registering for an event that fires after an entity has died.
    """

    def subscribe(self, callback, options=EntityEventsOptions):
        # type: (types.FunctionType, dict) -> None
        """
        Subscribes to an event that fires when an entity dies.
        """
        if type(options).__name__ != "dict":
            options = None
        eventName = "MobDieEvent"
        listener = EventListener(eventName, callback, options)
        world = serverApi.GetSystem("SAPI", "world")
        world.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), eventName, listener, listener.listen)


class EffectAddAfterEventSignal(EntityEvents):
    """
    Manages callbacks that are connected to when an effect is added to an entity.
    """

    def subscribe(self, callback, options=EntityEventsOptions):
        # type: (types.FunctionType, dict) -> None
        """
        Adds a callback that will be called when an effect is added to an entity.
        """
        world = serverApi.GetSystem("SAPI", "world")
        world.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "AddEffectServerEvent", world, callback)


class EntityHealthChangedAfterEventSignal(EntityEvents):
    """
    Manages callbacks that are connected to when an effect is added to an entity.
    """

    def subscribe(self, callback, options=EntityEventsOptions):
        # type: (types.FunctionType, dict) -> None
        """
        Adds a callback that will be called when an effect is added to an entity.
        """
        world = serverApi.GetSystem("SAPI", "world")
        world.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "HealthChangeServerEvent", world, callback)


class EntityHitBlockAfterEventSignal(EntityEvents):
    """
    Manages callbacks that are connected to when an effect is added to an entity.
    """

    def subscribe(self, callback, options=EntityEventsOptions):
        # type: (types.FunctionType, dict) -> None
        """
        Adds a callback that will be called when an effect is added to an entity.
        """
        world = serverApi.GetSystem("SAPI", "world")
        world.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "OnMobHitBlockServerEvent", world, callback)


class EntityHitEntityAfterEventSignal(EntityEvents):
    """
    Manages callbacks that are connected to when an effect is added to an entity.
    """

    def subscribe(self, callback, options=EntityEventsOptions):
        # type: (types.FunctionType, dict) -> None
        """
        Adds a callback that will be called when an effect is added to an entity.
        """
        world = serverApi.GetSystem("SAPI", "world")
        world.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "DamageEvent", world, callback)


class EntityHurtAfterEventSignal(EntityEvents):
    """
    Manages callbacks that are connected to when an effect is added to an entity.
    """

    def subscribe(self, callback, options=EntityEventsOptions):
        # type: (types.FunctionType, dict) -> None
        """
        Adds a callback that will be called when an effect is added to an entity.
        """
        if type(options).__name__ != "dict":
            options = None
        eventName = "DamageEvent"
        listener = EventListener(eventName, callback, options)
        world = serverApi.GetSystem("SAPI", "world")
        world.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), eventName, listener,
                             listener.listen)


class EntityLoadAfterEventSignal(EntityEvents):
    """
    Manages callbacks that are connected to when an effect is added to an entity.
    """

    def subscribe(self, callback, options=EntityEventsOptions):
        # type: (types.FunctionType, dict) -> None
        """
        Adds a callback that will be called when an effect is added to an entity.
        """
        world = serverApi.GetSystem("SAPI", "world")
        world.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "AddEntityServerEvent", world, callback)


class EntityRemoveAfterEventSignal(EntityEvents):
    """
    Manages callbacks that are connected to when an effect is added to an entity.
    """

    def subscribe(self, callback, options=EntityEventsOptions):
        # type: (types.FunctionType, dict) -> None
        """
        Adds a callback that will be called when an effect is added to an entity.
        """
        world = serverApi.GetSystem("SAPI", "world")
        world.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "EntityRemoveEvent", world, callback)


class EntitySpawnAfterEventSignal(EntityEvents):
    """
    Manages callbacks that are connected to when an effect is added to an entity.
    """

    def subscribe(self, callback, options=EntityEventsOptions):
        # type: (types.FunctionType, dict) -> None
        """
        Adds a callback that will be called when an effect is added to an entity.
        """
        world = serverApi.GetSystem("SAPI", "world")
        world.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "EntityRemoveEvent", world, callback)
