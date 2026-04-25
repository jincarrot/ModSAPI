# -*- coding: utf-8 -*-
# from typing import Union, Dict

class Component(object):
    """
    Base class for downstream Component implementations.
    """

    def __init__(self, data):
        # type: (str, dict) -> None
        self.__typeId = data.get("typeId", "")

    def __str__(self):
        return "<Component> %s" % self.__typeId

    @property
    def typeId(self):
        # type: () -> str
        """
        Identifier of the component.
        """
        return self.__typeId
    
    @property
    def isValid(self):
        # type: () -> bool
        """
        Returns whether the component is valid. 
        A component is considered valid if its owner is valid, in addition to any additional validation required by the component.
        """
        return True
    
class EntityComponent(Component):
    """
    Base class for downstream entity components.
    """
    
    def __init__(self, data):
        Component.__init__(self, data)
        self.__entity = data['entity']
    
    def __str__(self):
        data = {
            "entity": str(self.__entity)
        }
        return "<EntityComponent> %s" % data
    
    @property
    def entity(self):
        """
        The entity that owns this component. 
        The entity will be undefined if it has been removed.
        """
        return self.__entity
    
class ConstMeta(type):
    def __setattr__(cls, name, value):
        if name == "componentId":
            raise AttributeError("Constant '{0}' cannot be reassigned".format(name))
        super(ConstMeta, cls).__setattr__(name, value)

