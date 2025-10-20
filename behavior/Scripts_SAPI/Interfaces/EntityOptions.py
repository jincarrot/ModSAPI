# -*- coding: utf-8 -*-
# from typing import List, Dict, Union
from Vector import *
from ..Enumerations import *
# from ..Classes.Entity import *
import math
import mod.server.extraServerApi as serverApi

comp = serverApi.GetEngineCompFactory()


class EntityFilter(object):
    """
    Contains options for filtering entities.
    """

    def __init__(self, data):
        self.excludeFamilies = data['excludeFamilies'] if 'excludeFamilies' in data else []
        """If this value is set, this event will only fire for entities that do not match the entity families within this collection."""
        self.excludeTypes = data['excludeTypes'] if 'excludeTypes' in data else []
        """If this value is set, this event will only fire if the impacted entities' type matches this parameter."""
        self.excludeGameModes = data['excludeGameModes'] if 'excludeGameModes' in data else []
        """If this value is set, this event will only fire if the impacted entities' game mode matches this parameter."""
        self.excludeNames = data['excludeNames'] if 'excludeNames' in data else []
        """If this value is set, this event will only fire if the impacted entities' name matches this parameter."""
        self.excludeTags = data['excludeTags'] if 'excludeTags' in data else []
        """If this value is set, this event will only fire if the impacted entities' tags match this parameter."""
        self.families = data['families'] if 'families' in data else []
        """If this value is set, this event will only fire if the impacted entities' family matches this parameter."""
        self.gameMode = data['gameMode'] if 'gameMode' in data else None
        """If this value is set, this event will only fire if the impacted entities' game mode matches this parameter."""
        self.maxHorizontalRotation = data['maxHorizontalRotation'] if 'maxHorizontalRotation' in data else None
        """If this value is set, this event will only fire if the impacted entities' max horizontal rotation matches this parameter."""
        self.maxLevel = data['maxLevel'] if 'maxLevel' in data else None
        """If this value is set, this event will only fire if the impacted entities' level matches this parameter."""
        self.maxVerticalRotation = data['maxVerticalRotation'] if 'maxVerticalRotation' in data else None
        """If this value is set, this event will only fire if the impacted entities' max vertical rotation matches this parameter."""
        self.minLevel = data['minLevel'] if 'minLevel' in data else None
        """If this value is set, this event will only fire if the impacted entities' level matches this parameter."""
        self.minHorizontalRotation = data['minHorizontalRotation'] if 'minHorizontalRotation' in data else None
        """If this value is set, this event will only fire if the impacted entities' min horizontal rotation matches this parameter."""
        self.minVerticalRotation = data['minVerticalRotation'] if 'minVerticalRotation' in data else None
        """If this value is set, this event will only fire if the impacted entities' min vertical rotation matches this parameter."""
        self.name = data['name'] if 'name' in data else ""
        """If this value is set, this event will only fire if the impacted"""
        self.propertyOptions = data['propertyOptions'] if 'propertyOptions' in data else None
        """If this value is set, this event will only fire if the impacted entities' property options match this parameter."""
        self.scoreOptions = data['scoreOptions'] if 'scoreOptions' in data else None
        """If this value is set, this event will only fire if the impacted entities' score options match this parameter."""
        self.tags = data['tags'] if 'tags' in data else []
        """If this value is set, this event will only fire if the impacted entities' tags match this parameter."""
        self.type = data['type'] if 'type' in data else ""


