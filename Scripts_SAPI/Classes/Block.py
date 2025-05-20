# -*- coding: utf-8 -*-
from typing import Any, List, Union, Dict
from Dimension import *
from ..Interfaces.Vector import *
from ..Classes.ItemStack import *


class BlockType(object):
    """
    The type (or template) of a block. 
    Does not contain permutation data (state) other than the type of block it represents.
    """

    def __init__(self, id):
        # type: (str) -> None
        self.__id = id

    @property
    def id(self):
        # type: () -> str
        """
        Block type name
        """
        return self.__id


class BlockPermutation(object):
    """
    Contains the combination of type @minecraft/server.
    BlockType and properties (also sometimes called block state) which describe a block (but does not belong to a specific @minecraft/server.Block).
    """
    
    def __init__(self, block):
        # type: (Block) -> None
        self.__block = block

    @property
    def type(self):
        # type: () -> BlockType
        """
        Block type name
        """
        return self.__block.type

    def __canBeDestroyedByLiquidSpread(self, liquidType='water'):
        # type: (str) -> bool
        """
        Returns whether this block is removed when touched by liquid
        """

    def __canContainLiquid(self, liquidType='water'):
        # type: (str) -> bool
        """
        Returns whether this block can contain liquid
        """

    def getAllStates(self):
        # type: () -> Dict[str, str]
        """
        Returns all available block states associated with this block.
        """
        return SComp.CreateBlockState(serverApi.GetLevelId()).GetBlockStates((self.__block.location.x, self.__block.location.y, self.__block.location.z), self.__block.dimension.dimId)
    
    def getItemStack(self, amount=1):
        # type: (int) -> ItemStack
        """
        Retrieves a prototype item stack based on this block permutation that can be used with item Container/ContainerSlot APIs.
        """
        return ItemStack(self.__block.typeId, amount)
    
    def getState(self, stateName):
        # type: (str) -> Any
        """
        Gets a state for the permutation.
        """
        return self.getAllStates()[stateName]
    
    def getTags(self):
        # type: () -> List[str]
        """
        Creates a copy of the permutation.
        """
        return SComp.CreateBlockInfo(serverApi.GetLevelId()).GetBlockTags(self.__block.typeId)
    
    def hasTag(self, tag):
        # type: (str) -> bool
        """
        Checks to see if the permutation has a specific tag.
        """
        return tag in self.getTags()


class Block(object):
    """
    Represents a block in a dimension. 
    A block represents a unique X, Y, and Z within a dimension and get/sets the state of the block at that location.
    """

    def __init__(self, data):
        self.__dimension = data['dimension']
        self.__location = data['location']
        self.__permutation = BlockPermutation(self)

    def __str__(self):
        data = {
            "dimension": str(self.dimension),
            "location": str(self.location),
            "type": str(self.type),
            "typeId": self.typeId,
            "permutation": str(self.permutation)
        }
        return "<Block> %s" % data

    @property
    def dimension(self):
        # type: () -> Dimension
        """
        Returns the dimension that the block is within.
        """
        return self.__dimension
    
    @property
    def location(self):
        # type: () -> Vector3
        """
        Coordinates of the specified block.
        """
        return self.__location
    
    @property
    def type(self):
        # type: () -> BlockType
        """
        Gets the type of block.
        """
        return BlockType(self.typeId)
    
    @property
    def typeId(self):
        # type: () -> str
        """
        Gets the type of block.
        """
        return SComp.CreateBlockInfo(serverApi.GetLevelId()).GetBlockNew((int(self.location.x), int(self.location.y), int(self.location.z)), self.dimension.dimId)['name']

    @property
    def isAir(self):
        # type: () -> bool
        """
        Returns true if the block is air.
        """
        return self.typeId == "minecraft:air"

    @property
    def isLiquid(self):
        # type: () -> bool
        """
        Returns true if the block is a liquid block.
        """
        liquidData = SComp.CreateBlockInfo(serverApi.GetLevelId()).GetLiquidBlock((int(self.location.x), int(self.location.y), int(self.location.z)), self.dimension.dimId)
        blockData = SComp.CreateBlockInfo(serverApi.GetLevelId()).GetBlockNew((int(self.location.x), int(self.location.y), int(self.location.z)), self.dimension.dimId)
        if liquidData and liquidData['name'] == blockData['name']:
            return True
        else:
            return False
        
    @property
    def isWaterloggeed(self):
        # type: () -> bool
        """
        Returns or sets whether this block has water on it.
        """
        liquidData = SComp.CreateBlockInfo(serverApi.GetLevelId()).GetLiquidBlock((int(self.location.x), int(self.location.y), int(self.location.z)), self.dimension.dimId)
        blockData = SComp.CreateBlockInfo(serverApi.GetLevelId()).GetBlockNew((int(self.location.x), int(self.location.y), int(self.location.z)), self.dimension.dimId)
        if liquidData and liquidData['name'] != blockData['name']:
            return True
        else:
            return False
        
    @property
    def permutation(self):
        # type: () -> BlockPermutation
        """
        Additional block configuration data that describes the block.
        """
        return self.__permutation
    
    @property
    def x(self):
        # type: () -> int
        """
        X coordinate of the block.
        """
        return self.location.x
    
    @property
    def y(self):
        # type: () -> int
        """
        Y coordinate of the block.
        """
        return self.location.y
    
    @property
    def z(self):
        # type: () -> int
        """
        Z coordinate of the block.
        """
        return self.location.z
    
    def above(self, steps):
        # type: (int) -> Block
        """
        Returns the @minecraft/server.Block above this block (positive in the Y direction).
        """
        return Block({'dimension': self.dimension, 'location': Vector3(self.location.x, self.location.y + steps, self.location.z)})
    
    def below(self, steps):
        # type: (int) -> Block
        """
        Returns the @minecraft/server.Block below this block (negative in the Y direction).
        """
        return Block({'dimension': self.dimension, 'location': Vector3(self.location.x, self.location.y - steps, self.location.z)})
    
    def bottomCenter(self):
        # type: () -> Vector3
        """
        Returns the @minecraft/server.Vector3 of the center of this block on the X and Z axis.
        """
        return Vector3({"x": int(self.location.x) + 0.5, "y": int(self.location.y), "z": int(self.location.z) + 0.5})
