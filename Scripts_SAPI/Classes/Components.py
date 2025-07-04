# -*- coding: utf-8 -*-
# from typing import Union, Dict
from ..Classes.Entity import *

class Component(object):
    """
    Base class for downstream Component implementations.
    """

    def __init__(self, typeId, data):
        # type: (str, dict) -> None
        if typeId.find("minecraft:") < 0:
            typeId = "minecraft:" + typeId
        self.__typeId = typeId.lower()

    def __str__(self):
        return "<Component> {typeId: %s}" % self.typeId

    @property
    def typeId(self):
        # type: () -> str
        """
        Identifier of the dimension.
        """
        return self.__typeId


class EntityComponent(Component):
    """
    Base class for downstream entity components.
    """
    
    def __init__(self, typeId, data):
        Component.__init__(self, typeId, data)
        self.__entity = data['entity']
    
    def __str__(self):
        data = {
            "typeId": self.typeId,
            "entity": str(self.entity)
        }
        return "<EntityComponent> %s" % data
    
    @property
    def entity(self):
        # type: () -> Entity
        """
        The entity that owns this component. 
        The entity will be undefined if it has been removed.
        """
        return self.__entity


class ComponentGenerater(object):
    """
    组件加载器
    """