class EntityEventOptions(object):
    """
    Contains optional parameters for registering an entity event.
    """

    def __init__(self, data):
        self.__entities = data['entities'] if 'entities' in data else []
        """If this value is set, this event will only fire for entities that match the entities within this collection."""
        self.__entityTypes = data['entityTypes'] if 'entityTypes' in data else []
        """If this value is set, this event will only fire if the impacted entities' type matches this parameter."""

    @property
    def entities(self):
        # type: () -> list[Entity]
        """If this value is set, this event will only fire for entities that match the entities within this collection."""
        return self.__entities

    @entities.setter
    def entities(self, data):
        # type: (list[Entity]) -> None
        self.__entities = data

    @property
    def entityTypes(self):
        # type: () -> list[str]
        """If this value is set, this event will only fire if the impacted entities' type matches this parameter."""
        return self.__entityTypes

    @entityTypes.setter
    def entityTypes(self, data):
        # type: (list[str]) -> None
        self.__entityTypes = data


class EntityQueryOptions(object):
    """
    Contains options for selecting entities within an area.
    """

    def __init__(self, data):
        # type: (dict) -> None
        self.data = data
        self.closest = data['closest'] if 'closest' in data else -1
        # type: int
        """
        Limits the number of entities to return, opting for the closest N entities as specified by this property.
        The location value must also be specified on the query options object.
        """
        self.farthest = data['farthest'] if 'farthest' in data else -1
        # type: int
        """
        Limits the number of entities to return, opting for the farthest N entities as specified by this property. 
        The location value must also be specified on the query options object.
        """
        self.location = Vector3(data['location']) if 'location' in data else Vector3({})
        # type: Vector3
        """
        Adds a seed location to the query that is used in conjunction with closest, farthest, limit, volume, and distance properties.
        """
        self.maxDistance = data['maxDistance'] if 'maxDistance' in data else -1
        # type: int
        """
        If specified, includes entities that are less than this distance away from the location specified in the location property.
        """
        self.minDistance = data['minDistance'] if 'minDistance' in data else -1
        # type: int
        """
        If specified, includes entities that are least this distance away from the location specified in the location property.
        """
        self.volume = Vector3(data['volume']) if 'volume' in data else None
        # type: Vector3
        """
        In conjunction with location, specified a cuboid volume of entities to include.
        """

    def selfCheck(self):
        # type: () -> bool
        """检查数据是否合法"""
        if type(self.data) == dict and set(self.data.keys()).issubset(set(EntityQueryOptionsProperties)):
            if self.farthest >= 0 and self.closest >= 0:
                return False
            for key in self.data:
                if key in ["closest", "farthest", "maxDistance", "minDistance"] and not (
                        type(self.data[key]) == int and self.data[key] >= 0):
                    return False
            return True
        print("Invalid value! Check your data: \n%s" % self.data)
        return False

    def checkLocation(self, entityIds):
        # type: (list[str]) -> list[str]
        """检查实体是否在指定范围内"""
        if self.minDistance < 0 and self.maxDistance < 0:
            return entityIds
        checkOuts = []
        for entityId in entityIds:
            location = comp.CreatePos(entityId).GetPos()
            if self.minDistance <= math.sqrt(
                    math.pow(location[0] - self.location.x, 2) + math.pow(location[1] - self.location.y, 2) + math.pow(
                            location[2] - self.location.z, 2)) <= self.maxDistance:
                checkOuts.append(entityId)
        return checkOuts

    def checkDistance(self, entityIds):
        # type: (list[str]) -> list[str]
        """检查实体距离"""
        if self.closest < 0 and self.farthest < 0:
            return entityIds
        checkOuts = []
        num = self.closest if self.closest >= 0 else self.farthest
        op = max if num == self.farthest else min
        distances = []
        for entityId in entityIds:
            location = comp.CreatePos(entityId).GetPos()
            distances.append(math.sqrt(
                math.pow(location[0] - self.location.x, 2) + math.pow(location[1] - self.location.y, 2) + math.pow(
                    location[2] - self.location.z, 2)))
        for i in range(0, num):
            checkOuts.append(entityIds[distances.index(op(distances))])
        return checkOuts

    def checkVolume(self, entityIds):
        # type: (list[str]) -> list[str]
        """
        检查实体位置是否在范围内
        """
        checkOuts = []
        if not self.volume:
            return entityIds
        x = (self.location.x, self.location.x + self.volume.x)
        y = (self.location.y, self.location.y + self.volume.y)
        z = (self.location.z, self.location.z + self.volume.z)
        for entityId in entityIds:
            location = comp.CreatePos(entityId).GetPos()
            if min(x) <= location[0] <= max(x) and min(y) <= location[1] <= max(y) and min(z) <= location[2] <= max(z):
                checkOuts.append(entityId)
        return checkOuts

    def check(self, entityIds):
        entityIds = self.checkVolume(entityIds)
        entityIds = self.checkLocation(entityIds)
        entityIds = self.checkDistance(entityIds)
        return entityIds


