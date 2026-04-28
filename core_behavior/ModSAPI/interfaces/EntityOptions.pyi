# -*- coding: utf-8 -*-
from typing import TypedDict
from Vector import *
from ..enums.Game import *
from ..modules.server.Entity import Entity
import mod.server.extraServerApi as serverApi
from ..enums.Entity import *

comp = serverApi.GetEngineCompFactory()

class EqualsComparison(TypedDict):
    """Represents an equals comparison for filtering entities."""

    equals: bool | str | int
    """The value to compare against."""

class GreaterThanComparison(TypedDict):
    """Represents a greater than comparison for filtering entities."""

    greaterThan: int
    """The value to compare against."""

class LessThanComparison(TypedDict):
    """Represents a less than comparison for filtering entities."""

    lessThan: int
    """The value to compare against."""

class GreaterThanOrEqualsComparison(TypedDict):
    """Represents a greater than or equals comparison for filtering entities."""

    greaterThanOrEquals: int
    """The value to compare against."""

class LessThanOrEqualsComparison(TypedDict):
    """Represents a less than or equals comparison for filtering entities."""

    lessThanOrEquals: int
    """The value to compare against."""

class NotEqualsComparison(TypedDict):
    """Represents a not equals comparison for filtering entities."""

    notEquals: bool | str | int
    """The value to compare against."""

class RangeComparison(TypedDict):

    lowerBound: int
    """The lower bound of the range."""
    upperBound: int
    """The upper bound of the range."""

class EntityQueryScoreOptions(TypedDict):
    """Contains additional options for filtering players based on their score for an objective."""

    exclude: bool
    """If set to true, entities and players within this score range are excluded from query results."""
    objective: str
    """Identifier of the scoreboard objective to filter on."""
    minScore: int
    """If defined, only players that have a score equal to or over minScore are included."""
    maxScore: int
    """If defined, only players that have a score equal to or under maxScore are included."""

class EntityQueryPropertyOptions:
    """"""
    
    exlude: bool
    propertyId: str
    value: bool | str | EqualsComparison | GreaterThanComparison | LessThanComparison | GreaterThanOrEqualsComparison | LessThanOrEqualsComparison | NotEqualsComparison | RangeComparison

class EntityFilter(TypedDict):
    """
    Contains options for filtering entities.
    """

    excludeFamilies: list[str]
    """If this value is set, this event will only fire for entities that do not match the entity families within this collection."""
    excludeTypes: list[str]
    """If this value is set, this event will only fire if the impacted entities' type matches this parameter."""
    excludeGameModes: list[GameMode]
    """If this value is set, this event will only fire if the impacted entities' game mode matches this parameter."""
    excludeNames: list[str]
    """If this value is set, this event will only fire if the impacted entities' name matches this parameter."""
    excludeTags: list[str]
    """If this value is set, this event will only fire if the impacted entities' tags match this parameter."""
    families: list[str]
    """If this value is set, this event will only fire if the impacted entities' family matches this parameter."""
    gameMode: GameMode
    """If this value is set, this event will only fire if the impacted entities' game mode matches this parameter."""
    maxHorizontalRotation: float
    """If this value is set, this event will only fire if the impacted entities' max horizontal rotation matches this parameter."""
    maxLevel: int
    """If this value is set, this event will only fire if the impacted entities' level matches this parameter."""
    maxVerticalRotation: float
    """If this value is set, this event will only fire if the impacted entities' max vertical rotation matches this parameter."""
    minLevel: int
    """If this value is set, this event will only fire if the impacted entities' level matches this parameter."""
    minHorizontalRotation: float
    """If this value is set, this event will only fire if the impacted entities' min horizontal rotation matches this parameter."""
    minVerticalRotation: float
    """If this value is set, this event will only fire if the impacted entities' min vertical rotation matches this parameter."""
    name: str
    """If this value is set, this event will only fire if the impacted"""
    propertyOptions: dict
    """If this value is set, this event will only fire if the impacted entities' property options match this parameter."""
    scoreOptions: dict
    """If this value is set, this event will only fire if the impacted entities' score options match this parameter."""
    tags: list[str]
    """If this value is set, this event will only fire if the impacted entities' tags match this parameter."""
    type: str
    """If this value is set, this event will only fire if the impacted entities' type matches this parameter."""


