# -*- coding: utf-8 -*-
# from typing import Union, Dict

class Component(object):
    """
    Base class for downstream Component implementations.
    """

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
    
    @property
    def isValid(self):
        # type: () -> bool
        """
        Returns whether the component is valid. 
        A component is considered valid if its owner is valid, in addition to any additional validation required by the component.
        """
        return True
