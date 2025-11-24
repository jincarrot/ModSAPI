# -*- coding: utf-8 -*-
# from typing import Any, List, Union, Dict
from ..Interfaces.Vector import *
from ..Classes.ItemStack import *

class BlockPaletteData(object):

    def __init__(self, data):
        self.__data = data
        """{
            'extra': {}, 
            'void': False, 
            'actor': {}, 
            'volume': (3, 3, 2), 
            'common': {
                ('minecraft:light_gray_terracotta', 0): [3], 
                ('minecraft:hardened_clay', 0): [4], 
                ('minecraft:white_terracotta', 0): [1], 
                ('minecraft:orange_terracotta', 0): [8], 
                ('minecraft:brown_terracotta', 0): [7], 
                ('minecraft:gray_terracotta', 0): [13], 
                ('minecraft:black_terracotta', 0): [5], 
                ('minecraft:red_terracotta', 0): [2], 
                ('minecraft:yellow_terracotta', 0): [0]
            }, 
            'eliminateAir': False
        }"""
        self.__volume = self.__data['volume'] # type: tuple[int, int, int]
        self.__blocks = self.__data['common'] # type: dict[tuple[str, int], list[int]]
        self.__exludeAirData = ("minecraft:air", 0) in self.__blocks

    def getLocationId(self, location):
        # type: (tuple[int, int, int]) -> int
        """returns the id of this location, or -1 if this location doesn't exist."""
        if location[0] >= self.__volume[0] or location[1] >= self.__volume[1] or location[2] >= self.__volume[2]:
            return -1
        else:
            return location[0] * self.__volume[0] + location[1] * self.__volume[0] * self.__volume[1] + location[2]
        
    def getLocation(self, locId):
        # type: (int) -> tuple[int, int, int]
        """returns the location of this id"""
        sq = self.__volume[0] * self.__volume[1]
        y = locId // sq
        locId %= sq
        x = locId // self.__volume[0]
        z = locId % self.__volume[0]
        return (x, y, z)
    
    def getBlock(self, location):
        # type: (tuple[int, int, int]) -> tuple[str, int]
        """returns block data in this location"""
        locId = self.getLocationId(location)
        if locId < 0:
            raise ValueError("location is not exist in this palette!")
        for (blockType, blockAux) in self.__blocks:
            if locId in self.__blocks[(blockType, blockAux)]:
                return (blockType, blockAux)
        return ("minecraft:air", 0)
            
    def getLocationIds(self, blockData):
        # type: (tuple[str, int] | str) -> list[int]
        """returns the location ids where this block exist."""
        if type(blockData) == str:
            for (blockType, __aux) in self.__blocks:
                if blockType == blockData:
                    return self.__blocks[(blockType, __aux)]
            return []
        else:
            return self.__blocks.get(blockData, [])
            
    def setBlock(self, location, blockData):
        # type: (tuple[int, int, int], tuple[str, int]) -> bool
        """set a block in a location"""
        locId = self.getLocationId(location)
        if locId < 0:
            return False
        ori = self.getBlock(location)
        if self.__exludeAirData or ori[0] != "minecraft:air":
            self.__blocks[ori].remove(locId)
            if not self.__blocks[ori]:
                del self.__blocks[ori]
        if blockData not in self.__blocks:
            self.__blocks[blockData] = []
        self.__blocks[blockData].append(locId)
        return True

    def getData(self):
        # type: () -> dict
        """get data."""
        return self.__data

    def fillBlocks(self, start, end, blockData):
        # type: (tuple[int, int, int], tuple[int, int, int], tuple[str, int]) -> None
        """fills blocks"""
        startId = self.getLocationId(start)
        endId = self.getLocationId(end)
        for id in range(min(startId, endId), max(startId, endId) + 1):
            self.setBlock(id, blockData)

    def fillAllBlocks(self, blockData):
        # type: (tuple[str, int]) -> None
        """fills all blocks"""
        maxNum = self.__volume[0] * self.__volume[1] * self.__volume[2]
        data = list(range(maxNum))
        self.__data['common'] = {}
        self.__blocks = self.__data['common']
        self.__blocks[blockData] = data
    
class BlockVolumeBase(object):

    def __init__(self, data):
        # type: (dict[str, Vector3]) -> None
        self.__fromLocation = data['fromLocation']
        self.__toLocation = data['toLocation']

    def getBlockLocationIterator(self):
        """Fetch a @minecraft/server.BlockLocationIterator that represents all of the block world locations within the specified volume"""
        locs = [] # type: list[Vector3]
        for x in range(min(self.__toLocation.x, self.__fromLocation.x), max(self.__toLocation.x, self.__fromLocation.x) + 1):
            for y in range(min(self.__toLocation.y, self.__fromLocation.y), max(self.__toLocation.y, self.__fromLocation.y) + 1):
                for z in range(min(self.__toLocation.z, self.__fromLocation.z), max(self.__toLocation.z, self.__fromLocation.z) + 1):
                    locs.append(Vector3((x, y, z)))
        return iter(locs)

