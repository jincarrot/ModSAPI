import types
import mod.server.extraServerApi as serverApi
from ....enums.Structure import *
from ....interfaces.Vector import Vector3
from ....interfaces.BlockBoundingBox import *
from ....interfaces.Structure import *
from ..Dimension import *
from ..Structure import *
from ....errors.structure import *
from ....utils.system import systems
from ....utils.block import BlockPaletteData
import random

SComp = serverApi.GetEngineCompFactory()

class StructureManager:
    """
    Manager for Structure related APIs. Includes APIs for creating, getting, placing and deleting Structures.
    """

    def __init__(self):
        self.__structures = {} # type: dict[str, Structure]

    def _setStructure(self, identifier, structure, saveMode):
        # type: (str, Structure, StructureSaveMode) -> None
        data = structure._getData()
        data['saveMode'] = saveMode
        self.__structures[identifier] = Structure(data)

    def createEmpty(self, identifier, size, saveMode=StructureSaveMode.Memory):
        # type: (str, Vector3, str) -> Structure
        """Creates an empty Structure in memory. 
        Use @minecraft/server.Structure.setBlockPermutation to populate the structure with blocks,
        and save changes with @minecraft/server.Structure.saveAs."""
        structure = Structure({'id': identifier, 'size': size, 'saveMode': saveMode})
        self.__structures[identifier] = structure
        return structure

    def createFromWorld(self, identifier, dimension, From, to, options={}):
        # type: (str, Dimension, Vector3, Vector3, StructureCreateOptions) -> Structure
        """Creates a new Structure from blocks in the world. 
        This is functionally equivalent to the /structure save command."""
        options["includeBlocks"] = options["includeBlocks"] if "includeBlocks" in options else True
        options["includeEntities"] = options["includeEntities"] if "includeEntities" in options else True
        options["includeAir"] = options["includeAir"] if "includeAir" in options else True
        options["saveMode"] = options["saveMode"] if "saveMode" in options else StructureSaveMode.Memory
        size = to - From
        size.x = abs(size.x) + 1
        size.y = abs(size.y) + 1
        size.z = abs(size.z) + 1
        bp = SComp.CreateBlock(serverApi.GetLevelId()).GetBlockPaletteBetweenPos(dimension.dimId, From.getIntTuple(), to.getIntTuple())
        structure = Structure({'id': identifier, 'size': size, 'saveMode': options["saveMode"], 'data': bp.SerializeBlockPalette(), 'includeAir': options["includeAir"]})
        self.__structures[identifier] = structure
        entities = dimension.getEntities({"location": {"x": min(From.x, to.x), "y": min(From.y, to.y), "z": min(From.z, to.z)}, "volume": size})
        for entity in entities:
            structure.setEntity(entity.location - From, entity)
        return structure

    def delete(self, structure):
        # type: (str | Structure) -> None
        """Deletes a structure from memory and from the world if it exists."""
        if structure in self.__structures or structure in self.__structures.values():
            self.__structures[structure if type(structure) == str else structure.id]._isValid = False
            del self.__structures[structure if type(structure) == str else structure.id]
        SComp.CreateCommand(serverApi.GetLevelId()).SetCommand("structure delete %s" % (structure if type(structure) == str else structure.id))

    def getAllEditableStructures(self):
        # type: () -> list[Structure]
        """Gets all structures that can be edited."""
        return [structure for structure in self.__structures.values() if structure.enableEdit]

    def get(self, identifier):
        # type: (str) -> Structure | None
        """Gets a Structure that is saved to memory or the world."""
        if identifier in self.__structures:
            return self.__structures[identifier]
        structureData = systems.world.getDynamicProperty("structure.%s" % identifier)
        if structureData:
            structure = Structure(
                {
                    "id": identifier, 
                    "size": structureData['size'], 
                    "includeAir": structureData['includeAir'],
                    "data": structureData['data'], 
                    "entities": structureData['entities'],
                }
            )
            self.__structures[identifier] = structure
            return structure
        size = SComp.CreateGame(serverApi.GetLevelId()).GetStructureSize(identifier)
        if size:
            print("[Warn][ModSAPI] Structure '%s' existed, but cannot be edited." % identifier)
            return Structure(
            {
                "id": identifier,
                "size": Vector3(size),
                "saveMode": StructureSaveMode.World
            })
        else:
            return None

    def place(self, structure, dimension, location, options={}):
        # type: (Structure | str, Dimension, Vector3, StructurePlaceOptions) -> None
        """Places a structure in the world. This is functionally equivalent to the /structure load command."""
        if not self.get(structure if type(structure) == str else structure.id):
            raise InvalidStructureError("Structure '%s' does not exist in memory or the world." % structure)
        pos = Vector3(location).getIntTuple()
        identifier = structure if type(structure) == str else structure.id
        dimId = dimension.dimId
        options["animationMode"] = options["animationMode"] if "animationMode" in options else "None"
        options["animationSeconds"] = options["animationSeconds"] if "animationSeconds" in options else 0
        options["includeBlocks"] = options["includeBlocks"] if "includeBlocks" in options else True
        options["includeEntities"] = options["includeEntities"] if "includeEntities" in options else True
        options["integrity"] = options["integrity"] if "integrity" in options else 100
        options["integritySeed"] = options["integritySeed"] if "integritySeed" in options else random.randint(-2147483648, 2147483647)
        options["mirror"] = options["mirror"] if "mirror" in options else StructureMirrorAxis.none
        options["rotation"] = options["rotation"] if "rotation" in options else StructureRotation.none
        options["waterlogged"] = options["waterlogged"] if "waterlogged" in options else False
        if structure in self.__structures or structure in self.__structures.values():
            """Structure that was created by API."""
            if options['includeBlocks']:
                bp = structure.getBlockPalette(options)
                SComp.CreateBlock(serverApi.GetLevelId()).SetBlockByBlockPalette(bp, dimension.dimId, location.getIntTuple(), 0)
            if options['includeEntities']:
                entities = structure.getEntities(options)
                for pos in entities:
                    for entity in entities[pos]:
                        if not entity:
                            continue
                        systems.world.CreateEngineEntityByNBT(
                            entity, 
                            (pos[0] + location.x, pos[1] + location.y, pos[2] + location.z),
                            (0, 0),
                            dimension.dimId
                        )
        else:
            """Structure that was saved by command or others."""
            SComp.CreateGame(serverApi.GetLevelId()).PlaceStructure(
                None, pos, identifier, dimId, 
                int(options['rotation'].replace("Rotate", "")) if options['rotation'] != StructureRotation.none else 0,
                STRUCTUREANIMATIONS.index(options['animationMode']),
                options['animationSeconds'],
                options['includeEntities'],
                not options['includeBlocks'],
                STRUCTUREMIRRORS.index(options['mirror']),
                options['integrity'] * 100,
                options['integritySeed']
            )