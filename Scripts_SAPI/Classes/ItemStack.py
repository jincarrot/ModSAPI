# -*- coding: utf-8 -*-
from ..Enumerations import *
import mod.server.extraServerApi as serverApi
import mod.client.extraClientApi as clientApi

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

    def __init__(self, itemType, amount):
        # type: (str, int) -> None
        self.__typeId = itemType
        self.__maxAmount = SComp.CreateItem(self.__typeId).GetItemBasicInfo(self.__typeId)['maxStackSize']
        """The maximum stack size. This value varies depending on the type of item. For example, torches have a maximum stack size of 64, while eggs have a maximum stack size of 16."""
        self.amount = amount
        """Number of the items in the stack. Valid values range between 1-255. The provided value will be clamped to the item's maximum stack size."""
        self.__isStackable = False if self.__maxAmount == 1 else True
        self.keepOnDeath = False
        """Gets or sets whether the item is kept on death."""
        self.lockMode = ItemLockMode.none
        """Gets or sets the item's lock mode. The default value is ItemLockMode.none."""
        self.nameTag = self.__typeId.split('minecraft:')[0]
        """Given name of this stack of items. The name tag is displayed when hovering over the item. Setting the name tag to an empty string or undefined will remove the name tag."""

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
