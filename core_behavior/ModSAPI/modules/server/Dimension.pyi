# -*- coding: utf-8 -*-
# from typing import Union, Dict
from ...enums.Dimension import *
import mod.server.extraServerApi as serverApi
from ...interfaces.Vector import Vector3
from ...interfaces.EntityOptions import *
from ...utils.system import systems
from ...interfaces.WorldOptions import *
import time
from Player import Player
from Entity import Entity
from ItemStack import ItemStack
from Block import Block
from Command import CommandResult
from MolangVariableMap import MolangVariableMap

SComp = serverApi.GetEngineCompFactory()

class DimensionLocation(object):
    """An exact coordinate within the world, including its dimension and location."""

    def __init__(self, dimension, location):
        # type: (Dimension, Vector3) -> None
        self.__dimension = dimension
        self.__location = location

    @property
    def dimension(self):
        return self.__dimension
    
    @dimension.setter
    def dimension(self, value):
        # type: (Dimension) -> None
        self.__dimension = value

    @property
    def x(self):
        return self.__location.x

    @x.setter
    def x(self, value):
        self.__location.x = value
    
    @property
    def y(self):
        return self.__location.y
    
    @y.setter
    def y(self, value):
        self.__location.y = value
    
    @property
    def z(self):
        return self.__location.z

    @z.setter
    def z(self, value):
        self.__location.z = value


class Dimension(object):
    """
    A class that represents a particular dimension (e.g., The End) within a world.
    """

    def __str__(self):
        return "<Dimension> {id: %s}" % self.id

    @property
    def id(self):
        # type: () -> str
        """
        Identifier of the dimension.
        """
    
    @property
    def dimId(self):
        # type: () -> int
        """
        id of the dimension.
        """

    def getBlock(self, location):
        # type: (Vector3) -> Block
        """
        Returns a block instance at the given location.
        """

    def getEntities(self, options={}):
        # type: (EntityQueryOptions) -> list[Entity]
        """
        Gets the entities in the dimension.
        """
    
    def getEntitiesAtBlockLocation(self, location):
        # type: (Vector3) -> list[Entity]
        """
        Returns a set of entities at a particular location.
        """

    def getPlayers(self, options={}):
        # type: (EntityQueryOptions) -> list[Player]
        """"""

    def getPlayer(self, playerId):
        # type: (int | str) -> Player
        """get player by id."""
    
    def runCommand(self, commandString):
        # type: (str) -> CommandResult
        """
        Runs a command synchronously using the context of the broader dimenion.

        Note: this may return wrong message.
        """

    def spawnEntity(self, identifier, location, options=SpawnEntityOptions):
        # type: (str, Vector3,  SpawnEntityOptions) -> Entity
        """
        Creates a new entity (e.g., a mob) at the specified location.
        """

    def spawnParticle(self, effectName: str, location: Vector3, molangVariables: MolangVariableMap = None):
        """
        Creates a new particle emitter at a specified location in the world.
        """

    def spawnItem(self, itemStack, location):
        # type: (ItemStack, Vector3) -> Entity
        """
        Creates a new item stack as an entity at the specified location.
        """

    def createExplosion(self, location, radius, explosionOptions={}):
        # type: (Vector3, float, ExplosionOptions) -> bool
        """Creates an explosion at the specified location."""

    def fillBlocks(self, volume, block, options):
        # type: (BlockVolume, BlockPermutation | str, 0) -> 0 
        """Fills an area of blocks with a specific block type."""

    def setBlockType(self, location, blockType):
        # type: (Vector3, str) -> None
        """Sets a block at a given location within the dimension."""
