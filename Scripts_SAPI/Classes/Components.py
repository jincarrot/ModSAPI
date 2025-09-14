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


class EntityComponent(Component):
    """
    Base class for downstream entity components.
    """
    __componentId = ""
    import Entity as en
    
    def __init__(self, data):
        Component.__init__(self, data)
        self.__entity = data['entity']
    
    def __str__(self):
        data = {
            "typeId": self.__componentId,
            "entity": str(self.__entity)
        }
        return "<EntityComponent> %s" % data
    
    @property
    def entity(self):
        # type: () -> en.Entity
        """
        The entity that owns this component. 
        The entity will be undefined if it has been removed.
        """
        return self.__entity

    def asHealthComponent(self): 
        import EntityComponents as ec
        return ec.EntityHealthComponent({"entity": self.__entity})


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
        import BlockComponents as bc
        return bc.BlockInventoryComponent({"block": self.__block})


class ItemComponent(Component):
    """Base type for components associated with blocks."""
    __componentId = ""
    import ItemStack as i

    def __init__(self, data):
        Component.__init__(self, data)
        self.__item = data['item']
    
    @property
    def item(self):
        # type: () -> i.ItemStack
        """Item instance that this component pertains to."""
        return self.__item


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
