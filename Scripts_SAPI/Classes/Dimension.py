# -*- coding: utf-8 -*-
# from typing import Union, Dict
from ..Enumerations import *
import mod.server.extraServerApi as serverApi
import mod.client.extraClientApi as clientApi

SComp = serverApi.GetEngineCompFactory()


class Dimension(object):
    """
    A class that represents a particular dimension (e.g., The End) within a world.
    """

    def __init__(self, dimId):
        # type: (Union[int, str]) -> None
        if type(dimId).__name__ == 'int':
            self.__dimId = dimId
            self.__id = MinecraftDimensionTypes[self.__dimId]
        else:
            if dimId.find("minecraft:") >= 0:
                self.__id = dimId
                self.__dimId = MinecraftDimensionTypes.index(self.__id)
            else:
                self.__id = "minecraft:" + dimId
                self.__dimId = MinecraftDimensionTypes.index(self.__id)

    def __str__(self):
        return "<Dimension> {id: %s}" % self.id

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

    def getEntities(self, options=None):
        # type: (None) -> List[Entity]
        """
        Gets the entities in the dimension.
        """
        import Entity as En
        entityData = serverApi.GetEngineActor()
        entities = []
        for data in entityData:
            if entityData[data]['dimensionId'] == self.__dimId:
                entities.append(En.Entity(data))
        return entities
