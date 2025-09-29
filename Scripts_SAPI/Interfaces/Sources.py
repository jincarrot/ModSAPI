# -*- coding: utf-8 -*-
from ..Classes.Entity import *

import mod.server.extraServerApi as serverApi

comp = serverApi.GetEngineCompFactory()


class EntityDamageSource(object):
    """
    Provides information about how damage has been applied to an entity.
    """

    def __init__(self, data):
        # type: (dict) -> None
        self.__cause = data['cause']
        self.__customTag = data['customTag'] if 'customTag' in data else ''
        self.__damagingEntity = data['damagingEntity'] if 'damagingEntity' in data else None
        self.__damagingProjectile = data['damagingProjectile'] if 'damagingProjectile' in data else None

    def __str__(self):
        data = {
            "cause": self.cause,
            "custom_tag": self.__customTag,
            "damagingEntity": str(self.damagingEntity),
            "damagingProjectile": str(self.damagingProjectile)
        }
        return "<EntityDamageSource> %s" % data

    @property
    def cause(self):
        # type: () -> str
        """
        Cause enumeration of damage.
        """
        return self.__cause

    @cause.setter
    def cause(self, data):
        self.__cause = data

    @property
    def damagingEntity(self):
        # type: () -> Entity
        """
        Optional entity that caused the damage.
        """
        return self.__damagingEntity

    @damagingEntity.setter
    def damagingEntity(self, data):
        self.__damagingEntity = data

    @property
    def damagingProjectile(self):
        # type: () -> Entity
        """
        Optional projectile that may have caused damage.
        """
        return self.__damagingProjectile

    @damagingProjectile.setter
    def damagingProjectile(self, data):
        self.__damagingProjectile = data

    @property
    def customTag(self):
        # type: () -> str
        """
        Custom damage tag.
        """
        return self.__customTag
    
    @customTag.setter
    def customTag(self, data):
        # type: (str) -> None
        self.__customTag = data

class BlockHitInformation(object):
    """
    Contains more information for events where a block is hit.
    """

    def __init__(self, data):
        self.block = Block(data['block']) # type: Block
        """Block that was hit."""
        self.face = Direction_ModSDK[data['face']] # type: str
        """Face of the block that was hit."""
        self.faceLocation = data['faceLocation'] # type: Vector3
        """Location relative to the bottom north-west corner of the block."""

class EntityHitInformation(object):
    """
    Contains additional information about an entity that was hit.
    """

    def __init__(self, data):
        self.entity = createEntity(data['entity']) # type: Entity
