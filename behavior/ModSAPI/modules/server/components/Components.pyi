# -*- coding: utf-8 -*-

class Component(object):
    """
    Base class for downstream Component implementations.
    """

    @property
    def typeId(self):
        # type: () -> str
        """
        Identifier of the dimension.
        """
        return self.__componentId

