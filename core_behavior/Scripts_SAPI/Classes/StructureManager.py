import types
import mod.server.extraServerApi as serverApi

from ..interfaces.Vector import Vector3
from ..interfaces.BlockBoundingBox import *
from ..interfaces.StructureSaveMode import *

SComp = serverApi.GetEngineCompFactory()

class StructureManager:
    """
    Manager for Structure related APIs. Includes APIs for creating, getting, placing and deleting Structures.
    """

    def __init__(self):
        pass

    def createEmpty(self, identifier, size, saveMode=StructureSaveMode.Memory):
        # type: (str, Vector3, str) -> None
        """Creates an empty Structure in memory. 
        Use @minecraft/server.Structure.setBlockPermutation to populate the structure with blocks,
        and save changes with @minecraft/server.Structure.saveAs."""
