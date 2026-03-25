# -*- coding: utf-8 -*-

class BlockBoundingBox:

    def __init__(self, data):
        # type: (dict[str, str]) -> None
        from Vector import Vector3
        self.max = data['max'] # type: Vector3
        self.min = data['min'] # type: Vector3