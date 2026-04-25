# -*- coding: utf-8 -*-
from ...enums.Dimension import *
import mod.server.extraServerApi as serverApi
from .components.ItemComponents import *

SComp = serverApi.GetEngineCompFactory()


class ItemType(object):
    """
    Defines the type of an item.
    """

    @property
    def id(self):
        # type: () -> str
        """
        Item type name
        """


class ItemStack(object):
    """
    Defines a collection of items.
    """
    
    def __init__(self, itemType, amount):
        # type: (str, int) -> None
        self.amount = amount
        """Number of the items in the stack. Valid values range between 1-255. The provided value will be clamped to the item's maximum stack size."""
        self.keepOnDeath = False
        """Gets or sets whether the item is kept on death."""
        self.lockMode = ItemLockMode.none
        """Gets or sets the item's lock mode. The default value is ItemLockMode.none."""
        self.nameTag = None
        """Given name of this stack of items. The name tag is displayed when hovering over the item. Setting the name tag to an empty string or undefined will remove the name tag."""

    def __str__(self):
        data = {
            "typeId": self.typeId,
            "amount": self.amount
        }
        return "<ItemStack> %s" % data

    @property
    def typeId(self):
        # type: () -> str
        """
        Identifier of the type of items for the stack. If a namespace is not specified, 'minecraft:' is assumed
        """
    
    @property
    def isStackable(self):
        # type: () -> bool
        """
        Returns whether the item is stackable. 
        An item is considered stackable if the item's maximum stack size is greater than 1 and the item does not contain any custom data or properties.
        """
    
    @property
    def type(self):
        # type: () -> ItemType
        """
        ItemType of the item.
        """
    
    @property
    def maxAmount(self):
        # type: () -> int
        """
        Maximum stack size of the item.
        """
    
    def getLore(self):
        # type: () -> list[str]
        """
        Returns the lore value - a secondary display string - for an ItemStack.
        """

    def setLore(self, loreList=None):
        # type: (list[str]) -> None
        """
        Sets the lore value - a secondary display string - for an ItemStack. 
        The lore list is cleared if set to an empty string or undefined.
        """

    def hasComponent(self, componentId):
        # type: (str) -> bool
        """Returns true if the specified component is present on this item stack."""

    def getComponent(self, componentId):
        # type: (str) -> None | ItemComponent
        """Gets a component (that represents additional capabilities) for an item stack."""

    def getDynamicProperty(self, identifier):
        # type: (str) -> 0
        """Returns a property value."""
    
    def getDynamicPropertyIds(self):
        # type: () -> list[str]
        """Returns the available set of dynamic property identifiers that have been used on this entity."""
    
    def setDynamicProperty(self, identifier, value=None):
        # type: (str, 0) -> None
        """Sets a specified property to a value. Note: This function only works with non-stackable items."""

    def setDynamicProperties(self, values):
        # type: (dict) -> None
        """Sets multiple dynamic properties with specific values."""

def createItemStack(itemDict):
    # type: (dict) -> ItemStack | None
    pass