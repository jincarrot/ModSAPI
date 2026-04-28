# coding=utf-8
from ..Classes.Entity import *
from ..Interfaces.Sources import *


class ProjectileHitBlockAfterEvent(object):
    """
    Contains information related to a projectile hitting a block.
    """

    def __init__(self, data):
        self.__data = data
        self.__dimension = Dimension(SComp.CreateDimension(data['id']).GetEntityDimensionId())
        dir = serverApi.GetDirFromRot(SComp.CreateRot(data['id']).GetRot())
        self.__hitVector = Vector3({"x": dir[0], "y": dir[1], "z": dir[2]})
        self.__location = Vector3({"x": data['x'], "y": data['y'], "z": data['z']})
        self.__projectile = createEntity(data['id'])
        self.__source = createEntity(data['srcId']) if data['srcId'] else None
        self.__blockHit = None

    def __str__(self):
        data = {
            "dimension": str(self.__dimension),
            "location": str(self.__location),
            "projectile": str(self.__projectile)
        }
        return "<ProjectileHitBlockAfterEvent> %s" % data

    @property
    def dimension(self):
        # type: () -> Dimension
        """
        Dimension where this projectile hit took place.
        """
        return self.__dimension
    
    @property
    def hitVector(self):
        # type: () -> Vector3
        """
        Direction vector of the projectile as it hit a block.
        """
        return self.__hitVector

    @property
    def location(self):
        # type: () -> Vector3
        """
        Location where the projectile hit occurred.
        """
        return self.__location
    
    @property
    def projectile(self):
        # type: () -> Entity
        """
        Entity for the projectile that hit a block.
        """
        return self.__projectile
    
    @property
    def source(self):
        # type: () -> Entity | None
        """
        Optional source entity that fired the projectile.
        """
        return self.__source
    
    def getBlockHit(self):
        # type: () -> BlockHitInformation
        """
        Contains additional information about the block that was hit by the projectile.
        """
        if not self.__blockHit:
            loc = Vector3({"x": self.__data['blockPosX'], "y": self.__data['blockPosY'], "z": self.__data['blockPosZ']})
            data = {
                "block": {
                    "dimension": self.__dimension,
                    "location": loc
                },
                "face": self.__data['hitFace'],
                "faceLocation": self.location - loc
            }
            self.__blockHit = BlockHitInformation(data)
        return self.__blockHit

class ProjectileHitEntityAfterEvent(object):
    """
    Contains information related to a projectile hitting an entity.
    """

    def __init__(self, data):
        self.__data = data
        self.__dimension = Dimension(SComp.CreateDimension(data['id']).GetEntityDimensionId())
        dir = serverApi.GetDirFromRot(SComp.CreateRot(data['id']).GetRot())
        self.__hitVector = Vector3({"x": dir[0], "y": dir[1], "z": dir[2]})
        self.__location = Vector3({"x": data['x'], "y": data['y'], "z": data['z']})
        self.__projectile = createEntity(data['id'])
        self.__source = createEntity(data['srcId']) if data['srcId'] else None
        self.__entityHit = None

    def __str__(self):
        data = {
            "dimension": str(self.__dimension),
            "location": str(self.__location),
            "projectile": str(self.__projectile)
        }
        return "<ProjectileHitEntityAfterEvent> %s" % data

    @property
    def dimension(self):
        # type: () -> Dimension
        """
        Dimension where this projectile hit took place.
        """
        return self.__dimension
    
    @property
    def hitVector(self):
        # type: () -> Vector3
        """
        Direction vector of the projectile as it hit a block.
        """
        return self.__hitVector

    @property
    def location(self):
        # type: () -> Vector3
        """
        Location where the projectile hit occurred.
        """
        return self.__location
    
    @property
    def projectile(self):
        # type: () -> Entity
        """
        Entity for the projectile that hit a block.
        """
        return self.__projectile
    
    @property
    def source(self):
        # type: () -> Entity | None
        """
        Optional source entity that fired the projectile.
        """
        return self.__source
    
    def getEntityHit(self):
        # type: () -> EntityHitInformation
        """
        Contains additional information about an entity that was hit.
        """
        if not self.__entityHit:
            data = {"entity": self.__data['targetId']}
            self.__entityHit = EntityHitInformation(data)
        return self.__entityHit
