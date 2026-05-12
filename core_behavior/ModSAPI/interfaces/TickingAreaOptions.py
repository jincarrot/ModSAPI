# -*- coding: utf-8 -*-
# from typing import List, Dict, Union


class TickingAreaOptions(object):
    """
    Contains additional options for how an animation is played.    
    """

    def __init__(self, data):
        # type: (dict[str, str]) -> None
        from ..modules.server.Dimension import Dimension
        from Vector import Vector3
        self.dimension = data['dimension'] # type: Dimension
        self._from = data['from'] # type: Vector3
        self.to = data['to'] # type: Vector3
        self._from = Vector3(self._from)
        self.to = Vector3(self.to)
