# -*- coding: utf-8 -*-
# from typing import Union, Dict
from Scripts_SAPI.Classes.Components import BlockComponent
import mod.server.extraServerApi as serverApi
from ..Classes.Container import *

SComp = serverApi.GetEngineCompFactory()

class BlockInventoryComponent(BlockComponent):
    """Represents the inventory of a block in the world. Used with blocks like chests."""

    def __init__(self, typeId, data):
        BlockComponent.__init__(self, typeId, data)
        self.__block = data['block']

    @property
    def container(self):
        # type: () -> Container
        """The container which holds an @minecraft/server.ItemStack."""
        pass