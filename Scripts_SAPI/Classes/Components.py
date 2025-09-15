# -*- coding: utf-8 -*-
# from typing import Union, Dict

class Component(object):
    """
    Base class for downstream Component implementations.
    """
    __componentId = ""

    def __init__(self, __data):
        # type: (str, dict) -> None
        pass

    def __str__(self):
        return "<Component> %s" % self.__componentId

    @property
    def typeId(self):
        # type: () -> str
        """
        Identifier of the dimension.
        """
        return self.__componentId


class EntityComponentGenerater(object):
    """
    实体组件加载器
    """
    import EntityComponents as ec
    import Entity as e

    def __init__(self, entity, componentId):
        # type: (e.Entity, str) -> None
        self.__entity = entity
        self.__componentId = componentId

    def get(self):
        # type: () -> ec.EntityComponent
        if self.__componentId == 'health':
            return self.ec.EntityHealthComponent({"entity": self.__entity})
        elif self.__componentId == 'inventory':
            return self.ec.EntityInventoryComponent({"entity": self.__entity})
