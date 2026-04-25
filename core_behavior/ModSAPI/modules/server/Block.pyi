# -*- coding: utf-8 -*-
import mod.server.extraServerApi as serverApi
from ...interfaces.Vector import *
from .components.BlockComponents import *
from ItemStack import *
from Dimension import Dimension

class BlockVolumeBase(object):

    def getBlockLocationIterator(self):
        """Fetch a @minecraft/server.BlockLocationIterator that represents all of the block world locations within the specified volume"""

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
        pass

    @property
    def fromLocation(self) -> Vector3:
        pass
    
    @property
    def toLocation(self) -> Vector3:
        pass

class BlockType(object):
    """
    The type (or template) of a block. 
    Does not contain permutation data (state) other than the type of block it represents.
    """

    @property
    def id(self):
        # type: () -> str
        """
        Block type name
        """
    
    @property
    def aux(self):
        # type: () -> int
        pass

class BlockPermutation(object):
    """
    Contains the combination of type @minecraft/server.
    BlockType and properties (also sometimes called block state) which describe a block (but does not belong to a specific @minecraft/server.Block).
    """

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
    
    def getItemStack(self, amount=1):
        # type: (int) -> ItemStack
        """
        Retrieves a prototype item stack based on this block permutation that can be used with item Container/ContainerSlot APIs.
        """
    
    def getState(self, stateName):
        # type: (str) -> 0
        """
        Gets a state for the permutation.
        """
    
    def getTags(self):
        # type: () -> list[str]
        """
        Get all tags of this permutation.
        """
    
    def hasTag(self, tag):
        # type: (str) -> bool
        """
        Checks to see if the permutation has a specific tag.
        """
    
    def matches(self, blockName, states=None):
        # type: (str, dict) -> bool
        """
        Returns a boolean whether a specified permutation matches this permutation. If states is not specified, matches checks against the set of types more broadly.
        """

    def resolve(self, blockName, states=None):
        # type: (str, dict) -> BlockPermutation
        """
        Given a type identifier and an optional set of properties, will return a BlockPermutation object that is usable in other block APIs (e.g., block.setPermutation)
        """
        
    def withState(self, stateName, value):
        # type: (str, 0) -> BlockPermutation
        """Returns a derived BlockPermutation with a specific property set."""

    def hasState(self, stateName):
        # type: (str) -> bool
        """Returns True if this block has a special state."""
    
    def setState(self, stateName, value):
        # type: (str, 0) -> bool
        """Set value of a state.
        
        Note: this method changes the value of self, but not return a new BlockPermutation."""

class Block(object):
    """
    Represents a block in a dimension. 
    A block represents a unique X, Y, and Z within a dimension and get/sets the state of the block at that location.
    """

    @property
    def dimension(self):
        # type: () -> Dimension
        """
        Returns the dimension that the block is within.
        """
    
    @property
    def location(self):
        # type: () -> Vector3
        """
        Coordinates of the specified block.
        """
    
    @property
    def type(self):
        # type: () -> BlockType
        """
        Gets the type of block.
        """
    
    @property
    def typeId(self):
        # type: () -> str
        """
        Gets the type of block.
        """

    @property
    def isAir(self):
        # type: () -> bool
        """
        Returns true if the block is air.
        """

    @property
    def isLiquid(self):
        # type: () -> bool
        """
        Returns true if the block is a liquid block.
        """
        
    @property
    def isWaterloggeed(self):
        # type: () -> bool
        """
        Returns or sets whether this block has water on it.
        """
        
    @property
    def permutation(self):
        # type: () -> BlockPermutation
        """
        Additional block configuration data that describes the block.
        """
    
    @property
    def x(self):
        # type: () -> int
        """
        X coordinate of the block.
        """
    
    @property
    def y(self):
        # type: () -> int
        """
        Y coordinate of the block.
        """
    
    @property
    def z(self):
        # type: () -> int
        """
        Z coordinate of the block.
        """
    
    def above(self, steps=1):
        # type: (int) -> Block
        """
        Returns the @minecraft/server.Block above this block (positive in the Y direction).
        """
    
    def below(self, steps=1):
        # type: (int) -> Block
        """
        Returns the @minecraft/server.Block below this block (negative in the Y direction).
        """
    
    def east(self, steps=1):
        # type: (int) -> Block | None
        """Returns the @minecraft/server.Block to the east of this block (positive in the X direction)."""

    def west(self, steps=1):
        """Returns the @minecraft/server.Block to the east of this block (negative in the X direction)."""

    def north(self, steps=1):
        """Returns the @minecraft/server.Block to the east of this block (negative in the Z direction)."""

    def south(self, steps=1):
        """Returns the @minecraft/server.Block to the east of this block (positive in the Z direction)."""

    def bottomCenter(self):
        # type: () -> Vector3
        """
        Returns the @minecraft/server.Vector3 of the center of this block on the X and Z axis.
        """

    def setPermutation(self, permutation):
        # type: (BlockPermutation) -> None
        """
        Sets the block in the dimension to the state of the permutation.
        """

    def getTags(self):
        # type: () -> list[str]
        """
        Returns a set of tags for a block.
        """
    
    def hasTag(self, tag):
        # type: (str) -> bool
        """
        Checks to see if the permutation of this block has a specific tag.
        """
    
    def hasComponent(self, componentId):
        # type: (str) -> bool
        """Returns true if the specified component is present on this block."""

    def getComponent(self, componentId):
        # type: (str) -> BlockComponent
        """Gets a component (that represents additional capabilities) for an entity."""
