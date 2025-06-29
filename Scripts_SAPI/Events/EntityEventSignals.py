# coding=utf-8

import types
from EventBases import *
from ..Interfaces.EntityOptions import *
import mod.server.extraServerApi as serverApi
from ..minecraft import *


class EntityEvents(Events):

    def __init__(self):
        self.__eventName = None

    def _check(self, obj, data, valueName):
        # type: (EventListener, dict, str) -> bool
        options = obj.options
        if type(options) != dict:
            options = None
        else:
            options = EntityEventsOptions(options)
        if options:
            if options.entities:
                entityIds = []
                for entity in options.entities:
                    entityIds.append(entity.id)
                if data[valueName] not in entityIds:
                    return False
            if options.entityTypes:
                if SComp.CreateEngineType(data[valueName]).GetEngineTypeStr() not in options.entityTypes:
                    return False
        return True
                
    def subscribe(self, callback, options=None):
        # type: (types.FunctionType, dict) -> None
        EventListener(self.eventName, callback, options, self._check, None)


class EntityDieAfterEventSignal(EntityEvents):
    """
    Supports registering for an event that fires after an entity has died.
    """

    def __init__(self):
        EntityEvents.__init__(self)
        self.__eventName = "MobDieEvent"

    def subscribe(self, callback, options=None):
        # type: (types.FunctionType, dict) -> None
        import EntityEvents as ee
        EventListener(self.__eventName, callback, options, self._check, "id", ee.EntityDieAfterEvent)


class EffectAddAfterEventSignal(EntityEvents):
    """
    Manages callbacks that are connected to when an effect is added to an entity.
    """

    def subscribe(self, callback, options=EntityEventsOptions):
        # type: (types.FunctionType, dict) -> None
        """
        Adds a callback that will be called when an effect is added to an entity.
        """

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

        world.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "DamageEvent", world, callback)


class EntityHurtAfterEventSignal(EntityEvents):
    """
    Manages callbacks that are connected to when an effect is added to an entity.
    """

    def __init__(self):
        self.__eventName = "DamageEvent"

    def subscribe(self, callback, options=EntityEventsOptions):
        # type: (types.FunctionType, dict) -> None
        """
        Adds a callback that will be called when an effect is added to an entity.
        """
        import EntityEvents as ee
        EventListener(self.__eventName, callback, options, "entityId", self._check, ee.EntityHurtAfterEvent)


class EntityLoadAfterEventSignal(EntityEvents):
    """
    Manages callbacks that are connected to when an effect is added to an entity.
    """

    def subscribe(self, callback, options=EntityEventsOptions):
        # type: (types.FunctionType, dict) -> None
        """
        Adds a callback that will be called when an effect is added to an entity.
        """

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

        world.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "EntityRemoveEvent", world, callback)


class EntitySpawnAfterEventSignal(EntityEvents):
    """
    Registers a script-based event handler for handling what happens when an entity spawns.
    """

    def __init__(self):
        self.__eventName = "ServerSpawnMobEvent"

    def subscribe(self, callback, options=EntityEventsOptions):
        # type: (types.FunctionType, dict) -> None
        """
        Adds a callback that will be called when an effect is added to an entity.
        """
        import EntityEvents as ee
        EventListener(self.__eventName, callback, options, self._check, "entityId", ee.EntitySpawnAfterEvent)
