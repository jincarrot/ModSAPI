# -*- coding: utf-8 -*-
# from typing import Union, Dict
from Components import *
import mod.server.extraServerApi as serverApi
from ....interfaces.Enchant import *

class ItemComponent(Component):
    """Base type for components associated with blocks."""
    
    def asEnchantableComponent(self):
        # type: () -> ItemEnchantableComponent
        pass

    def asDurabilityComponent(self):
        # type: () -> ItemDurabilityComponent
        pass
    
class ItemEnchantableComponent(ItemComponent):
    """When present on an item, this item can have enchantments applied to it."""

    def canAddEnchantment(self, enchantment):
        # type: (Enchantment | dict) -> bool
        """Checks whether an enchantment can be added to the item stack."""
        pass

    def addEnchantment(self, enchantment):
        # type: (dict | Enchantment) -> None
        """Adds an enchantment to the item stack."""

    def addEnchantments(self, enchantments):
        # type: (list[dict | Enchantment]) -> None
        """Adds a list of enchantments to the item stack."""

    def getEnchantment(self, enchantmentType):
        # type: (str) -> Enchantment
        """Gets the enchantment of a given type from the item stack."""

    def getEnchantments(self):
        # type: () -> list[Enchantment]
        """Gets all enchantments on the item stack."""
    
    def hasEnchantment(self, enchantmentType):
        # type: (str) -> bool
        """Checks whether an item stack has a given enchantment type."""
    
    def removeAllEnchantments(self):
        """Removes all enchantments applied to this item stack."""

    def removeEnchantment(self, enchantmentType):
        # type: (str) -> None
        """Removes an enchantment of the given type."""

class ItemDurabilityComponent(ItemComponent):
    """
    When present on an item, this item can take damage in the process of being used. 
    
    Note that this component only applies to data-driven items.
    """

    @property
    def maxDurability(self):
        # type: () -> int
        """Represents the amount of damage that this item can take before breaking."""
    
    @property
    def remain(self):
        # type: () -> int
        """Represents the current durability"""
    
    @remain.setter
    def remain(self, value):
        # type: (int) -> None
        pass

    @property
    def damage(self):
        # type: () -> int
        """Returns the current damage level of this particular item."""

    @damage.setter
    def damage(self, value):
        # type: (int) -> None
        pass

