# -*- coding: utf-8 -*-
# from typing import Union, Dict
from Scripts_SAPI.Classes.Components import BlockComponent
import mod.server.extraServerApi as serverApi
from ..Classes.Container import *

SComp = serverApi.GetEngineCompFactory()

class BlockInventoryComponent(BlockComponent):
    """Represents the inventory of a block in the world. Used with blocks like chests."""
    __componentId = "minecraft:inventory"
    import Block as b

    def __init__(self, data):
        BlockComponent.__init__(self, data)
        self.__block = data['block'] # type: BlockInventoryComponent.b.Block
        self.__container = None

    @property
    def container(self):
        # type: () -> Container
        """The container."""
        if not self.__container:
            self.__container = Container(self.__block.location.getTuple(), dimId=self.__block.dimension.dimId)
        return self.__container