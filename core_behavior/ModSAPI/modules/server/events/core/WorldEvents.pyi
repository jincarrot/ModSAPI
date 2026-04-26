# coding=utf-8
from ...Entity import *
from ...Player import *
from .....interfaces.Sources import *
from .....enums.Events import ScriptEventSource
from ...Block import Block
from ...Dimension import Dimension


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
    
    @property
    def id(self) -> str:
        # type: () -> str
        """Identifier of this ScriptEvent command message."""
    
    @property
    def message(self) -> str:
        # type: () -> str
        """Optional additional data passed in with the script event command."""
    
    @property
    def initiator(self) -> Entity | None:
        """If this command was initiated via an NPC, returns the entity that initiated the NPC dialogue."""
    
    @property
    def sourceEntity(self) -> Entity | None:
        """Source entity if this command was triggered by an entity (e.g., a NPC)."""
    
    @property
    def sourceBlock(self) -> Block | None:
        """Source block if this command was triggered via a block (e.g., a commandblock.)"""
        return self.__source
    
    @property
    def sourceType(self) -> ScriptEventSource:
        """Returns the type of source that fired this command."""

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

    