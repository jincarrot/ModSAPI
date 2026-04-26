# -*- coding: utf-8 -*-
from ..modules.server.Entity import *

import mod.server.extraServerApi as serverApi

comp = serverApi.GetEngineCompFactory()


class EntityDamageSource(object):
    """
    Provides information about how damage has been applied to an entity.
    """

    @property
    def cause(self):
        # type: () -> str
        """
        Cause enumeration of damage.
        """

    @cause.setter
    def cause(self, data):
        pass

    @property
    def damagingEntity(self):
        # type: () -> Entity
        """
        Optional entity that caused the damage.
        """

    @damagingEntity.setter
    def damagingEntity(self, data):
        pass

    @property
    def damagingProjectile(self):
        # type: () -> Entity
        """
        Optional projectile that may have caused damage.
        """

    @damagingProjectile.setter
    def damagingProjectile(self, data):
        pass

    @property
    def customTag(self):
        # type: () -> str
        """
        Custom damage tag.
        """
    
    @customTag.setter
    def customTag(self, data):
        # type: (str) -> None
        pass

class BlockHitInformation(object):
    """
    Contains more information for events where a block is hit.
    """

    def __init__(self, data):
        self.block = Block(data['block']) # type: Block
        """Block that was hit."""
        self.face = ""# type: str
        """Face of the block that was hit."""
        self.faceLocation = data['faceLocation'] # type: Vector3
        """Location relative to the bottom north-west corner of the block."""

class EntityHitInformation(object):
    """
    Contains additional information about an entity that was hit.
    """

    def __init__(self, data):
        self.entity = createEntity(data['entity']) # type: Entity
