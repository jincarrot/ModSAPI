# coding=utf-8
from ...Entity import *
from ...Player import *
from .....interfaces.Sources import *

class BlockEvent(object):
    """Contains information regarding an event that impacts a specific block."""

    @property
    def block(self):
        # type: () -> Block
        """Block currently in the world at the location of this event."""
    
    @property
    def dimension(self):
        # type: () -> Dimension
        """Dimension that contains the block that is the subject of this event."""


class BlockExplodeAfterEvent(BlockEvent):
    """
    Contains information related to a projectile hitting a block.
    """

    @property
    def source(self):
        # type: () -> Entity
        """
        Optional source of the explosion.
        """
    
    @property
    def explodedBlockPermutation(self):
        # type: () -> BlockPermutation
        """Description of the block that has exploded."""
    
class PlayerBreakBlockAfterEvent(BlockEvent):
    """
    Contains information regarding an event after a player breaks a block.
    """

    @property
    def player(self):
        # type: () -> Player
        """
        Player that broke the block for this event.
        """
    
class PlayerPlaceBlockAfterEvent(BlockEvent):
    """
    Contains information regarding an event where a player places a block.
    """

    @property
    def player(self):
        # type: () -> Player
        """
        Player that broke the block for this event.
        """
    
 
class PlayerBreakBlockBeforeEvent(BlockEvent):
    """
    Contains information regarding an event before a player breaks a block.
    """

    @property
    def player(self):
        # type: () -> Player
        """
        Player that broke the block for this event.
        """
    
    @property
    def brokenBlockPermutation(self):
        """Returns permutation information about this block before it was broken."""
    
    @property
    def itemStackBeforeBreak(self):
        """The item stack that was used to break the block before the block was broken, or undefined if empty hand."""
    
    @property
    def cancel(self):
        pass
    
    @cancel.setter
    def cancel(self, value):
        # type: (bool) -> None
        pass
    