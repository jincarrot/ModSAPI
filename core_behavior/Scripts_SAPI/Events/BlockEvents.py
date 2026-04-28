# coding=utf-8
from ..Classes.Entity import *
from ..Interfaces.Sources import *

class BlockEvent(object):
    """Contains information regarding an event that impacts a specific block."""

    def __init__(self, data):
        self.__block = data.get("block", None)
        self.__dimension = data.get("dimension", None)
    
    @property
    def block(self):
        # type: () -> Block
        """Block currently in the world at the location of this event."""
        return self.__block
    
    @property
    def dimension(self):
        # type: () -> Dimension
        """Dimension that contains the block that is the subject of this event."""
        return self.__dimension


class BlockExplodeAfterEvent(BlockEvent):
    """
    Contains information related to a projectile hitting a block.
    """

    def __init__(self, data):
        self.__source = createEntity(data['sourceId']) if data['sourceId'] else None
        self.__explodedBlockPermutation = BlockPermutation(Block({"dimension": Dimension(data['dimensionId']), "location": Vector3(data['explodePos'])}))

    def __str__(self):
        data = {
            "source": self.__source
        }
        return "<BlockExplodeAfterEvent> %s" % data
    
    @property
    def source(self):
        # type: () -> Entity
        """
        Optional source of the explosion.
        """
        return self.__source
    
    @property
    def explodedBlockPermutation(self):
        # type: () -> BlockPermutation
        """Description of the block that has exploded."""
        return self.__explodedBlockPermutation
    
class PlayerBreakBlockAfterEvent(BlockEvent):
    """
    Contains information regarding an event after a player breaks a block.
    """

    def __init__(self, data):
        self.__dimension = Dimension(data['dimensionId'])
        self.__block = Block({"dimension": self.__dimension, "location": Vector3((data['x'], data['y'], data['z']))})
        self.__player = Player(data['playerId'])
        BlockEvent.__init__(self, {"block": self.__block, "dimension": self.__dimension})

    def __str__(self):
        data = {
            "block": str(self.__block),
            "player": str(self.__player)
        }
        return "<PlayerBreakBlockAfterEvent> %s" % data
    
    @property
    def player(self):
        # type: () -> Player
        """
        Player that broke the block for this event.
        """
        return self.__player
    
class PlayerPlaceBlockAfterEvent(BlockEvent):
    """
    Contains information regarding an event where a player places a block.
    """

    def __init__(self, data):
        self.__dimension = Dimension(data['dimensionId'])
        self.__block = Block({"dimension": self.__dimension, "location": Vector3((data['x'], data['y'], data['z']))})
        self.__player = Player(data['entityId'])

    def __str__(self):
        data = {
            "block": str(self.__block),
            "player": str(self.__player)
        }
        return "<PlayerPlaceBlockAfterEvent> %s" % data
    
    @property
    def player(self):
        # type: () -> Player
        """
        Player that broke the block for this event.
        """
        return self.__player
    
 
class PlayerBreakBlockBeforeEvent(BlockEvent):
    """
    Contains information regarding an event before a player breaks a block.
    """

    def __init__(self, data):
        self.__data = data
        self.__dimension = Dimension(data['dimensionId'])
        self.__block = Block({"dimension": self.__dimension, "location": Vector3((data['x'], data['y'], data['z']))})
        self.__player = Player(data['playerId'])
        self.__cancel = False

    def __str__(self):
        data = {
            "block": str(self.__block),
            "player": str(self.__player)
        }
        return "<PlayerBreakBlockAfterEvent> %s" % data
    
    @property
    def player(self):
        # type: () -> Player
        """
        Player that broke the block for this event.
        """
        return self.__player
    
    @property
    def brokenBlockPermutation(self):
        """Returns permutation information about this block before it was broken."""
        return self.__brokenBlockPermutation
    
    @property
    def itemStackBeforeBreak(self):
        """The item stack that was used to break the block before the block was broken, or undefined if empty hand."""
        return self
    
    @property
    def cancel(self):
        return self.__cancel
    
    @cancel.setter
    def cancel(self, value):
        # type: (bool) -> None
        self.__cancel = value
        self.__data['cancel'] = value
    
    