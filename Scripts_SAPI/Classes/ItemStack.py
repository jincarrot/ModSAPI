# -*- coding: utf-8 -*-
from ..Enumerations import *
import mod.server.extraServerApi as serverApi

SComp = serverApi.GetEngineCompFactory()


class ItemType(object):
    """
    Defines the type of an item.
    """

    def __init__(self, id):
        # type: (str) -> None
        self.__id = id

    @property
    def id(self):
        # type: () -> str
        """
        Item type name
        """
        return self.__id


class ItemStack(object):
    """
    Defines a collection of items.
    """

    import ItemComponents as ic
    
    def __init__(self, itemType, amount):
        # type: (str, int) -> None
        self.__typeId = itemType
        self.__maxAmount = (SComp.CreateItem(self.__typeId).GetItemBasicInfo(self.__typeId) or {}).get('maxStackSize', 1)
        """The maximum stack size. This value varies depending on the type of item. For example, torches have a maximum stack size of 64, while eggs have a maximum stack size of 16."""
        self.amount = amount
        """Number of the items in the stack. Valid values range between 1-255. The provided value will be clamped to the item's maximum stack size."""
        self.__isStackable = False if self.__maxAmount == 1 else True
        self.keepOnDeath = False
        """Gets or sets whether the item is kept on death."""
        self.lockMode = ItemLockMode.none
        """Gets or sets the item's lock mode. The default value is ItemLockMode.none."""
        self.nameTag = None
        """Given name of this stack of items. The name tag is displayed when hovering over the item. Setting the name tag to an empty string or undefined will remove the name tag."""
        self.__lore = []
        self.__components = {}
        self.__generateComponents()

    def __str__(self):
        data = {
            "typeId": self.typeId,
            "amount": self.amount
        }
        return "<ItemStack> %s" % data

    def __generateComponents(self):
        # generate components
        itemData = SComp.CreateItem(serverApi.GetLevelId()).GetItemBasicInfo(self.__typeId) or {}
        if itemData.get("enchant_slot_type", 0):
            self.__components["minecraft:enchantable"] = self.ic.ItemEnchantableComponent({"slots": itemData.get("enchant_slot_type")})
        if itemData.get("maxDurability", 0):
            self.__components['minecraft:durability'] = self.ic.ItemDurabilityComponent({"maxDurability": itemData['maxDurability']})

    @property
    def typeId(self):
        # type: () -> str
        """
        Identifier of the type of items for the stack. If a namespace is not specified, 'minecraft:' is assumed
        """
        return self.__typeId
    
    @property
    def isStackable(self):
        # type: () -> bool
        """
        Returns whether the item is stackable. 
        An item is considered stackable if the item's maximum stack size is greater than 1 and the item does not contain any custom data or properties.
        """
        return self.__isStackable
    
    @property
    def type(self):
        # type: () -> ItemType
        """
        ItemType of the item.
        """
        return ItemType(self.__typeId)
    
    @property
    def maxAmount(self):
        # type: () -> int
        """
        Maximum stack size of the item.
        """
        return self.__maxAmount

    def getItemDict(self):
        # type: () -> dict
        """获取网易物品数据"""
        data = {
            "newItemName": self.__typeId,
            "count": self.amount
        }
        userData = {}
        if self.keepOnDeath:
            userData['minecraft:keep_on_death'] = {'__type__': 1, '__value__': 1}
        if self.lockMode != "none":
            userData['minecraft:item_lock'] = {'__type__': 1, '__value__': 2 if self.lockMode == 'inventory' else 1}
        if self.nameTag:
            SComp.CreateItem(serverApi.GetLevelId()).SetCustomName(data, self.nameTag)
        if userData:
            data['userData'] = userData
        if self.__lore:
            baseInfo = "%name%%category%%enchanting%%attack_damage%\n"
            data['customTips'] = baseInfo + "\n".join(self.__lore)
        for componentId in self.__components:
            if componentId == 'minecraft:enchantable':
                enchantmentList = self.__components['minecraft:enchantable'].getEnchantments()
                enchantData = []
                customEnchantData = []
                for enchantment in enchantmentList:
                    enchantData.append((enchantment._id, enchantment.level)) if self._id >= 0 else customEnchantData.append((enchantment.typeId, enchantment.level))
                data['enchantData'] = enchantData
                data['modEnchantData'] = customEnchantData
            elif componentId == 'minecraft:durability':
                data['durability'] = self.__components['minecraft:durability'].remain
        return data
    
    def getLore(self):
        # type: () -> list[str]
        """
        Returns the lore value - a secondary display string - for an ItemStack.
        """
        return self.__lore

    def setLore(self, loreList=None):
        # type: (list[str]) -> None
        """
        Sets the lore value - a secondary display string - for an ItemStack. 
        The lore list is cleared if set to an empty string or undefined.
        """
        self.__lore = loreList

    def hasComponent(self, componentId):
        # type: (str) -> bool
        """Returns true if the specified component is present on this item stack."""
        return componentId in self.__components

    def getComponent(self, componentId):
        # type: (str) -> None | ic.ItemComponent
        """Gets a component (that represents additional capabilities) for an item stack."""
        if self.hasComponent(componentId):
            return self.__components[componentId]


def createItemStack(itemDict):
    # type: (dict) -> ItemStack | None
    if not itemDict:
        return None
    item = ItemStack(itemDict['newItemName'], itemDict['count'])
    if 'userData' in itemDict and itemDict['userData']:
        userData = itemDict['userData']
        if 'minecraft:keep_on_death' in userData:
            item.keepOnDeath = userData['minecraft:keep_on_death']['__value__'] == 1
        if 'minecraft:item_lock' in userData:
            v = userData['minecraft:item_lock']['__value__']
            item.lockMode = "none" if not v else ("inventory" if v == 2 else "slot")
        if 'display' in userData:
            item.nameTag = userData['display']['__value__']
    if 'customTips' in itemDict:
        item.setLore(itemDict['customTips'].split("\n"))
    if item.hasComponent("minecraft:enchantable"):
        enchantData = itemDict['enchantData']
        customEnchantData = itemDict['modEnchantData']
        enchantList = []
        for enchant in enchantData:
            enchantList.append({"type": EnchantTypes[enchant[0]], "level": enchant[1]})
        for enchant in customEnchantData:
            enchantList.append({"type": enchant[0], 'level': enchant[1]})
        item.getComponent("minecraft:enchantable").asEnchantableComponent().addEnchantments(enchantList)
    if item.hasComponent("minecraft:durability"):
        remain = itemDict['durability']
        item.getComponent("minecraft:durability").asDurabilityComponent().remain = remain
    return item
