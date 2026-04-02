# -*- coding: utf-8 -*-
import mod.server.extraServerApi as serverApi
from ItemStack import ItemStack

class Container(object):
    """Represents a container that can hold sets of items. Used with entities such as Players, Chest Minecarts, Llamas, and more."""
    @property
    def emptySlotsCount(self):
        # type: () -> int
        """
        Count of the slots in the container that are empty.

        Note: If this is invalid, return None
        """

    @property
    def size(self):
        # type: () -> int | None
        """
        The number of slots in this container. 
        For example, a standard single-block chest has a size of 27. 
        Note, a player's inventory container contains a total of 36 slots, 9 hotbar slots plus 27 inventory slots.
        """
    
    @property
    def isValid(self):
        # type: () -> bool
        """
        Returns whether a container object (or the entity or block that this container is associated with) is still available for use in this context.
        """

    def addItem(self, itemStack):
        # type: (ItemStack) -> ItemStack | None
        """
        Adds an item to the container. 
        The item is placed in the first available slot(s) and can be stacked with existing items of the same type. 
        Note, use @minecraft/server.Container.setItem if you wish to set the item in a particular slot.
        """

    def clearAll(self):
        # type: () -> None
        """
        Clears all inventory items in the container.
        """

    def getItem(self, slot):
        # type: (int) -> ItemStack | None
        """
        Gets an @minecraft/server.ItemStack of the item at the specified slot. 
        If the slot is empty, returns undefined. 
        This method does not change or clear the contents of the specified slot. 
        To get a reference to a particular slot, see @minecraft/server.Container.getSlot.
        """

    def moveItem(self, fromSlot, toSlot, toContainer=None):
        # type: (int, int, Container) -> None
        """
        Moves an item from one slot to another, potentially across containers.
        """

    def setItem(self, slot, itemStack):
        # type: (int, ItemStack) -> None
        """
        Sets an item stack within a particular slot.
        """

    def swapItems(self, slot, otherSlot, otherContainer=None):
        # type: (int, int, Container) -> None
        """
        Swaps items between two different slots within containers.
        """

    def transferItem(self, fromSlot, toContainer):
        # type: (int, Container) -> ItemStack
        """
        Moves an item from one slot to another container, 
        or to the first available slot in the same container.
        """
