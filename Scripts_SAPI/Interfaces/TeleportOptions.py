# -*- coding: utf-8 -*-
# from typing import List, Dict, Union


from ..Classes.Dimension import Dimension
from ..Interfaces.Vector import *


class TeleportOptions(object):
    """
    Returns the first intersecting block from the direction that this entity is looking at.
    """

    def __init__(self, data):
        self.checkForBlocks = data['checkForBlocks'] if 'checkForBlocks' in data else False
        """Whether to check whether blocks will block the entity after teleport."""
        self.dimension = data['dimension'] if 'dimension' in data else Dimension(0)
        """Dimension to potentially move the entity to. If not specified, the entity is teleported within the dimension that they reside."""
        self.facingLocation = data['facingLocation'] if 'facingLocation' in data else Vector3({})
        """Location that the entity should be facing after teleport."""
        self.keepVelocity = data['keepVelocity'] if 'keepVelocity' in data else False
        """Whether to retain the entities velocity after teleport."""
        self.rotation = data['rotation'] if 'rotation' in data else Vector2({})
        """Rotation of the entity after teleport."""
