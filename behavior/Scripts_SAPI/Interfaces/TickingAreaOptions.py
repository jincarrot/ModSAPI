# -*- coding: utf-8 -*-
# from typing import List, Dict, Union


class TickingAreaOptions(object):
    """
    Contains additional options for how an animation is played.    
    """

    def __init__(self, data):
        # type: (dict[str, str]) -> None
        from ..Classes.Dimension import Dimension
        from Vector import Vector3
        self.dimension = data['dimension'] # type: Dimension
        self._from = data['from'] # type: Vector3
        self.to = data['to'] # type: Vector3
        self._from = Vector3(self._from) if type(self._from) == dict else self._from
        self.to = Vector3(self.to) if type(self.to) == dict else self.to
