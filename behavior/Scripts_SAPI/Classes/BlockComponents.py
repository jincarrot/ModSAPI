# -*- coding: utf-8 -*-
# from typing import Union, Dict
from Components import *
import mod.server.extraServerApi as serverApi
from ..Classes.Container import *

SComp = serverApi.GetEngineCompFactory()

class BlockComponent(Component):
    """Base type for components associated with blocks."""
    __componentId = ""
    import Block as bl

    def __init__(self, data):
        Component.__init__(self, data)
        self.__block = data['block']

    def __str__(self):
        data = {
            "typeId": self.__componentId,
            "block": str(self.__block)
        }
        return "<BlockComponent> %s" % data
    
    @property
    def block(self):
        # type: () -> bl.Block
        """Block instance that this component pertains to."""
        return self.__block
    
    def asInventoryComponent(self):
        # type: () -> BlockInventoryComponent
        return self

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