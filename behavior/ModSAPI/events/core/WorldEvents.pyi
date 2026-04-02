# coding=utf-8
from ...modules.server.Entity import *
from ...modules.server.Player import *
from ...interfaces.Sources import *


class ExplosionAfterEvent(object):
    """
    Contains information regarding an explosion that has happened.
    """
    
    @property
    def source(self):
        # type: () -> Entity
        """
        Optional source of the explosion.
        """
    
    @property
    def dimension(self):
        # type: () -> Dimension
        """Dimension where the explosion has occurred."""
    
    def getImpactedBlocks(self):
        # type: () -> list[Block]
        """A collection of blocks impacted by this explosion event."""

class ScriptEventCommandMessageAfterEvent(object):
    """
    Returns additional data about a /scriptevent command invocation.
    """
    

class ExplosionBeforeEvent(object):
    """
    Contains information regarding an explosion that has happened.
    """
    
    @property
    def source(self):
        # type: () -> Entity
        """
        Optional source of the explosion.
        """
    
    @property
    def dimension(self):
        # type: () -> Dimension
        """Dimension where the explosion has occurred."""
    
    def getImpactedBlocks(self):
        # type: () -> list[Block]
        """A collection of blocks impacted by this explosion event."""

    