# -*- coding: utf-8 -*-
# from typing import Union, Dict
ConstMeta = None
from Components import *
import mod.server.extraServerApi as serverApi
from mod.common.minecraftEnum import EntityComponentType
from ....enums.Entity import EquipmentSlot
from ..ItemStack import createItemStack

SComp = serverApi.GetEngineCompFactory()


class EntityAddRiderComponent(EntityComponent):
    """
    When added, this component makes the entity spawn with a rider of the specified entityType.
    """
    __metaclass__ = ConstMeta
    componentId = "minecraft:addrider"
    
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

    def __init__(self, data):
        EntityComponent.__init__(self, data)
        self.__comp = SComp.CreateAttr(self.entity.id)
        nbt = SComp.CreateEntityDefinitions(self.entity.id).GetEntityNBTTags()['Attributes']
        self.__attrId = getattr(EntityComponentType, data['componentId'].replace("minecraft:", ""))
        data['componentId'] = data['componentId'].replace("_basic", "")
        for tag in nbt:
            if tag['Name']['__value__'] == data['componentId']:
                self.__defaultValue = tag['Base']['__value__']
                self.__effectiveMax = tag['Max']['__value__']
                self.__effectiveMin = tag['Min']['__value__']
                break

    @property
    def currentValue(self):
        # type: () -> float
        """
        Current value of this attribute for this instance.
        """
        nbt = SComp.CreateEntityDefinitions(self.entity.id).GetEntityNBTTags()['Attributes']
        for tag in nbt:
            if tag['Name']['__value__'] == self.componentId:
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
        SComp.CreateAttr(self.entity.id).SetAttrValue(self.__attrId, self.defaultValue)

    def resetToMaxValue(self):
        # type: () -> None
        """
        Resets the current value of this attribute to the defined max value.
        """
        SComp.CreateAttr(self.entity.id).SetAttrValue(self.__attrId, self.effectiveMax)

    def resetToMinValue(self):
        # type: () -> None
        """
        Resets the current value of this attribute to the defined min value.
        """
        SComp.CreateAttr(self.entity.id).SetAttrValue(self.__attrId, self.effectiveMin)

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
    __metaclass__ = ConstMeta
    componentId = "minecraft:health"

    def __init__(self, data):
        data['componentId'] = "minecraft:health"
        EntityAttributeComponent.__init__(self, data)

class EntityMovementComponent(EntityAttributeComponent):
    """
    Defines the base movement speed of this entity.
    """
    __metaclass__ = ConstMeta
    componentId = "minecraft:movement"

    def __init__(self, data):
        data['componentId'] = self.componentId + "_basic"
        EntityAttributeComponent.__init__(self, data)

class EntityJumpComponent(EntityAttributeComponent):
    """
    Defines the base movement speed of this entity.
    """
    __metaclass__ = ConstMeta
    componentId = "minecraft:movement.jump"

    def __init__(self, data):
        data['componentId'] = self.componentId
        EntityAttributeComponent.__init__(self, data)

class EntityLavaMovementComponent(EntityAttributeComponent):
    """
    Defines the base movement speed in lava of this entity.
    """
    __metaclass__ = ConstMeta
    componentId = "minecraft:lava_movement"

    def __init__(self, data):
        data['componentId'] = self.componentId
        EntityAttributeComponent.__init__(self, data)

class EntityUnderwaterMovementComponent(EntityAttributeComponent):
    """
    Defines the base movement speed under water of this entity.
    """
    __metaclass__ = ConstMeta
    componentId = "minecraft:underwater_movement"

    def __init__(self, data):
        data['componentId'] = self.componentId
        EntityAttributeComponent.__init__(self, data)

class EntityInventoryComponent(EntityComponent):
    """Defines this entity's inventory properties."""
    __metaclass__ = ConstMeta
    componentId = 'minecraft:inventory'

    def __init__(self, data):
        EntityComponent.__init__(self, data)
        from ..Container import Container
        self.__container = Container(entityId=self.entity.id)

    def __str__(self):
        data = {
            "entity": str(self.entity)
        }
        return "<EntityInventoryComponent> %s" % data
        
    @property
    def container(self):
        """
        Defines the container for this entity. 
        The container will be undefined if the entity has been removed.
        """
        return self.__container
    
class EntityEquippableComponent(EntityComponent):
    """Provides access to a mob's equipment slots. This component exists on player entities."""
    __metaclass__ = ConstMeta
    componentId = "minecraft:equippable"

    def __init__(self, data):
        EntityComponent.__init__(self, data)
        self.__itemComp = SComp.CreateItem(self.entity.id)
        self.__attrComp = SComp.CreateAttr(self.entity.id)

    @property
    def totalArmor(self):
        """Returns the total Armor level of the owner."""
        defense = 0
        for i in range(4):
            item = self.__itemComp.GetEntityItem(3, i)
            if item:
                defense += self.__itemComp.GetItemBasicInfo(item['newItemName']).get("armorDefense", 0)
        return defense

    @property
    def totalToughness(self):
        """Returns the total Toughness level of the owner."""
        toughness = 0
        for i in range(4):
            item = self.__itemComp.GetEntityItem(3, i)
            if item:
                toughness += self.__itemComp.GetItemBasicInfo(item['newItemName']).get("armorToughness", 0)
        return toughness

    def getEquipment(self, equipmentSlot):
        """Gets the equipped item for the given EquipmentSlot."""
        posType = 3
        if equipmentSlot == EquipmentSlot.Mainhand:
            posType = 2
        elif equipmentSlot == EquipmentSlot.Offhand:
            posType = 1
        slotPos = 0
        if equipmentSlot == EquipmentSlot.Feet:
            slotPos = 3
        elif equipmentSlot == EquipmentSlot.Legs:
            slotPos = 2
        elif equipmentSlot == EquipmentSlot.Chest:
            slotPos = 1
        elif equipmentSlot == EquipmentSlot.Head:
            slotPos = 0
        elif equipmentSlot == EquipmentSlot.Body:
            slotPos = 1
        itemDict = self.__itemComp.GetEntityItem(posType, slotPos, True)
        if itemDict:
            return createItemStack(itemDict)
        
    def setEquipment(self, equipmentSlot, itemStack=None):
        """Replaces the item in the given EquipmentSlot."""
        posType = 3
        if equipmentSlot == EquipmentSlot.Mainhand:
            posType = 2
        elif equipmentSlot == EquipmentSlot.Offhand:
            posType = 1
        slotPos = 0
        if equipmentSlot == EquipmentSlot.Feet:
            slotPos = 3
        elif equipmentSlot == EquipmentSlot.Legs:
            slotPos = 2
        elif equipmentSlot == EquipmentSlot.Chest:
            slotPos = 1
        elif equipmentSlot == EquipmentSlot.Head:
            slotPos = 0
        elif equipmentSlot == EquipmentSlot.Body:
            slotPos = 1
        if itemStack:
            self.__itemComp.SetEntityItem(posType, slotPos, itemStack.getItemDict())
        else:
            self.__itemComp.SetEntityItem(posType, slotPos, {"newItemName": "minecraft:air", "count": 0})
