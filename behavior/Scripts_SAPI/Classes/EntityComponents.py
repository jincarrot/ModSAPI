# -*- coding: utf-8 -*-
# from typing import Union, Dict
from Components import *
import mod.server.extraServerApi as serverApi
from mod.common.minecraftEnum import EntityComponentType

SComp = serverApi.GetEngineCompFactory()

class EntityComponent(Component):
    """
    Base class for downstream entity components.
    """
    __componentId = ""
    import Entity as en
    
    def __init__(self, data):
        Component.__init__(self, data)
        self.__entity = data['entity']
    
    def __str__(self):
        data = {
            "typeId": self.__componentId,
            "entity": str(self.__entity)
        }
        return "<EntityComponent> %s" % data
    
    @property
    def entity(self):
        # type: () -> en.Entity
        """
        The entity that owns this component. 
        The entity will be undefined if it has been removed.
        """
        return self.__entity

    def asHealthComponent(self): 
        # type: () -> EntityHealthComponent
        return self


class EntityAddRiderComponent(EntityComponent):
    """
    When added, this component makes the entity spawn with a rider of the specified entityType.
    """

    __componentId = "minecraft:addrider"
    
    def __init__(self, typeId, data):
        EntityComponent.__init__(self, typeId, data)
        self.__entityType = data['entityType']
        self.__spawnEvent = data['spawnEvent']
    
    def __str__(self):
        data = {
            "typeId": self.typeId,
            "entity": str(self.entity),
            "entityType": self.entityType,
            "spawnEvent": self.spawnEvent
        }
        return "<EntityComponent> %s" % data
    
    @property
    def entityType(self):
        # type: () -> str
        """
        The type of entity that is added as a rider for this entity when spawned under certain conditions.
        """
        return self.__entityType
    
    @property
    def spawnEvent(self):
        # type: () -> str
        """
        Optional spawn event to trigger on the rider when that rider is spawned for this entity.
        """
        return self.__spawnEvent


class EntityAttributeComponent(EntityComponent):
    """
    This is a base abstract class for any entity component that centers around a number and can have a minimum, maximum, and default defined value.
    """
    import Entity as en
    __componentId = ""

    def __init__(self, data):
        EntityComponent.__init__(self, data)
        self.__entity = data['entity'] # type: EntityAttributeComponent.en.Entity
        self.__comp = SComp.CreateAttr(self.__entity.id)
        nbt = SComp.CreateEntityDefinitions(self.entity.id).GetEntityNBTTags()['Attributes']
        for tag in nbt:
            if tag['Name']['__value__'] == data['componentId']:
                self.__defaultValue = tag['Base']['__value__']
                self.__effectiveMax = tag['Max']['__value__']
                self.__effectiveMin = tag['Min']['__value__']
                break
        self.__attrId = getattr(EntityComponentType, data['componentId'][10::])

    @property
    def componentId(self):
        # type: () -> str
        """
        The id of the component.
        """
        return self.__componentId

    @property
    def currentValue(self):
        # type: () -> float
        """
        Current value of this attribute for this instance.
        """
        nbt = SComp.CreateEntityDefinitions(self.entity.id).GetEntityNBTTags()['Attributes']
        for tag in nbt:
            if tag['Name']['__value__'] == self.__componentId:
                return tag['Current']['__value__']
    
    @property
    def defaultValue(self):
        # type: () -> float
        """
        Returns the default defined value for this attribute.
        """
        return self.__defaultValue
    
    @property
    def effectiveMax(self):
        # type: () -> float
        """
        Returns the effective max of this attribute given any other ambient components or factors.
        """
        return self.__effectiveMax
    
    @property
    def effectiveMin(self):
        # type: () -> float
        """
        Returns the effective min of this attribute given any other ambient components or factors.
        """
        return self.__effectiveMin
    
    def resetToDefaultValue(self):
        # type: () -> None
        """
        Resets the current value of this attribute to the defined default value.
        """
        SComp.CreateAttr(self.entity.id).SetAttrValue(getattr(EntityComponentType, self.componentId.split("minecraft:")[1]), self.defaultValue)

    def resetToMaxValue(self):
        # type: () -> None
        """
        Resets the current value of this attribute to the defined max value.
        """
        SComp.CreateAttr(self.entity.id).SetAttrValue(getattr(EntityComponentType, self.componentId.split("minecraft:")[1]), self.effectiveMax)

    def resetToMinValue(self):
        # type: () -> None
        """
        Resets the current value of this attribute to the defined min value.
        """
        SComp.CreateAttr(self.entity.id).SetAttrValue(getattr(EntityComponentType, self.componentId.split("minecraft:")[0]), self.effectiveMin)

    def setCurrentValue(self, value):
        # type: (float) -> None
        """
        Sets the current value of this attribute to the specified value.
        """
        self.__comp.SetAttrValue(self.__attrId, value)

class EntityHealthComponent(EntityAttributeComponent):
    """
    Defines the health properties of an entity.
    """
    __componentId = "minecraft:health"
    import Entity as e

    def __init__(self, data):
        self._entity = data['entity']
        data['componentId'] = "minecraft:health"
        EntityAttributeComponent.__init__(self, data)

    @property
    def entity(self):
        # type: () -> e.Entity
        return self._entity

class EntityMovementComponent(EntityAttributeComponent):
    """
    Defines the base movement speed of this entity.
    """
    __componentId = "minecraft:movement"
    import Entity as e

    def __init__(self, data):
        EntityAttributeComponent.__init__(self, data)
        self.__entity = data['entity']

    @property
    def entity(self):
        # type: () -> e.Entity
        return self.__entity

class EntityJumpComponent(EntityAttributeComponent):
    """
    Defines the base movement speed of this entity.
    """
    __componentId = "minecraft:movement.jump"
    import Entity as e

    def __init__(self, data):
        EntityAttributeComponent.__init__(self, data)
        self.__entity = data['entity']

    @property
    def entity(self):
        # type: () -> e.Entity
        return self.__entity

class EntityLavaMovementComponent(EntityAttributeComponent):
    """
    Defines the base movement speed in lava of this entity.
    """
    __componentId = "minecraft:lava_movement"
    import Entity as e

    def __init__(self, data):
        EntityAttributeComponent.__init__(self, data)
        self.__entity = data['entity']

    @property
    def entity(self):
        # type: () -> e.Entity
        return self.__entity

class EntityUnderwaterMovementComponent(EntityAttributeComponent):
    """
    Defines the base movement speed under water of this entity.
    """
    __componentId = "minecraft:underwater_movement"
    import Entity as e

    def __init__(self, data):
        EntityAttributeComponent.__init__(self, data)
        self.__entity = data['entity']

    @property
    def entity(self):
        # type: () -> e.Entity
        return self.__entity


class EntityInventoryComponent(EntityComponent):
    """Defines this entity's inventory properties."""
    __componentId = 'minecraft:inventory'
    import Container as con
    import Entity as en

    def __init__(self, data):
        EntityComponent.__init__(self, data)
        self.__entity = data['entity'] # type: EntityInventoryComponent.en.Entity
        self.__container = self.con.Container(None, self.__entity.id)

    def __str__(self):
        data = {
            "entity": str(self.__entity)
        }
        return "<EntityInventoryComponent> %s" % data

    @property
    def componentId(self):
        return self.__componentId
        
    @property
    def container(self):
        # type: () -> con.Container
        """
        Defines the container for this entity. 
        The container will be undefined if the entity has been removed.
        """
        return self.__container
    