class EntityEffectOptions(object):
    """
    Contains additional options for entity effects.
    """

    def __init__(self, data):
        self.__data = data
        if type(self.__data).__name__ != 'dict':
            self.__data = {}
        self.amplifier = self.__data['amplifier'] if 'amplifier' in self.__data else 0
        self.showParticle = self.__data['showParticle'] if 'showParticle' in self.__data else True


class EntityApplyDamageByProjectileOptions(object):
    """
    Additional options for when damage has been applied via a projectile.
    """

    def __init__(self, data):
        # type: (Dict[str, Entity]) -> None
        self.damagingProjectile = data['damagingProjectile']
        self.damagingEntity = data['damagingEntity'] if 'damagingEntity' in data else None
        """Optional entity that caused the damage."""


class EntityApplyDamageOptions(object):
    """
    Additional descriptions and metadata for a damage event.
    """
    def __init__(self, data):
        # type: (Dict[str, Union[str, Entity]]) -> None
        self.cause = data['cause'] if 'cause' in data else 'none'
        """Underlying cause of the damage."""
        self.cause = getattr(EntityDamageCause, self.cause)
        self.damagingEntity = data['damagingEntity'] if 'damagingEntity' in data else None
        """Optional entity that caused the damage."""


class EntityRaycastOptions(EntityFilter):
    """
    Returns the first intersecting block from the direction that this entity is looking at.
    """

    def __init__(self, data):
        EntityFilter.__init__(self, data)
        self.ignoreBlockCollision =  data['ignoreBlockCollision'] if 'ignoreBlockCollision' in data else False
        """Whether to ignore block collision."""
        self.includeLiquidBlocks = data['includeLiquidBlocks'] if 'includeLiquidBlocks' in data else False
        """Whether to include liquid blocks in the raycast."""
        self.includePassableBlocks = data['includePassableBlocks'] if 'includePassableBlocks' in data else False
        """Whether to include passable blocks in the raycast."""
        self.maxDistance = data['maxDistance'] if 'maxDistance' in data else 16


class SpawnEntityOptions(object):
    """
    Contains additional options for spawning an Entity.
    """

    def __init__(self, data):
        self.initialPersistence = data['initialPersistence'] if 'initialPersistence' in data else False# type: bool
        """Optional boolean which determines if this entity should persist in the game world. Persistence prevents the entity from automatically despawning."""
        self.initialRotation = data['initialRotation'] if 'initialRotation' in data else 0 # type: int
        """Optional initial rotation, in degrees, to set on the entity when it spawns."""
        self.spawnEvent = data['spawnEvent'] if 'spawnEvent' in data else None # type： str
        """Optional spawn event to send to the entity after it is spawned."""


class PlayerSoundOptions(object):
    """
    Additional options for how a sound plays for a player.
    """

    def __init__(self, data):
        self.location = data['location'] if 'location' in data else None # type: Vector3
        """Location of the sound; if not specified, the sound is played near a player."""
        if type(self.location) == dict:
            self.location = Vector3(self.location)
        self.pitch = data['pitch'] if 'pitch' in data else 1.0
        """Optional pitch of the sound."""
        self.volume = data['volume'] if 'volume' in data else 1.0
        """Optional volume of the sound."""
