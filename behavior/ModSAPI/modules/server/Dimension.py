# -*- coding: utf-8 -*-
# from typing import Union, Dict
from ...enums.Dimension import *
import mod.server.extraServerApi as serverApi
from ...interfaces.Vector import *
from ...interfaces.EntityOptions import *
from ...utils.system import systems
from ...interfaces.WorldOptions import *

SComp = serverApi.GetEngineCompFactory()

class Dimension(object):
    """
    A class that represents a particular dimension (e.g., The End) within a world.
    """
    import Entity as __e
    import ItemStack as __i
    import Block as __b
    import Command as __c

    def __init__(self, dimId):
        # type: (int | str) -> None
        if type(dimId).__name__ == 'int':
            self.__dimId = dimId
            self.__id = MinecraftDimensionTypes[self.__dimId] if self.__dimId < len(MinecraftDimensionTypes) else "dm%s" % self.__dimId
        else:
            if dimId.find("minecraft:") >= 0:
                self.__id = dimId
                self.__dimId = MinecraftDimensionTypes.index(self.__id)
            else:
                self.__id = "minecraft:" + dimId
                self.__dimId = MinecraftDimensionTypes.index(self.__id)

    def __str__(self):
        return "<Dimension> {id: '%s'}" % self.id

    @property
    def id(self):
        # type: () -> str
        """
        Identifier of the dimension.
        """
        return self.__id
    
    @property
    def dimId(self):
        # type: () -> int
        """
        id of the dimension.
        """
        return self.__dimId

    def getBlock(self, location):
        # type: (dict | Vector3) -> __b.Block
        """
        Returns a block instance at the given location.
        """
        return self.__b.Block({"dimension": self, "location": Vector3(location) if type(location) == dict else location})

    def getEntities(self, options=EntityQueryOptions):
        # type: (dict | EntityQueryOptions) -> list[__e.Entity]
        """
        Gets the entities in the dimension.
        """
        entityData = serverApi.GetEngineActor()
        entityIds = serverApi.GetPlayerList()
        entities = []
        if options == EntityQueryOptions:
            options = {}
        options = EntityQueryOptions(options) if type(options) == dict else options
        if options.selfCheck():
            for entityId in entityData:
                if entityData[entityId]['dimensionId'] == self.__dimId:
                    entityIds.append(entityId)
            entityIds = options.check(entityIds)
            for entityId in entityIds:
                entities.append(self.__e.Entity(entityId))
        return entities
    
    def getEntitiesAtBlockLocation(self, location):
        # type: (dict | Vector3) -> list[__e.Entity]
        """
        Returns a set of entities at a particular location.
        """
        result = []
        pos = Vector3(location) if type(location) == dict else location
        entityIds = SComp.CreateGame(serverApi.GetLevelId()).GetEntitiesInSquareArea(None, (int(pos.x), int(pos.y), int(pos.z)), (int(pos.x), int(pos.y), int(pos.z)), self.dimId)
        for entityId in entityIds:
            result.append(self.__e.Entity(entityId))
        return result

    def getPlayers(self, options=EntityQueryOptions):
        # type: (dict | EntityQueryOptions) -> list[__e.Player]
        playerIds = serverApi.GetPlayerList()
        if options == EntityQueryOptions:
            options = {}
        options = EntityQueryOptions(options) if type(options) == dict else options
        players = []
        if options.selfCheck():
            for playerId in playerIds:
                if SComp.CreateDimension(playerId).GetEntityDimensionId() != self.dimId:
                    playerIds.remove(playerId)
            playerIds = options.check(playerIds)
            for playerId in playerIds:
                players.append(self.e.Player(playerId))
        return players

    def getPlayer(self, playerId):
        # type: (int | str) -> __e.Player
        """get player by id"""
        return self.e.Player(playerId)
    
    def runCommand(self, commandString):
        # type: (str) -> __c.CommandResult
        """
        Runs a command synchronously using the context of the broader dimenion.

        Note: this may return wrong message.
        """
        SComp.CreateCommand(serverApi.GetLevelId()).SetCommand("execute in %s run %s" % (self.id, commandString))
        index = commandString.find("@")
        if index >= 0:
            selector = ""
            while index < len(commandString):
                hasParam = False
                if commandString[index] == "[":
                    hasParam = True
                if commandString[index] == "]":
                    selector += commandString[index]
                    break
                if commandString[index] == " " and not hasParam:
                    break
                selector += commandString[index]
                index += 1
            return self.__c.CommandResult({"successCount": len(SComp.CreateEntityComponent(self.__id).GetEntitiesBySelector(selector))})
        return None

    def spawnEntity(self, identifier, location, options=SpawnEntityOptions):
        # type: (str, dict | Vector3, dict | SpawnEntityOptions) -> Dimension.__e.Entity
        """
        Creates a new entity (e.g., a mob) at the specified location.
        """
        world = systems.world
        pos = Vector3(location) if type(location) == dict else location
        if options == SpawnEntityOptions:
            options = {}
        options = SpawnEntityOptions(options) if type(options) == dict else options
        entityId = world.CreateEngineEntityByTypeStr(identifier, (pos.x, pos.y, pos.z), (0, options.initialRotation), self.dimId)
        if options.spawnEvent:
            SComp.CreateEntityEvent(serverApi.GetLevelId()).TriggerCustomEvent(entityId, options.spawnEvent)
        if options.initialPersistence:
            SComp.CreateAttr(entityId).SetPersistent(options.initialPersistence)
        return self.__e.Entity(entityId)

    def spawnItem(self, itemStack, location):
        # type: (Dimension.__i.ItemStack, Vector3 | dict) -> Dimension.__e.Entity
        """
        Creates a new item stack as an entity at the specified location.
        """
        world = systems.world
        itemDict = itemStack.getItemDict()
        location = Vector3(location) if type(location) == dict else location
        return Dimension.__e.Entity(world.CreateEngineItemEntity(itemDict, self.__dimId, (location.x, location.y, location.z)))

    def createExplosion(self, location, radius, explosionOptions={}):
        # type: (Vector3 | dict, float, dict | ExplosionOptions) -> bool
        """Creates an explosion at the specified location."""
        location = Vector3(location) if type(location) == dict else location
        options = ExplosionOptions(explosionOptions) if type(explosionOptions) == dict else explosionOptions
        return SComp.CreateExplosion(serverApi.GetLevelId()).CreateExplosion((location.x, location.y, location.z), radius, options.causesFire, options.breaksBlocks, options.source.id, options.source.id)
    
    def fillBlocks(self, volume, block, options):
        # type: (__b.BlockVolume, __b.BlockPermutation | str, 0) -> 0 
        """Fills an area of blocks with a specific block type."""
        if not isinstance(volume, self.__b.BlockVolumeBase):
            print("[Error][ModSAPI][TypeError] volume should be BlockVolumeBase type")
            return
        comp = SComp.CreateBlock(serverApi.GetLevelId())
        data = comp.GetBlockPaletteBetweenPos(self.dimId, volume.fromLocation.getTuple(), volume.toLocation.getTuple(), False).SerializeBlockPalette()
        temp = self.__b.BlockPaletteData(data)
        temp.fillAllBlocks((block.type.id, block.type.aux))
        data = temp.getData()
        p = comp.GetBlankBlockPalette()
        p.DeserializeBlockPalette(data)
        comp.SetBlockByBlockPalette(p, self.dimId, volume.fromLocation.getTuple(), 0)

    def setBlockType(self, location, blockType):
        # type: (Vector3, str) -> None
        """Sets a block at a given location within the dimension."""
        location = Vector3(location)
        SComp.CreateBlockInfo(serverApi.GetLevelId()).SetBlockNew(location.getTuple(), {"name": blockType}, 0, self.dimId)
