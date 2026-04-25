# -*- coding: utf-8 -*-

import mod.server.extraServerApi as serverApi

class StructureSaveMode(object):
    """
    Specifies how a structure should be saved.
    """

    @property
    def Memory(self):
        """The structure will be temporarily saved to memory. 
        The structure will persist until the world is shut down."""
        return "Memory"
    
    @property
    def World(self):
        """The structure will be saved to the world file and persist between world loads. 
        A saved structure can be removed from the world via @minecraft/server.StructureManager.delete."""
        return "World"
