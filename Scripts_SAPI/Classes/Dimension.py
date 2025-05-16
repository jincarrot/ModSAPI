# -*- coding: utf-8 -*-
# from typing import Union, Dict
from ..Enumerations import *
import mod.server.extraServerApi as serverApi
import mod.client.extraClientApi as clientApi

SComp = serverApi.GetEngineCompFactory()
CComp = clientApi.GetEngineCompFactory()


class Dimension(object):
    """
    A class that represents a particular dimension (e.g., The End) within a world.
    """

    def __init__(self, dimId):
        # type: (int) -> None
        self.__dimId = dimId
        self.__id = MinecraftDimensionTypes[self.__dimId]

    def __str__(self):
        return "<Dimension> {id: %s}" % self.id

    @property
    def id(self):
        # type: () -> str
        """
        Identifier of the dimension.
        """
        return self.__id
