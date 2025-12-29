import types
import mod.server.extraServerApi as serverApi
import mod.client.extraClientApi as clientApi

from ..Interfaces.Vector import Vector3
from ..Interfaces.TickingAreaOptions import *
from ..Interfaces.TickingArea import *
from ..Interfaces.BlockBoundingBox import *

SComp = serverApi.GetEngineCompFactory()

def hasArg(callback):
        # type: (types.FunctionType) -> bool
        args = callback.func_code.co_argcount
        if hasattr(callback, "im_self"):
            args -= 1
        return args > 0

class Promise(object):
    """Promise"""

    def __init__(self):
        def default(arg):
            # type: (TickingArea) -> None
            pass
        self.callback = default

    def then(self, callback):
        self.callback = callback

class TickingAreaManager:
    """
    This manager is used to add, remove or query temporary ticking areas to a dimension. 
    These ticking areas are limited by a fixed amount of ticking chunks per pack independent of the command limits. 
    Cannot modify or query ticking areas added by other packs or commands.

    Tips: Every ticking area will be removed when game closed.
    """

    def __init__(self):
        self.__chunkCount = 0
        self.__tickingAreas = {}

    @property
    def chunkCount(self):
        """The number of currently ticking chunks in this manager."""
        return self.__chunkCount
    
    @property
    def maxChunkCount(self):
        """The maximum number of allowed ticking chunks. Overlapping ticking area chunks do count towards total."""
        return 300
    
    def hasCapacity(self, options):
        """
        Returns true if the manager has enough chunk capacity for the ticking area and false otherwise. 
        Will also return false if the length or width exceeds the 255 chunk limit.
        """
        return self.maxChunkCount > self.chunkCount
    
    def createTickingArea(self, identifier, options):
        # type: (str, TickingAreaOptions | dict) -> None
        """
        Creates a ticking area. Promise will return when all the chunks in the area are loaded and ticking.
        """
        if type(options) == dict:
            options = TickingAreaOptions(options)
        comp = SComp.CreateChunkSource(serverApi.GetLevelId())
        comp.SetAddArea(identifier, options.dimension.dimId, options._from.getTuple(), options.to.getTuple())
        scale = options._from - options.to
        xAmount = int(scale.x) % 16 + 1
        zAmount = int(scale.z) % 16 + 1
        chunkCount = xAmount * zAmount
        self.__chunkCount += chunkCount
        promise = Promise()
        def finishLoad():
            if hasArg(promise.callback):
                promise.callback(tickingArea)
            else:
                promise.callback()
        minCorner = (
            min(options._from.getTuple()[0], options.to.getTuple()[0]), 
            min(options._from.getTuple()[1], options.to.getTuple()[1]), 
            min(options._from.getTuple()[2], options.to.getTuple()[2])
        )
        maxCorner = (
            max(options._from.getTuple()[0], options.to.getTuple()[0]), 
            max(options._from.getTuple()[1], options.to.getTuple()[1]), 
            max(options._from.getTuple()[2], options.to.getTuple()[2])
        )
        tickingArea = TickingArea(
            {
                "dimension": options.dimension, 
                "identifier": identifier, 
                "boundingBox": BlockBoundingBox(
                    {
                        "max": Vector3(maxCorner), 
                        "min": Vector3(minCorner)
                    }
                ),
                "chunkCount": chunkCount
            }
        )
        comp.DoTaskOnChunkAsync(options.dimension.dimId, minCorner, maxCorner, finishLoad)
        self.__tickingAreas[identifier] = tickingArea
        return promise
    
    def getAllTickingAreas(self):
        # type: () -> list[TickingArea]
        """Gets all ticking areas added by this manager."""
        comp = SComp.CreateChunkSource(serverApi.GetLevelId())
        areaKeys = comp.GetAllAreaKeys()
        areas = []
        for key in areaKeys:
            areas.append(self.__tickingAreas.get(key, None))
        return areas
    
    def getTickingArea(self, identifier):
        # type: (str) -> TickingArea
        """Tries to get specific ticking area by identifier."""
        return self.__tickingAreas.get(identifier, None)
    
    def hasTickingArea(self, identifier):
        # type: (str) -> bool
        """Returns true if the identifier is already in the manager and false otherwise."""
        return identifier in self.__tickingAreas.keys()
    
    def removeTickingArea(self, identifier):
        # type: (str) -> None
        """Removes specific ticking area by unique identifier."""
        comp = SComp.CreateChunkSource(serverApi.GetLevelId())
        comp.DeleteArea(identifier)

    def removeAllTickingAreas(self):
        """Removes all ticking areas added by this manager."""
        comp = SComp.CreateChunkSource(serverApi.GetLevelId())
        comp.DeleteAllArea()
