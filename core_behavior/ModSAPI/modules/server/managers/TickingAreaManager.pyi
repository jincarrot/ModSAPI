# -*- coding: utf-8 -*-
from ....interfaces.Vector import Vector3
from ....interfaces.TickingAreaOptions import *
from ....interfaces.TickingArea import *
from ....interfaces.BlockBoundingBox import *

class TickingAreaManager:
    """
    This manager is used to add, remove or query temporary ticking areas to a dimension. 
    These ticking areas are limited by a fixed amount of ticking chunks per pack independent of the command limits. 
    Cannot modify or query ticking areas added by other packs or commands.

    Tips: Every ticking area will be removed when game closed.
    """
    @property
    def chunkCount(self) -> int:
        """The number of currently ticking chunks in this manager."""
    
    @property
    def maxChunkCount(self) -> int:
        """The maximum number of allowed ticking chunks. Overlapping ticking area chunks do count towards total."""
    
    def hasCapacity(self, options: dict) -> bool:
        """
        Returns true if the manager has enough chunk capacity for the ticking area and false otherwise. 
        Will also return false if the length or width exceeds the 255 chunk limit.

        Always returns true because ModSDK has no limit.
        """
    
    def createTickingArea(self, identifier, options):
        # type: (str, TickingAreaOptions | dict) -> None
        """
        Creates a ticking area. Promise will return when all the chunks in the area are loaded and ticking.
        """
    
    def getAllTickingAreas(self):
        # type: () -> list[TickingArea]
        """Gets all ticking areas added by this manager."""
    
    def getTickingArea(self, identifier):
        # type: (str) -> TickingArea
        """Tries to get specific ticking area by identifier."""
    
    def hasTickingArea(self, identifier):
        # type: (str) -> bool
        """Returns true if the identifier is already in the manager and false otherwise."""
    
    def removeTickingArea(self, identifier):
        # type: (str) -> None
        """Removes specific ticking area by unique identifier."""

    def removeAllTickingAreas(self):
        """Removes all ticking areas added by this manager."""
