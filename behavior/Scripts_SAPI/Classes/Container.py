# -*- coding: utf-8 -*-
import mod.server.extraServerApi as serverApi

SComp = serverApi.GetEngineCompFactory()


class Container(object):
    """Represents a container that can hold sets of items. Used with entities such as Players, Chest Minecarts, Llamas, and more."""
    import ItemStack as i
    def __init__(self, location=None, entityId=None, dimId=None):
        # type: (tuple, str, int) -> None
        self.__location = location
        self.__entityId = entityId
        self.__playerId = entityId if entityId and SComp.CreateEngineType(entityId).GetEngineTypeStr() == 'minecraft:player' else None
        self.__dimId = dimId
        self.__size = -1

    def __str__(self):
        data = {
            "size": self.size
        }
        return "<Container> %s" % data

    @property
    def emptySlotsCount(self):
        # type: () -> int
        """
        Count of the slots in the container that are empty.

        Note: If this is invalid, return None
        """
        amount = 0
        if not self.isValid:
            return None
        if self.__location:
            comp = SComp.CreateItem(serverApi.GetLevelId())
            for i in range(0, self.size):
                if not comp.GetContainerItem(self.__location, i, self.__dimId):
                    amount += 1
        elif self.__entityId:
            nbt = SComp.CreateEntityDefinitions(self.__entityId).GetEntityNBTTags()
            inv = nbt['ChestItems'] if not self.__playerId else nbt['Inventory']
            for item in inv:
                if not item['Count']['__value__']:
                    amount += 1
        return amount

    @property
    def size(self):
        # type: () -> int | None
        """
        The number of slots in this container. 
        For example, a standard single-block chest has a size of 27. 
        Note, a player's inventory container contains a total of 36 slots, 9 hotbar slots plus 27 inventory slots.
        """
        # detect self.__size and save source
        if self.__size != -1:
            return self.__size
        size = -1
        if self.__location:
            if SComp.CreateBlockInfo(serverApi.GetLevelId()).GetBlockNew(self.__location, self.__dimId)['name'] == 'minecraft:ender_chest':
                size = 27
            else:
                size = SComp.CreateItem(serverApi.GetLevelId()).GetContainerSize(self.__location, self.__dimId)
        elif self.__playerId:
            size = 36
        elif self.__entityId:
            nbt = SComp.CreateEntityDefinitions(self.__entityId).GetEntityNBTTags()
            if nbt['ChestItems']:
                inv = nbt['ChestItems']
                size = len(inv)
        self.__size = size if size != -1 else None
        return size if size != -1 else None
    
    @property
    def isValid(self):
        # type: () -> bool
        """
        Returns whether a container object (or the entity or block that this container is associated with) is still available for use in this context.
        """
        if self.size or self.size == 0:
            return True
        else:
            return False

    def addItem(self, itemStack):
        # type: (i.ItemStack) -> i.ItemStack | None
        """
        Adds an item to the container. 
        The item is placed in the first available slot(s) and can be stacked with existing items of the same type. 
        Note, use @minecraft/server.Container.setItem if you wish to set the item in a particular slot.
        """
        if not self.isValid:
            return None
        if not itemStack:
            return None
        itemDict = itemStack.getItemDict()
        itemDict['count'] = 1
        if self.__playerId:
            for i in range(0, itemStack.amount):
                if not SComp.CreateItem(serverApi.GetLevelId()).SpawnItemToPlayerInv(itemDict, self.__playerId):
                    break
                itemStack.amount -= 1
            return itemStack if itemStack.amount > 0 else None
        elif self.__entityId:
            if self.emptySlotsCount:
                # has empty slots
                InvComp = SComp.CreateItem(self.__entityId)
                for slotId in range(0, self.size):
                    if itemStack.amount < 1:
                        return None
                    slotData = InvComp.GetEntityItem(0, slotId, True)
                    if (not slotData) or (slotData['newItemName'] == itemStack.typeId and slotData['count'] < itemStack.maxAmount and slotData['userData'] == itemDict['userData']):
                        # get empty or stackable slot
                        if not slotData:
                            slotData = itemDict
                            slotData['count'] = 0
                        itemDict['count'] = slotData['count'] + itemStack.amount
                        itemDict['count'] = itemDict['count'] if itemDict['count'] <= itemStack.maxAmount else itemStack.maxAmount
                        itemStack.amount -= itemDict['count'] - slotData['count']
                        InvComp.SetEntityItem(0, itemDict, slotId)
                return itemStack if itemStack.amount > 0 else None
        elif self.__location:
            if self.emptySlotsCount:
                comp = SComp.CreateItem(serverApi.GetLevelId())
                for i in range(0, self.size):
                    if itemStack < 1:
                        return None
                    slotData = comp.GetContainerItem(self.__location, i, self.__dimId)
                    if (not slotData) or (slotData['newItemName'] == itemStack.typeId and slotData['count'] < itemStack.maxAmount and slotData['userData'] == itemDict['userData']):
                        if not slotData:
                            slotData = itemDict
                            slotData['count'] = 0
                        itemDict['count'] = slotData['count'] + itemStack.amount
                        itemDict['count'] = itemDict['count'] if itemDict['count'] <= itemStack.maxAmount else itemStack.maxAmount
                        itemStack.amount -= itemDict['count'] - slotData['count']
                        # vanilla container
                        comp.SpawnItemToContainer(itemDict, i, self.__location, self.__dimId)
                        if not comp.GetContainerItem(self.__location, i, self.__dimId):
                            # custom container
                            nbt = SComp.CreateBlockInfo(serverApi.GetLevelId()).GetBlockEntityData(self.__dimId, self.__location)
                            data = {
                                'Count': {'__type__': 1, '__value__': itemDict['count']}, 
                                'Slot': {'__type__': 1, '__value__': i}, 
                                'Name': {'__type__': 8, '__value__': itemDict['newItemName']}
                            }
                            if 'userData' in itemDict:
                                data['tag'] = itemDict['userData']
                            nbt['Items'].append(data)
                            SComp.CreateBlockInfo(serverApi.GetLevelId()).SetBlockEntityData(self.__dimId, self.__location, nbt)
                return itemStack if itemStack.amount > 0 else None
        return None

    def clearAll(self):
        # type: () -> None
        """
        Clears all inventory items in the container.
        """
        if not self.isValid:
            return
        comp = SComp.CreateItem(self.__entityId)
        if self.__playerId:
            for i in range(0, self.size):
                comp.SetInvItemNum(i, 0)
        elif self.__entityId:
            for i in range(0, self.size):
                comp.SetEntityItem(0, None, i)
        elif self.__location:
            nbt = SComp.CreateBlockInfo(serverApi.GetLevelId()).GetBlockEntityData(self.__dimId, self.__location)
            nbt['Items'] = []
            SComp.CreateBlockInfo(serverApi.GetLevelId()).SetBlockEntityData(self.__dimId, self.__location, nbt)

    def getItem(self, slot):
        # type: (int) -> i.ItemStack | None
        """
        Gets an @minecraft/server.ItemStack of the item at the specified slot. 
        If the slot is empty, returns undefined. 
        This method does not change or clear the contents of the specified slot. 
        To get a reference to a particular slot, see @minecraft/server.Container.getSlot.
        """
        if not self.isValid:
            return None
        comp = SComp.CreateItem(self.__entityId)
        if self.__playerId:
            itemDict = comp.GetPlayerItem(0, slot, True)
            if not itemDict:
                return None
            item = self.i.createItemStack(itemDict)
            return item
        elif self.__entityId:
            itemDict = comp.GetEntityItem(0, slot, True)
            if not itemDict:
                return None
            item = self.i.createItemStack(itemDict)
            return item
        elif self.__location:
            itemDict = comp.GetContainerItem(self.__location, slot, self.__dimId, True)
            if not itemDict:
                return None
            item = self.i.createItemStack(itemDict)
            return item
        return None

    def moveItem(self, fromSlot, toSlot, toContainer=None):
        # type: (int, int, Container) -> None
        """
        Moves an item from one slot to another, potentially across containers.
        """
        if not toContainer:
            toContainer = self
        item = self.getItem(fromSlot)
        toContainer.setItem(toSlot, item)

    def setItem(self, slot, itemStack):
        # type: (int, i.ItemStack) -> None
        """
        Sets an item stack within a particular slot.
        """
        if not self.isValid:
            return None
        if not itemStack:
            itemStack = self.i.ItemStack("minecraft:air", 0)
        itemDict = itemStack.getItemDict()
        if self.__playerId:
            SComp.CreateItem(self.__entityId).SpawnItemToPlayerInv(itemDict, self.__playerId, slot)
            return itemStack
        elif self.__entityId:
            SComp.CreateItem(self.__entityId).SetEntityItem(0, itemDict, slot)
            return itemStack
        elif self.__location:
            if self.emptySlotsCount:
                comp = SComp.CreateItem(serverApi.GetLevelId())
                comp.SpawnItemToContainer(itemDict, slot, self.__location, self.__dimId)
                if not comp.GetContainerItem(self.__location, slot, self.__dimId):
                    nbt = SComp.CreateBlockInfo(serverApi.GetLevelId()).GetBlockEntityData(self.__dimId, self.__location)
                    data = {
                        'Count': {'__type__': 1, '__value__': itemDict['count']}, 
                        'Slot': {'__type__': 1, '__value__': slot}, 
                        'Name': {'__type__': 8, '__value__': itemDict['newItemName']}
                    }
                    if 'userData' in itemDict:
                        data['tag'] = itemDict['userData']
                    nbt['Items'].append(data)
                    SComp.CreateBlockInfo(serverApi.GetLevelId()).SetBlockEntityData(self.__dimId, self.__location, nbt)
                return itemStack
        return None

    def swapItems(self, slot, otherSlot, otherContainer=None):
        # type: (int, int, Container) -> None
        """
        Swaps items between two different slots within containers.
        """
        if not otherContainer:
            otherContainer = self
        item_a = self.getItem(slot)
        item_b = otherContainer.getItem(otherSlot)
        otherContainer.setItem(otherSlot, item_a)
        self.setItem(slot, item_b)

    def transferItem(self, fromSlot, toContainer):
        # type: (int, Container) -> i.ItemStack
        """
        Moves an item from one slot to another container, 
        or to the first available slot in the same container.
        """
        if not toContainer:
            toContainer = self
        item = self.getItem(fromSlot)
        toContainer.addItem(item)
    