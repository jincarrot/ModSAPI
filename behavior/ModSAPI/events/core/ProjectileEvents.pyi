# coding=utf-8
from ...modules.server.Entity import *
from ...modules.server.Player import *
from ...interfaces.Sources import *


class ProjectileHitBlockAfterEvent(object):
    """
    Contains information related to a projectile hitting a block.
    """

    @property
    def dimension(self):
        # type: () -> Dimension
        """
        Dimension where this projectile hit took place.
        """
    
    @property
    def hitVector(self):
        # type: () -> Vector3
        """
        Direction vector of the projectile as it hit a block.
        """

    @property
    def location(self):
        # type: () -> Vector3
        """
        Location where the projectile hit occurred.
        """
    
    @property
    def projectile(self):
        # type: () -> Entity
        """
        Entity for the projectile that hit a block.
        """
    
    @property
    def source(self):
        # type: () -> Entity | None
        """
        Optional source entity that fired the projectile.
        """
    
    def getBlockHit(self):
        # type: () -> BlockHitInformation
        """
        Contains additional information about the block that was hit by the projectile.
        """

class ProjectileHitEntityAfterEvent(object):
    """
    Contains information related to a projectile hitting an entity.
    """

    @property
    def dimension(self):
        # type: () -> Dimension
        """
        Dimension where this projectile hit took place.
        """
    
    @property
    def hitVector(self):
        # type: () -> Vector3
        """
        Direction vector of the projectile as it hit a block.
        """

    @property
    def location(self):
        # type: () -> Vector3
        """
        Location where the projectile hit occurred.
        """
    
    @property
    def projectile(self):
        # type: () -> Entity
        """
        Entity for the projectile that hit a block.
        """
    
    @property
    def source(self):
        # type: () -> Entity | None
        """
        Optional source entity that fired the projectile.
        """
    
    def getEntityHit(self):
        # type: () -> EntityHitInformation
        """
        Contains additional information about an entity that was hit.
        """
