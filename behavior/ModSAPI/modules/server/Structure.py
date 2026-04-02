import types
import mod.server.extraServerApi as serverApi
from ..server.Block import BlockPermutation
from ...interfaces.Vector import Vector3
from ...interfaces.BlockBoundingBox import *
from ...interfaces.Structure import *
from ...enums.Structure import *
from copy import deepcopy
from ...utils.block import BlockPaletteData
from ...utils.system import systems

SComp = serverApi.GetEngineCompFactory()

class Structure:
    """
    Represents a loaded structure template (.mcstructure file). 
    Structures can be placed in a world using the /structure command or the @minecraft/server.StructureManager APIs.
    """

    def __init__(self, data):
        # type: (dict) -> None
        self.__id = data['id'] # type: str
        self.__size = data['size'] # type: Vector3
        self.__data = data['data'] if 'data' in data else None # type: dict
        self.__saveMode = data['saveMode'] if 'saveMode' in data else StructureSaveMode.Memory
        self.__entities = data['entities'] if 'entities' in data else {} # type: dict[tuple[float, float, float], list[dict]]
        """Key is the location and the value is a list includes nbt."""
        self._isValid = True
        self.__bp = BlockPaletteData(self.__data, False)
        if self.__saveMode == StructureSaveMode.World and self.__data:
            systems.world.setDynamicProperty("structure.%s" % self.__id, {"size": self.__size, "saveMode": self.__saveMode, "data": self.__data, "entities": self.__entities})

    def __str__(self):
        return "<Structure> {id: '%s', size: '%s'}" % (self.__id, self.__size)

    @property
    def id(self):
        # type: () -> str
        """The name of the structure. The identifier must include a namespace. 
        For structures created via the /structure command or structure blocks, this namespace defaults to "mystructure"."""
        return self.__id
    
    @property
    def entities(self):
        return self.__entities
    
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
        return self.__size
    
    @property
    def enableEdit(self):
        # type: () -> bool
        """Returns whether the Structure can be edited."""
        return self.__data is not None

    def getBlockPermutation(self, location):
        # type: (Vector3) -> BlockPermutation
        """Returns a BlockPermutation representing the block contained within the Structure at the given location."""
        blockData = self.__bp.getBlock(location.getIntTuple())
        if blockData:
            states = SComp.CreateBlockState(serverApi.GetLevelId()).GetBlockStatesFromAuxValue(blockData[0], blockData[1])
            blockPermutation = BlockPermutation(None, blockData[0], states)
            return blockPermutation

    def getIsWaterLogged(self, location):
        # type: (Vector3) -> bool
        """Returns whether the block at the given location is waterlogged."""
        block = self.__bp.getExtraBlock(location.getIntTuple())
        return block and block[0] == "minecraft:water"

    def saveAs(self, identifier, saveMode):
        # type: (str, StructureSaveMode) -> None
        """Creates a copy of a Structure and saves it with a new name."""

    def saveToWorld(self):
        """Saves a modified Structure to the world file."""
        self.__saveMode = StructureSaveMode.World
        if self.__data:
            systems.world.setDynamicProperty("structure.%s" % self.__id, {"size": self.__size, "saveMode": self.__saveMode, "data": self.__data, "entities": self.__entities})

    def setBlockPermutation(self, location, blockPermutation=None, waterlogged=False):
        # type: (Vector3, BlockPermutation, bool) -> None
        """Sets the block contained within the Structure at the given location to the given BlockPermutation."""
        if not blockPermutation:
            blockPermutation = BlockPermutation(None, "minecraft:air")
        aux = SComp.CreateBlockState(serverApi.GetLevelId()).GetBlockAuxValueFromStates(blockPermutation.type.id, blockPermutation.getAllStates())
        self.__bp.setBlock(location.getIntTuple(), (blockPermutation.type.id, aux))

    def getBlockPalette(self, options):
        # type: (StructurePlaceOptions) -> any
        if self.__data:
            # Generate data.
            data = deepcopy(self.__data)
            rot = options['rotation']
            if rot == StructureRotation.none:
                rot = "Rotate0"
            rot = int(rot.replace("Rotate", ""))
            mirror = options['mirror']
            seed = options['integritySeed']
            integrity = options['integrity']
            # Create and return.
            bpd = BlockPaletteData(data)
            bpd.rotate(rot)
            bpd.mirror(mirror)
            bpd.damage(seed, integrity)
            if not options['waterlogged']:
                bpd.clearExtraWater()
            data = bpd.getData()
            bp = SComp.CreateBlock(serverApi.GetLevelId()).GetBlankBlockPalette()
            bp.DeserializeBlockPalette(data)
            return bp
        else:
            return None

    def getEntities(self, options):
        # type: (StructurePlaceOptions) -> dict[tuple[float, float, float], list[dict]]
        rot = options['rotation']
        if rot == StructureRotation.none:
            rot = "Rotate0"
        rot = int(rot.replace("Rotate", ""))
        mirror = options['mirror']
        data = {}
        for pos in self.__entities:
            newPos = Vector3(pos).rotateY(rot)
            if "Z" in mirror:
                newPos.x = self.size.x - newPos.x - 1
            if "X" in mirror:
                newPos.z = self.size.z - newPos.z - 1
            data[newPos.getTuple()] = self.__entities[pos]
        return data

    def setEntity(self, location, entity):
        # type: (Vector3, any) -> None
        pos = location.getTuple()
        if pos not in self.__entities:
            self.__entities[pos] = []
        self.__entities[pos].append(entity.getNbt())
        if self.__saveMode == StructureSaveMode.World:
            systems.world.setDynamicProperty("structure.%s" % self.__id, {"size": self.__size, "saveMode": self.__saveMode, "data": self.__data, "entities": self.__entities})