import types
import mod.server.extraServerApi as serverApi
from ..server.Block import BlockPermutation
from ...interfaces.Vector import Vector3
from ...interfaces.BlockBoundingBox import *
from ...interfaces.Structure import *
from ...enums.Structure import *
from Entity import *
from ...utils.system import systems
from mod.common.component import blockPaletteComp

class Structure:
    """
    Represents a loaded structure template (.mcstructure file). 
    Structures can be placed in a world using the /structure command or the @minecraft/server.StructureManager APIs.
    """

    def __str__(self):
        return "<Structure> {id: '%s', size: '%s'}" % (self.__id, self.__size)

    @property
    def id(self):
        # type: () -> str
        """The name of the structure. The identifier must include a namespace. 
        For structures created via the /structure command or structure blocks, this namespace defaults to "mystructure"."""
    
    @property
    def isValid(self):
        # type: () -> bool
        """Returns whether the Structure is valid. The Structure may become invalid if it is deleted."""
        return self._isValid
    
    @property
    def size(self):
        # type: () -> Vector3
        """
        The dimensions of the structure. 
        For example, a single block structure will have a size of {x:1, y:1, z:1}
        """
    
    @property
    def enableEdit(self):
        # type: () -> bool
        """Returns whether the Structure can be edited."""

    def getBlockPermutation(self, location):
        # type: (Vector3) -> BlockPermutation
        """Returns a BlockPermutation representing the block contained within the Structure at the given location."""

    def getIsWaterLogged(self, location):
        # type: (Vector3) -> bool
        """Returns whether the block at the given location is waterlogged."""

    def saveAs(self, identifier, saveMode):
        # type: (str, StructureSaveMode) -> None
        """Creates a copy of a Structure and saves it with a new name."""

    def saveToWorld(self):
        """Saves a modified Structure to the world file."""

    def setBlockPermutation(self, location, blockPermutation=None, waterlogged=False):
        # type: (Vector3, BlockPermutation, bool) -> None
        """Sets the block contained within the Structure at the given location to the given BlockPermutation."""

    def getBlockPalette(self, options) -> blockPaletteComp.BlockPaletteComponent: ...

    def setEntity(self, location, entity):
        # type: (Vector3, Entity) -> None
        """Sets an entity to be included in the Structure at the given location."""