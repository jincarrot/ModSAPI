# coding=utf-8

import types
from EventBases import *
from ..Interfaces.EntityOptions import *
import mod.server.extraServerApi as serverApi
from ..minecraft import *
from ..decorators import *


class EntityEvents(Events):

    def __init__(self):
        Events.__init__(self)
        self.__eventName = None

    def _check(self, obj, data, valueName):
        # type: (EventListener, dict, str) -> bool
        options = obj.options
        if type(options) == dict:
            options = EntityEventOptions(options)
        elif type(options) == EntityEventOptions:
            options = options
        else:
            options = None
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
        self._events[id(callback)] = EventListener(self.eventName, callback, options, self._check, None)

    def unsubscribe(self, callback):
        # type: (types.FunctionType) -> None
        Events.unsubscribe(self, callback)


class EntityDieAfterEventSignal(EntityEvents):
    """
    Supports registering for an event that fires after an entity has died.
    """

    def __init__(self):
        EntityEvents.__init__(self)
        self.__eventName = "MobDieEvent"

    def subscribe(self, callback, options=None):
        # type: (types.FunctionType, dict) -> None
        """Subscribes to an event that fires when an entity dies."""
        import EntityEvents as ee
        self._events[id(callback)] = EventListener(self.__eventName, callback, options, self._check, "id", ee.EntityDieAfterEvent)

    def unsubscribe(self, callback):
        # type: (types.FunctionType) -> None
        Events.unsubscribe(self, callback)


class EffectAddAfterEventSignal(EntityEvents):
    """
    Manages callbacks that are connected to when an effect is added to an entity.
    """

    def __init__(self):
        EntityEvents.__init__(self)
        self.__eventName = "AddEffectServerEvent"

    def subscribe(self, callback, options=None):
        # type: (types.FunctionType, dict) -> None
        """Adds a callback that will be called when an effect is added to an entity."""
        import EntityEvents as ee
        self._events[id(callback)] = EventListener(self.__eventName, callback, options, self._check, "entityId", ee.EffectAddAfterEvent)


class EntityHealthChangedAfterEventSignal(EntityEvents):
    """
    Manages callbacks that are connected to when the health of an entity changes.
    """

    def __init__(self):
        EntityEvents.__init__(self)
        self.__eventName = "HealthChangeServerEvent"

    def subscribe(self, callback, options=None):
        # type: (types.FunctionType, dict) -> None
        """Adds a callback that will be called when the health of an entity changes."""
        import EntityEvents as ee
        self._events[id(callback)] =  EventListener(self.__eventName, callback, options, self._check, "entityId", ee.EntityHealthChangedAfterEvent)


class __EntityHitBlockAfterEventSignal(EntityEvents):
    """
    Manages callbacks that are connected to when an effect is added to an entity.
    """

    def subscribe(self, callback, options=EntityEventOptions):
        # type: (types.FunctionType, dict) -> None
        """
        Adds a callback that will be called when an effect is added to an entity.
        """

        world.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "OnMobHitBlockServerEvent", world, callback)


class EntityHitEntityAfterEventSignal(EntityEvents):
    """
    Manages callbacks that are connected to when an entity makes a melee attack on another entity.
    """

    def __init__(self):
        EntityEvents.__init__(self)
        self.__eventName = "DamageEvent"

    def _check(self, obj, data, valueName):
        # type: (EventListener, dict, str) -> bool
        options = obj.options
        if SComp.CreateEngineType(data['srcId']).GetEngineTypeStr() == 'minecraft:player':
            return False
        if data['cause'] != "entity_attack":
            return False
        if type(options) != dict:
            options = None
        else:
            options = EntityEventOptions(options)
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

    def _checkPlayer(self, obj, data, valueName):
        # type: (EventListener, dict, str) -> bool
        options = obj.options
        print(data)
        if SComp.CreateEngineType(data['playerId']).GetEngineTypeStr() != 'minecraft:player':
            return False
        if type(options) != dict:
            options = None
        else:
            options = EntityEventOptions(options)
        if options:
            if options.entities:
                entityIds = []
                for entity in options.entities:
                    entityIds.append(entity.id)
                if data['playerId'] not in entityIds:
                    return False
            if options.entityTypes:
                if 'minecraft:player' not in options.entityTypes:
                    return False
        return True

    def subscribe(self, callback, options=EntityEventOptions):
        # type: (types.FunctionType, dict) -> None
        """
        Adds a callback that will be called when an entity hits another entity.
        """
        import EntityEvents as ee
        self._events[id(callback)] = EventListener(self.__eventName, callback, options, self._check, "entityId", ee.EntityHitEntityAfterEvent)
        # 实体与玩家分开
        EventListener("PlayerAttackEntityEvent", callback, options, self._checkPlayer, "entityId", ee.EntityHitEntityAfterEvent)


