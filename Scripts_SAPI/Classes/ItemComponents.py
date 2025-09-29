# -*- coding: utf-8 -*-
# from typing import Union, Dict
from Components import *
import mod.server.extraServerApi as serverApi
from ..Interfaces.Enchant import *

SComp = serverApi.GetEngineCompFactory()

enchantInfo = {}
enchantIds = {
    0: "ArmorHead",
    1: "ArmorTorso",
    2: "ArmorFeet",
    3: "ArmorLegs",
    4: "Sword",
    5: "Bow",
    6: "Hoe",
    7: "Shears",
    8: "Flintsteel",
    9: "Axe",
    10: "Pickaxe",
    11: "Shovel",
    12: "FishingRod",
    13: "CarrotStick",
    14: "Elytra",
    15: "Spear",
    16: "Crossbow",
    17: "Shield", 
    18: "CosmeticHead",
    19: "Compass", 
    20: "MushroomStick",
    21: "Brush", 
    22: "HeavyWeapon"
}

class ItemComponent(Component):
    """Base type for components associated with blocks."""
    __componentId = ""
    import ItemStack as i

    def __init__(self, data):
        Component.__init__(self, data)
    
    def asEnchantableComponent(self):
        # type: () -> ItemEnchantableComponent
        return self

    def asDurabilityComponent(self):
        # type: () -> ItemDurabilityComponent
        return self
    
class ItemEnchantableComponent(ItemComponent):
    """When present on an item, this item can have enchantments applied to it."""
    __componentId = "minecraft:enchantable"

    def __init__(self, data):
        ItemComponent.__init__(self, data)
        self.__slots = [] # type: list[str]
        self.__enchantments = [] # type: list[Enchantment]
        # load slots data
        slotsData = data['slots']
        slotList = bin(slotsData)[2::][::-1]
        for i in range(len(slotList)):
            if int(slotList[i]):
                self.__slots.append(enchantIds[i].lower())

    def canAddEnchantment(self, enchantment):
        # type: (Enchantment | dict) -> bool
        """Checks whether an enchantment can be added to the item stack."""
        global enchantInfo
        if not enchantInfo:
            # generate enchant data
            enchantDatas = SComp.CreateItem(serverApi.GetLevelId()).GetAllEnchantsInfo()
            for enchantData in enchantDatas:
                enchantInfo[enchantData['identifier']] = enchantData
        if type(enchantment) == dict:
            enchantment = Enchantment(enchantment['type'], enchantment['level'])
        availableSlots = enchantInfo.get(enchantment.typeId, {}).get("primary_slots", [])
        slots = []
        for slotType in self.__slots:
            slots.append(slotType.lower())
        return True if len([item for item in availableSlots if item in slots]) else False

    def addEnchantment(self, enchantment):
        # type: (dict | Enchantment) -> None
        """Adds an enchantment to the item stack."""
        if self.canAddEnchantment(enchantment):
            if type(enchantment) == dict:
                enchantment = Enchantment(enchantment['type'], enchantment['level'])
            self.__enchantments.append(enchantment)

    def addEnchantments(self, enchantments):
        # type: (list[dict | Enchantment]) -> None
        """Adds a list of enchantments to the item stack."""
        for enchantment in enchantments:
            self.addEnchantment(enchantment)

    def getEnchantment(self, enchantmentType):
        # type: (str) -> Enchantment
        """Gets the enchantment of a given type from the item stack."""
        if enchantmentType in self.__enchantments:
            return self.__enchantments[self.__enchantments.index(enchantmentType)]

    def getEnchantments(self):
        # type: () -> list[Enchantment]
        """Gets all enchantments on the item stack."""
        return self.__enchantments
    
    def hasEnchantment(self, enchantmentType):
        # type: (str) -> bool
        """Checks whether an item stack has a given enchantment type."""
        return enchantmentType in self.__enchantments
    
    def removeAllEnchantments(self):
        """Removes all enchantments applied to this item stack."""
        self.__enchantments = []

    def removeEnchantment(self, enchantmentType):
        # type: (str) -> None
        """Removes an enchantment of the given type."""
        if self.hasEnchantment(enchantmentType):
            self.__enchantments.remove(enchantmentType)

class ItemDurabilityComponent(ItemComponent):
    """
    When present on an item, this item can take damage in the process of being used. 
    
    Note that this component only applies to data-driven items.
    """
    __componentId = "minecraft:durability"

    def __init__(self, data):
        # type: (dict) -> None
        ItemComponent.__init__(self, data)
        self.__maxDurability = data.get('maxDurability', 0)
        self.__currentDurability = data.get('remain', self.__maxDurability)
        self.__damage = self.__maxDurability - self.__currentDurability

    @property
    def maxDurability(self):
        # type: () -> int
        """Represents the amount of damage that this item can take before breaking."""
        return self.__maxDurability
    
    @property
    def remain(self):
        # type: () -> int
        """Represents the current durability"""
        return self.__currentDurability
    
    @remain.setter
    def remain(self, value):
        # type: (int) -> None
        self.__currentDurability = value
        self.__damage = self.__maxDurability - self.__currentDurability

    @property
    def damage(self):
        # type: () -> int
        """Returns the current damage level of this particular item."""
        return self.__damage

    @damage.setter
    def damage(self, value):
        # type: (int) -> None
        self.__damage = value
        self.__currentDurability = self.__maxDurability - value

