# -*- coding: utf-8 -*-
# from typing import Union, Dict
from Components import *
import mod.server.extraServerApi as serverApi
from mod.common.minecraftEnum import EntityComponentType
from ..Entity import Entity
from typing import Literal, TypeVar
from ..Container import Container
from ..ItemStack import *
from ....enums.Entity import EquipmentSlot


class EntityAddRiderComponent(EntityComponent):
    """
    When added, this component makes the entity spawn with a rider of the specified entityType.
    """
    componentId = "minecraft:addrider"
    
    @property
    def entityType(self):
        # type: () -> str
        """
        The type of entity that is added as a rider for this entity when spawned under certain conditions.
        """
    
    @property
    def spawnEvent(self):
        # type: () -> str
        """
        Optional spawn event to trigger on the rider when that rider is spawned for this entity.
        """


class EntityAttributeComponent(EntityComponent):
    """
    This is a base abstract class for any entity component that centers around a number and can have a minimum, maximum, and default defined value.
    """
    @property
    def currentValue(self):
        # type: () -> float
        """
        Current value of this attribute for this instance.
        """
    
    @property
    def defaultValue(self):
        # type: () -> float
        """
        Returns the default defined value for this attribute.
        """
    
    @property
    def effectiveMax(self):
        # type: () -> float
        """
        Returns the effective max of this attribute given any other ambient components or factors.
        """
    
    @property
    def effectiveMin(self):
        # type: () -> float
        """
        Returns the effective min of this attribute given any other ambient components or factors.
        """
    
    def resetToDefaultValue(self):
        # type: () -> None
        """
        Resets the current value of this attribute to the defined default value.
        """

    def resetToMaxValue(self):
        # type: () -> None
        """
        Resets the current value of this attribute to the defined max value.
        """

    def resetToMinValue(self):
        # type: () -> None
        """
        Resets the current value of this attribute to the defined min value.
        """

    def setCurrentValue(self, value):
        # type: (float) -> None
        """
        Sets the current value of this attribute to the specified value.
        """

class EntityHealthComponent(EntityAttributeComponent):
    """
    Defines the health properties of an entity.
    """
    componentId: Literal['minecraft:health'] = "minecraft:health"

class EntityMovementComponent(EntityAttributeComponent):
    """
    Defines the base movement speed of this entity.
    """
    componentId: Literal['minecraft:movement'] = "minecraft:movement"

class EntityJumpComponent(EntityAttributeComponent):
    """
    Defines the base movement speed of this entity.
    """
    componentId: Literal['minecraft:movement.jump'] = "minecraft:movement.jump"

class EntityLavaMovementComponent(EntityAttributeComponent):
    """
    Defines the base movement speed in lava of this entity.
    """
    componentId: Literal['minecraft:lava_movement'] = "minecraft:lava_movement"

class EntityUnderwaterMovementComponent(EntityAttributeComponent):
    """
    Defines the base movement speed under water of this entity.
    """
    componentId: Literal['minecraft:underwater_movement'] = "minecraft:underwater_movement"


class EntityInventoryComponent(EntityComponent):
    """Defines this entity's inventory properties."""

    componentId: Literal['minecraft:inventory'] = 'minecraft:inventory'
        
    @property
    def container(self) -> Container:
        """
        Defines the container for this entity. 
        The container will be undefined if the entity has been removed.
        """
    

class EntityEquippableComponent(EntityComponent):
    """Provides access to a mob's equipment slots. This component exists on player entities."""
    componentId: Literal['minecraft:equippable'] = "minecraft:equippable"

    @property
    def totalArmor(self) -> int:
        """Returns the total Armor level of the owner."""

    @property
    def totalToughness(self) -> int:
        """Returns the total Toughness level of the owner."""

    def getEquipment(self, equipmentSlot: EquipmentSlot) -> ItemStack:
        """Gets the equipped item for the given EquipmentSlot."""
        
    def setEquipment(self, equipmentSlot: EquipmentSlot, itemStack: ItemStack=None) -> None:
        """Replaces the item in the given EquipmentSlot."""
