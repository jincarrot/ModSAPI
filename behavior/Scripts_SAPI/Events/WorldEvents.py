# coding=utf-8
from ..Classes.Entity import *
from ..Interfaces.Sources import *


class ExplosionAfterEvent(object):
    """
    Contains information regarding an explosion that has happened.
    """

    def __init__(self, data):
        self.__source = createEntity(data['sourceId']) if data['sourceId'] else None
        self.__dimension = Dimension(data['dimensionId'])
        self.__data = data

    def __str__(self):
        data = {
            "source": self.__source
        }
        return "<ExplosionAfterEvent> %s" % data
    
    @property
    def source(self):
        # type: () -> Entity
        """
        Optional source of the explosion.
        """
        return self.__source
    
    @property
    def dimension(self):
        # type: () -> Dimension
        """Dimension where the explosion has occurred."""
        return self.__dimension
    
    def getImpactedBlocks(self):
        # type: () -> list[Block]
        """A collection of blocks impacted by this explosion event."""
        lst = []
        for block in self.__data:
            lst.append(Block({"dimension": self.__dimension, "location": Vector3(block)}))
        return lst

class ScriptEventCommandMessageAfterEvent(object):
    """
    Returns additional data about a /scriptevent command invocation.
    """

    def __init__(self, data):
        self.__id = None

    def __str__(self):
        data = {
            "id": self.__id
        }
        return "<ScriptEventCommandMessageAfterEvent> %s" % data
    