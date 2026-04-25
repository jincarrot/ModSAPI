# -*- coding: utf-8 -*-
import mod.server.extraServerApi as serverApi

class TickingArea:
    """A context which provides information about a specific ticking area."""

    def __init__(self, data):
        # type: (dict[str, str]) -> None
        from ..Classes.Dimension import Dimension
        from BlockBoundingBox import BlockBoundingBox
        self.dimension = data['dimension'] # type: Dimension
        """The dimension the ticking area is located."""
        self.identifier = data['identifier'] # type: str
        """The unique identifier of the ticking area."""
        self.chunkCount = data['chunkCount'] # type: int
        """The number of chunks that the ticking area contains."""
        self.boundingBox = data['boundingBox'] # type: BlockBoundingBox
        """The box which contains all the ticking blocks in the ticking area."""

    @property
    def isFullyLoaded(self):
        """Will be true if all the ticking areas chunks are loaded in ticking and false otherwise."""
        minCorner = self.boundingBox.min
        maxCorner = self.boundingBox.max
        comp = serverApi.GetEngineCompFactory().CreateChunkSource(serverApi.GetLevelId())
        for x in range(int(minCorner.x / 16), int(maxCorner.x / 16)):
            for z in range(int(minCorner.z / 16), int(maxCorner.z / 16)):
                if not comp.IsChunkGenerated(self.dimension.dimId, (x, z)):
                    return False
        return True