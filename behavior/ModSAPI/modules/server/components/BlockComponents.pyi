# -*- coding: utf-8 -*-
# from typing import Union, Dict
from Components import *
import mod.server.extraServerApi as serverApi
from Container import *
from Block import Block

SComp = serverApi.GetEngineCompFactory()

class BlockComponent(Component):
    """Base type for components associated with blocks."""

    @property
    def block(self):
        # type: () -> Block
        """Block instance that this component pertains to."""
    
    def asInventoryComponent(self):
        # type: () -> BlockInventoryComponent
        pass

class BlockInventoryComponent(BlockComponent):
    """Represents the inventory of a block in the world. Used with blocks like chests."""

    @property
    def container(self):
        # type: () -> Container
        """The container."""
    
    