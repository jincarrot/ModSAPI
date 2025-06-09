# coding=utf-8

import types
from EventBases import *
from ..Interfaces.EntityOptions import *
import mod.server.extraServerApi as serverApi


class EntityDieAfterEventSignal(EntityEvents):
    """
    Supports registering for an event that fires after an entity has died.
    """

    @staticmethod
    def __detectFunction(obj, data):
        arg = {}
        if obj.options:
            if obj.options.entities:
                entityIds = []
                for entity in obj.options.entities:
                    entityIds.append(entity.id)
                if data['id'] not in entityIds:
                    arg['error'] = True
            if obj.options.entityTypes:
                if SComp.CreateEngineType(data['id']).GetEngineTypeStr() not in obj.options.entityTypes:
                    arg['error'] = True
        damagingEntity = data['attacker'] if data['attacker'] else None
        damagingProjectile = None
        if damagingEntity and SComp.CreateEntityComponent(damagingEntity).HasComponent(EntityComponentType.projectile):
            damagingProjectile = damagingEntity
            damagingEntity = SComp.CreateActorOwner(damagingProjectile).GetEntityOwner()
        temp = {
            "cause": data['cause']
        }
        if damagingEntity:
            temp['damagingEntity'] = Entity(damagingEntity)
        if damagingProjectile:
            temp['damagingProjectile'] = Entity(damagingProjectile)
        arg['damageSource'] = EntityDamageSource(temp)
        arg['deadEntity'] = Entity(data['id'])
        if arg['error']:
            return False
        return EntityDieAfterEvent(arg)


    def subscribe(self, callback, options=EntityEventsOptions):
        # type: (types.FunctionType, dict) -> None
        """
        Subscribes to an event that fires when an entity dies.
        """
        if type(options).__name__ != "dict":
            options = None
        eventName = "MobDieEvent"
        listener = EventListener(eventName, callback, options, self.__detectFunction)
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

    @staticmethod
    def __detectFunction(obj, data):
        arg = {'error': False}
        if obj.options:
            if obj.options.entities:
                entityIds = []
                for entity in obj.options.entities:
                    entityIds.append(entity.id)
                if data['entityId'] not in entityIds:
                    arg['error'] = True
            if obj.options.entityTypes:
                if SComp.CreateEngineType(data['entityId']).GetEngineTypeStr() not in obj.options.entityTypes:
                    arg['error'] = True
        damagingEntity = data['srcId'] if data['srcId'] else None
        damagingProjectile = data['projectileId']
        temp = {
            "cause": data['cause']
        }
        if damagingEntity:
            temp['damagingEntity'] = Entity(damagingEntity)
        if damagingProjectile:
            temp['damagingProjectile'] = Entity(damagingProjectile)
        arg['damageSource'] = EntityDamageSource(temp)
        arg['hurtEntity'] = Entity(data['entityId'])
        arg['damage'] = data['damage']
        if arg['error']:
            return False
        return EntityHurtAfterEvent(arg)

    def subscribe(self, callback, options=EntityEventsOptions):
        # type: (types.FunctionType, dict) -> None
        """
        Adds a callback that will be called when an effect is added to an entity.
        """
        if type(options).__name__ != "dict":
            options = None
        eventName = "DamageEvent"
        listener = EventListener(eventName, callback, options, self.__detectFunction)
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