class EntityHurtAfterEventSignal(EntityEvents):
    """
    Manages callbacks that are connected to when an effect is added to an entity.
    """

    def __init__(self):
        EntityEvents.__init__(self)
        self.__eventName = "ActuallyHurtServerEvent"

    def subscribe(self, callback, options=EntityEventOptions):
        # type: (types.FunctionType, dict) -> None
        """
        Adds a callback that will be called when an effect is added to an entity.
        """
        import EntityEvents as ee
        self._events[id(callback)] = EventListener(self.__eventName, callback, options, self._check, "entityId", ee.EntityHurtAfterEvent)


class EntityLoadAfterEventSignal(EntityEvents):
    """
    Registers a script-based event handler for handling what happens when an entity loads.
    """

    def __init__(self):
        EntityEvents.__init__(self)
        self.__eventName = "AddEntityServerEvent"

    def subscribe(self, callback, options=EntityEventOptions):
        # type: (types.FunctionType, dict) -> None
        """
        Adds a callback that will be called when an effect is added to an entity.
        """
        import EntityEvents as ee
        self._events[id(callback)] = EventListener(self.__eventName, callback, options, self._check, "id", ee.EntityLoadAfterEvent)


class EntityRemoveAfterEventSignal(EntityEvents):
    """
    Allows registration for an event that fires when an entity is being removed from the game 
    
    (for example, unloaded, or a few seconds after they are dead.)
    """

    def __init__(self):
        EntityEvents.__init__(self)
        self.__eventName = "EntityRemoveEvent"

    def subscribe(self, callback, options=EntityEventOptions):
        # type: (types.FunctionType, dict) -> None
        """
        Will call your function every time an entity is being removed from the game.
        """

        import EntityEvents as ee
        self._events[id(callback)] = EventListener(self.__eventName, callback, options, self._check, "id", ee.EntityRemoveAfterEvent)


class EntitySpawnAfterEventSignal(EntityEvents):
    """
    Registers a script-based event handler for handling what happens when an entity spawns.
    """

    def __init__(self):
        EntityEvents.__init__(self)
        self.__eventName = "AddEntityServerEvent"

    def subscribe(self, callback, options=EntityEventOptions):
        # type: (types.FunctionType, dict) -> None
        """
        Adds a callback that will be called when an effect is added to an entity.
        """
        import EntityEvents as ee
        self._events[id(callback)] = EventListener(self.__eventName, callback, options, self._check, "id", ee.EntitySpawnAfterEvent)


class DataDrivenEntityTriggerEventSignal(EntityEvents):
    """
    Contains event registration related to firing of a data driven entity event - 
    for example, the minecraft:ageable_grow_up event on a chicken.
    """

    def __init__(self):
        EntityEvents.__init__(self)
        self.__eventName = "EntityDefinitionsEventServerEvent"

    def subscribe(self, callback, options=EntityEventOptions):
        # type: (types.FunctionType, dict) -> None
        """
        Adds a callback that will be called after a data driven entity event is triggered.
        """
        import EntityEvents as ee
        self._events[id(callback)] = EventListener(self.__eventName, callback, options, self._check, "entityId", ee.DataDrivenEntityTriggerAfterEvent)



class EntityHurtBeforeEventSignal(EntityEvents):
    """
    Manages callbacks that are connected to when an entity hurt.
    """

    def __init__(self):
        EntityEvents.__init__(self)
        self.__eventName = "DamageEvent"

    def subscribe(self, callback, options=EntityEventOptions):
        # type: (types.FunctionType, dict) -> None
        """
        Adds a callback that will be called when an effect is added to an entity.
        """
        import EntityEvents as ee
        self._events[id(callback)] = EventListener(self.__eventName, callback, options, self._check, "entityId", ee.EntityHurtBeforeEvent)
