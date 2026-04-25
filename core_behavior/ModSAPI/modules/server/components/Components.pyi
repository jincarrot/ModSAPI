# -*- coding: utf-8 -*-

class Component(object):
    """
    Base class for downstream Component implementations.
    """

    @property
    def typeId(self):
        # type: () -> str
        """
        Identifier of the component.
        """
    
    @property
    def isValid(self) -> bool:
        """
        Returns whether the component is valid. 
        A component is considered valid if its owner is valid, in addition to any additional validation required by the component.
        """

from ..Entity import Entity

class EntityComponent(Component):
    """
    Base class for downstream entity components.
    """
    
    @property
    def entity(self) -> Entity:
        """
        The entity that owns this component. 
        The entity will be undefined if it has been removed.
        """