class EntityEventOptions(TypedDict):
    """
    Contains optional parameters for registering an entity event.
    """

    @property
    def entities(self):
        # type: () -> list[Entity]
        """If this value is set, this event will only fire for entities that match the entities within this collection."""

    @entities.setter
    def entities(self, data):
        # type: (list[Entity]) -> None
        pass

    @property
    def entityTypes(self):
        # type: () -> list[str]
        """If this value is set, this event will only fire if the impacted entities' type matches this parameter."""

    @entityTypes.setter
    def entityTypes(self, data):
        # type: (list[str]) -> None
        pass


class EntityQueryOptions(EntityFilter):
    """
    Contains options for selecting entities within an area.
    """

    closest: int
    """
    Limits the number of entities to return, opting for the closest N entities as specified by this property.
    The location value must also be specified on the query options object.
    """
    farthest: int
    """
    Limits the number of entities to return, opting for the farthest N entities as specified by this property. 
    The location value must also be specified on the query options object.
    """
    location: Vector3
    """
    Adds a seed location to the query that is used in conjunction with closest, farthest, limit, volume, and distance properties.
    """
    maxDistance: int
    """
    If specified, includes entities that are less than this distance away from the location specified in the location property.
    """
    minDistance: int
    """
    If specified, includes entities that are least this distance away from the location specified in the location property.
    """
    volume: Vector3
    """
    In conjunction with location, specified a cuboid volume of entities to include.
    """


class EntityEffectOptions(TypedDict):
    """
    Contains additional options for entity effects.
    """

    amplifier: int
    """The strength of the effect."""
    showParticle: bool
    """Whether to show particles for the effect."""


class EntityApplyDamageByProjectileOptions(TypedDict):
    """
    Additional options for when damage has been applied via a projectile.
    """
    
    damagingProjectile: Entity | None
    """The projectile that caused the damage."""
    damagingEntity: Entity | None
    """Optional entity that caused the damage."""


class EntityApplyDamageOptions(object):
    """
    Additional descriptions and metadata for a damage event.
    """
    cause: EntityDamageCause
    """Underlying cause of the damage."""
    damagingEntity: Entity | None
    """Optional entity that caused the damage."""


class EntityRaycastOptions(EntityFilter):
    """
    Returns the first intersecting block from the direction that this entity is looking at.
    """

    ignoreBlockCollision: bool
    """Whether to ignore block collision."""
    includeLiquidBlocks: bool
    """Whether to include liquid blocks in the raycast."""
    includePassableBlocks: bool
    """Whether to include passable blocks in the raycast."""
    maxDistance: float


class SpawnEntityOptions(object):
    """
    Contains additional options for spawning an Entity.
    """

    initialPersistence: bool
    """Optional boolean which determines if this entity should persist in the game world. Persistence prevents the entity from automatically despawning."""
    initialRotation: int
    """Optional initial rotation, in degrees, to set on the entity when it spawns."""
    spawnEvent: str
    """Optional spawn event to send to the entity after it is spawned."""


class PlayerSoundOptions(object):
    """
    Additional options for how a sound plays for a player.
    """

    location: Vector3
    """Location of the sound; if not specified, the sound is played near a player."""
    pitch: float
    """Optional pitch of the sound."""
    volume: float
    """Optional volume of the sound."""


class MusicOptions(object):
    """
    Additional options for how a sound plays for a player.
    """

    loop: bool
    """If set to true, this music track will play repeatedly."""
    fade: float
    """Specifies a fade overlap for music at the end of play."""
    volume: float
    """Relative volume level of the music."""
