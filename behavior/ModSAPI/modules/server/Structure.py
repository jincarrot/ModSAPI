import types
import mod.server.extraServerApi as serverApi

from ...interfaces.Vector import Vector3
from ...interfaces.BlockBoundingBox import *
from ...interfaces.StructureSaveMode import *

SComp = serverApi.GetEngineCompFactory()

class Structure:
    """
    Represents a loaded structure template (.mcstructure file). 
    Structures can be placed in a world using the /structure command or the @minecraft/server.StructureManager APIs.
    """

    def __init__(self, data):
        # type: (dict) -> None
        self.__id = data['id']
        self.__size = data['size']

    @property
    def id(self):
        # type: () -> str
        """The name of the structure. The identifier must include a namespace. 
        For structures created via the /structure command or structure blocks, this namespace defaults to "mystructure"."""
        return self.__id
    
    @property
    def isValid(self):
        # type: () -> bool
        """Returns whether the Structure is valid. The Structure may become invalid if it is deleted."""
        return True
    
    @property
    def size(self):
        # type: () -> Vector3
        """The dimensions of the structure. 
        For example, a single block structure will have a size of {x:1, y:1, z:1}"""
        return self.__size

    def saveAs(self, identifier, saveMode):
        pass
