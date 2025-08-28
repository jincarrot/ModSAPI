# -*- coding: utf-8 -*-
# from typing import Union, Dict
from Components import EntityComponent
import mod.server.extraServerApi as serverApi
from mod.common.minecraftEnum import EntityComponentType

SComp = serverApi.GetEngineCompFactory()

class EntityAddRiderComponent(EntityComponent):
    """
    When added, this component makes the entity spawn with a rider of the specified entityType.
    """
    
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
        The entity that owns this component. 
        The entity will be undefined if it has been removed.
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
            if tag['Name']['__value__'] == self.__componentId:
                self.__defaultValue = tag['Base']['__value__']
                self.__effectiveMax = tag['Max']['__value__']
                self.__effectiveMin = tag['Min']['__value__']
                break
        self.__attrId = getattr(EntityComponentType, self.__componentId.split("minecraft:")[1])

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
            if tag['Name']['__value__'] == self.__typeId:
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
        SComp.CreateAttr(self.entity.id).SetAttribute(getattr(EntityComponentType, self.componentId.split("minecraft:")[0]), self.defaultValue)

    def resetToMaxValue(self):
        # type: () -> None
        """
        Resets the current value of this attribute to the defined max value.
        """
        SComp.CreateAttr(self.entity.id).SetAttribute(getattr(EntityComponentType, self.componentId.split("minecraft:")[0]), self.effectiveMax)

    def resetToMinValue(self):
        # type: () -> None
        """
        Resets the current value of this attribute to the defined min value.
        """
        SComp.CreateAttr(self.entity.id).SetAttribute(getattr(EntityComponentType, self.componentId.split("minecraft:")[0]), self.effectiveMin)

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
        return self.con.Container(None, self.__entity.id)
    