class BlockVolume(BlockVolumeBase):
    """
    A BlockVolume is a simple interface to an object which represents a 3D rectangle of a given size (in blocks) at a world block location.

    Note that these are not analogous to "min" and "max" values, in that the vector components are not guaranteed to be in any order.

    In addition, these vector positions are not interchangeable with BlockLocation.

    If you want to get this volume represented as range of of BlockLocations, you can use the getBoundingBox utility function.

    This volume class will maintain the ordering of the corner indexes as initially set. imagine that each corner is assigned in Editor - as you move the corner around (potentially inverting the min/max relationship of the bounds) - what

    you had originally selected as the top/left corner would traditionally become the bottom/right.

    When manually editing these kinds of volumes, you need to maintain the identity of the corner as you edit - the BlockVolume utility functions do this.

    Important to note that this measures block sizes (to/from) - a normal AABB (0,0,0) to (0,0,0) would traditionally be of size (0,0,0)

    However, because we're measuring blocks - the size or span of a BlockVolume would actually be (1,1,1)"""

    def __init__(self, fromLocation, toLocation):
        # type: (Vector3, Vector3) -> None
        self.__fromLocation = Vector3(fromLocation)
        self.__toLocation = Vector3(toLocation)
        BlockVolumeBase.__init__(self, {"fromLocation": fromLocation, "toLocation": toLocation})

    @property
    def fromLocation(self):
        return self.__fromLocation
    
    @property
    def toLocation(self):
        return self.__toLocation

class BlockType(object):
    """
    The type (or template) of a block. 
    Does not contain permutation data (state) other than the type of block it represents.
    """

    def __init__(self, id, aux=0):
        # type: (str, int) -> None
        self.__id = id
        self.__aux = aux

    @property
    def id(self):
        # type: () -> str
        """
        Block type name
        """
        return self.__id
    
    @property
    def aux(self):
        # type: () -> int
        return self.__aux


class BlockPermutation(object):
    """
    Contains the combination of type @minecraft/server.
    BlockType and properties (also sometimes called block state) which describe a block (but does not belong to a specific @minecraft/server.Block).
    """
    
    def __init__(self, block=None, blockName=None, states=None):
        # type: (Block, str, dict) -> None
        self.__block = block
        self.__blockName = blockName
        self.__states = states
        if block:
            self.__states = SComp.CreateBlockState(serverApi.GetLevelId()).GetBlockStates((self.__block.location.x, self.__block.location.y, self.__block.location.z), self.__block.dimension.dimId)
            self.__blockName = self.__block.typeId

    def __str__(self):
        data = {
            "type": self.__blockName
        }
        return "<BlockPermutation> %s" % data

    def __eq__(self, obj):
        # type: (BlockPermutation) -> bool
        return self.__blockName == obj.type and self.__states == obj.getAllStates()

    @property
    def type(self):
        # type: () -> BlockType
        """
        Block type name
        """
        return BlockType(self.__blockName)

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
        # type: () -> dict[str, 0]
        """
        Returns all available block states associated with this block.
        """
        return self.__states
    
    def getItemStack(self, amount=1):
        # type: (int) -> ItemStack
        """
        Retrieves a prototype item stack based on this block permutation that can be used with item Container/ContainerSlot APIs.
        """
        return ItemStack(self.__blockName, amount)
    
    def getState(self, stateName):
        # type: (str) -> 0
        """
        Gets a state for the permutation.
        """
        return self.__states[stateName] if stateName in self.__states else None
    
    def getTags(self):
        # type: () -> list[str]
        """
        Get all tags of this permutation.
        """
        return SComp.CreateBlockInfo(serverApi.GetLevelId()).GetBlockTags(self.__blockName)
    
    def hasTag(self, tag):
        # type: (str) -> bool
        """
        Checks to see if the permutation has a specific tag.
        """
        return tag in self.getTags()
    
    def matches(self, blockName, states=None):
        # type: (str, dict) -> bool
        """
        Returns a boolean whether a specified permutation matches this permutation. If states is not specified, matches checks against the set of types more broadly.
        """
        if self.__blockName != blockName:
            return False
        if states:
            current = self.getAllStates()
            for state in states:
                if state in current:
                    if current[state] != states[state]:
                        return False
                else:
                    return False
        return True

    def resolve(self, blockName, states=None):
        # type: (str, dict) -> BlockPermutation
        """
        Given a type identifier and an optional set of properties, will return a BlockPermutation object that is usable in other block APIs (e.g., block.setPermutation)
        """
        return BlockPermutation(None, blockName, states)
        
    def withState(self, stateName, value):
        # type: (str, 0) -> BlockPermutation
        """Returns a derived BlockPermutation with a specific property set."""
        state = self.__states.copy()
        state[stateName] = value
        return BlockPermutation(None, self.__blockName, state)

    def hasState(self, stateName):
        # type: (str) -> bool
        """Returns True if this block has a special state."""
        return stateName in self.__states
    
    def setState(self, stateName, value):
        # type: (str, 0) -> bool
        """Set value of a state.
        
        Note: this method changes the value of self, but not return a new BlockPermutation."""
        if self.hasState(stateName):
            if type(value) == type(self.__states[stateName]):
                self.__states[stateName] = value
            else:
                print("type of state \"%s\" is %s, but not %s." % (stateName, type(self.__states[stateName]).__name__, type(value).__name__))
                return False
        print("state \"%s\" doesn't exist in block \"%s\"" % (stateName, self.__blockName))
        return self.hasState(stateName)


