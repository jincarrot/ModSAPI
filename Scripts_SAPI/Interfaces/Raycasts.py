# -*- coding: utf-8 -*-

from ..Classes.Block import *

class EntityRaycastHit(object):
    """
    Contains information for entity raycast hit results.
    """

    def __init__(self, data):
        self.distance = data['distance']
        """Distance from ray origin to entity bounds."""
        self.entity = data['entity']
        """Entity that was hit."""

    def __str__(self):
        data = {
            "distance": self.distance,
            "entity": str(self.entity)
        }
        return "<EntityRaycastHit> %s" % data
    

class BlockRaycastHit(object):
    """
    Contains information for block raycast hit results.
    """

    def __init__(self, data):
        self.__block = data['block']
        """Block that was hit."""
        self.__face = data['face']
        """Face of the block that was hit."""
        self.__faceLocation = data['faceLocation']
        """Hit location relative to the bottom north-west corner of the block."""
    
    def __str__(self):
        data = {
            "block": str(self.block),
            "face": str(self.face),
            "faceLocation": str(self.faceLocation)
        }
        return "<BlockRaycastHit> %s" % data

    @property
    def block(self):
        # type: () -> Block
        """Block that was hit."""
        return self.__block
    
    @property
    def face(self):
        # type: () -> Direction
        """Face of the block that was hit."""
        return self.__face

    @property
    def faceLocation(self):
        # type: () -> Vector3
        """Hit location relative to the bottom north-west corner of the block."""
        return self.__faceLocation
