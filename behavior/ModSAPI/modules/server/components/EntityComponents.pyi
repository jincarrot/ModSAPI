# -*- coding: utf-8 -*-
# from typing import Union, Dict
from Components import *
import mod.server.extraServerApi as serverApi
from mod.common.minecraftEnum import EntityComponentType
from ..Entity import Entity
from typing import TypeVar

T = TypeVar("T")

class EntityComponent(Component):
    """
    Base class for downstream entity components.
    """
    
    @property
    def entity(self) -> Entity:
        """
        The entity that owns this component. 
        The entity will be undefined if it has been removed.
        """

    def asType(self, componentType: T) -> T: ...


class EntityAddRiderComponent(EntityComponent):
    """
    When added, this component makes the entity spawn with a rider of the specified entityType.
    """
    
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
    def componentId(self):
        # type: () -> str
        """
        The id of the component.
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

class EntityMovementComponent(EntityAttributeComponent):
    """
    Defines the base movement speed of this entity.
    """

class EntityJumpComponent(EntityAttributeComponent):
    """
    Defines the base movement speed of this entity.
    """

class EntityLavaMovementComponent(EntityAttributeComponent):
    """
    Defines the base movement speed in lava of this entity.
    """

class EntityUnderwaterMovementComponent(EntityAttributeComponent):
    """
    Defines the base movement speed under water of this entity.
    """


class EntityInventoryComponent(EntityComponent):
    """Defines this entity's inventory properties."""

    @property
    def componentId(self):
        pass
        
    @property
    def container(self):
        """
        Defines the container for this entity. 
        The container will be undefined if the entity has been removed.
        """
        pass
    
