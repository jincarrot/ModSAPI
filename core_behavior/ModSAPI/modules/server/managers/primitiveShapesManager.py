# -*- coding: utf-8 -*-
# from typing import Union, Dict
import mod.server.extraServerApi as serverApi

SComp = serverApi.GetEngineCompFactory()

class PrimitiveShapesManager(object):
    """
    Primitive Shapes class used to allow adding and removing text primitives to the world.
    """
    
    def __init__(self):
        pass

    @property
    def maxShapes(self):
        """This is the maximum number of allowed primitive shapes."""
        return 300000