class Block(object):
    """
    Represents a block in a dimension. 
    A block represents a unique X, Y, and Z within a dimension and get/sets the state of the block at that location.
    """
    import BlockComponents as bc
    import Container as con
    import Dimension as d

    def __init__(self, data):
        self.__dimension = data['dimension'] # type: Block.d.Dimension
        self.__location = data['location'] # type: Vector3
        self.__permutation = BlockPermutation(self)

    def __str__(self):
        data = {
            "dimension": str(self.dimension),
            "location": str(self.location),
            "typeId": self.typeId
        }
        return "<Block> %s" % data

    @property
    def dimension(self):
        # type: () -> d.Dimension
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
        return BlockType(self.typeId, SComp.CreateBlockInfo(serverApi.GetLevelId()).GetBlockNew((int(self.location.x), int(self.location.y), int(self.location.z)), self.dimension.dimId)['aux'])
    
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
    
    def above(self, steps=1):
        # type: (int) -> Block
        """
        Returns the @minecraft/server.Block above this block (positive in the Y direction).
        """
        return Block({'dimension': self.dimension, 'location': Vector3({"x": self.location.x, "y": self.location.y + steps, "z": self.location.z})})
    
    def below(self, steps=1):
        # type: (int) -> Block
        """
        Returns the @minecraft/server.Block below this block (negative in the Y direction).
        """
        return Block({'dimension': self.dimension, 'location': Vector3({"x": self.location.x, "y": self.location.y - steps, "z": self.location.z})})
    
    def east(self, steps=1):
        # type: (int) -> Block | None
        """Returns the @minecraft/server.Block to the east of this block (positive in the X direction)."""
        return Block({'dimension': self.dimension, 'location': Vector3({"x": self.location.x + steps, "y": self.location.y, "z": self.location.z})})

    def west(self, steps=1):
        """Returns the @minecraft/server.Block to the east of this block (negative in the X direction)."""
        return Block({'dimension': self.dimension, 'location': Vector3({"x": self.location.x - steps, "y": self.location.y, "z": self.location.z})})

    def north(self, steps=1):
        """Returns the @minecraft/server.Block to the east of this block (negative in the Z direction)."""
        return Block({'dimension': self.dimension, 'location': Vector3({"x": self.location.x, "y": self.location.y, "z": self.location.z - steps})})

    def south(self, steps=1):
        """Returns the @minecraft/server.Block to the east of this block (positive in the Z direction)."""
        return Block({'dimension': self.dimension, 'location': Vector3({"x": self.location.x, "y": self.location.y, "z": self.location.z + steps})})

    def bottomCenter(self):
        # type: () -> Vector3
        """
        Returns the @minecraft/server.Vector3 of the center of this block on the X and Z axis.
        """
        return Vector3({"x": int(self.location.x) + 0.5, "y": int(self.location.y), "z": int(self.location.z) + 0.5})

    def setPermutation(self, permutation):
        # type: (BlockPermutation) -> None
        """
        Sets the block in the dimension to the state of the permutation.
        """
        SComp.CreateBlockState(serverApi.GetLevelId()).SetBlockStates((self.__location.x, self.__location.y, self.__location.z), permutation.getAllStates(), self.__dimension.dimId)

    def getTags(self):
        # type: () -> list[str]
        """
        Returns a set of tags for a block.
        """
        return SComp.CreateBlockInfo(serverApi.GetLevelId()).GetBlockTags(self.typeId)
    
    def hasTag(self, tag):
        # type: (str) -> bool
        """
        Checks to see if the permutation of this block has a specific tag.
        """
        return tag in self.getTags()
    
    def hasComponent(self, componentId):
        # type: (str) -> bool
        """Returns true if the specified component is present on this block."""
        if componentId in ['netease:block_container', "minecraft:inventory", "inventory"]:
            container = self.con.Container(self.__location.getTuple(), dimId=self.__dimension.dimId)
            return container.isValid

    def getComponent(self, componentId):
        # type: (str) -> bc.BlockComponent
        """Gets a component (that represents additional capabilities) for an entity."""
        if self.hasComponent(componentId):
            if componentId in ['netease:block_container', "minecraft:inventory", "inventory"]:
                return self.bc.BlockInventoryComponent({"block": self})
