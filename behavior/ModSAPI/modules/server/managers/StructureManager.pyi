import types
import mod.server.extraServerApi as serverApi
from ....enums.Structure import *
from ....interfaces.Vector import Vector3
from ....interfaces.BlockBoundingBox import *
from ....interfaces.Structure import *
from ..Dimension import *
from ..Structure import *

SComp = serverApi.GetEngineCompFactory()

class StructureManager:
    """
    Manager for Structure related APIs. Includes APIs for creating, getting, placing and deleting Structures.
    """

    def createEmpty(self, identifier, size, saveMode=StructureSaveMode.Memory):
        # type: (str, Vector3, str) -> Structure
        """Creates an empty Structure in memory. 
        Use @minecraft/server.Structure.setBlockPermutation to populate the structure with blocks,
        and save changes with @minecraft/server.Structure.saveAs."""

    def createFromWorld(self, identifier, dimension, From, to, options={}):
        # type: (str, Dimension, Vector3, Vector3, StructureCreateOptions) -> Structure
        """Creates a new Structure from blocks in the world. 
        This is functionally equivalent to the /structure save command."""

    def delete(self, structure):
        # type: (str | Structure) -> None
        """Deletes a structure from memory and from the world if it exists."""

    def getAllEditableStructures(self):
        # type: () -> list[Structure]
        """Gets all structures that can be edited."""

    def get(self, identifier):
        # type: (str) -> Structure | None
        """Gets a Structure that is saved to memory or the world."""

    def place(self, structure, dimension, location, options={}):
        # type: (Structure | str, Dimension, Vector3, StructurePlaceOptions) -> None
        """Places a structure in the world. This is functionally equivalent to the /structure load command."""
