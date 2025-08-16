# -*- coding: utf-8 -*-
# from typing import Union, Dict
from Components import BlockComponent
import mod.server.extraServerApi as serverApi

SComp = serverApi.GetEngineCompFactory()

class BlockInventoryComponent(BlockComponent):
    """Represents the inventory of a block in the world. Used with blocks like chests."""
    import Container as c

    def __init__(self, typeId, data):
        BlockComponent.__init__(self, typeId, data)
        self.__block = data['block']

    @property
    def container(self):
        # type: () -> c.Container
        """The container which holds an @minecraft/server.ItemStack."""
        pass