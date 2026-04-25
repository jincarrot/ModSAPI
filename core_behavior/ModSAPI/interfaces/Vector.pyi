# -*- coding: utf-8 -*-
from typing import TypedDict

import mod.server.extraServerApi as serverApi
from ..modules.server.Dimension import Dimension

comp = serverApi.GetEngineCompFactory()


class Vector3:

    x: float
    y: float
    z: float

    def __eq__(self, data):
        # type: (Vector3) -> bool
        pass

    def __sub__(self, data):
        # type: (Vector3 | tuple) -> Vector3
        pass
    
    def __add__(self, data):
        # type: (Vector3 | tuple) -> Vector3
        pass
    
    def getData(self):
        # type: () -> dict
        """获取字典数据"""
        pass
    
    def rotateY(self, angle) -> Vector3: ...

    def getTuple(self) -> tuple[float, float, float]:
        return (self.x, self.y, self.z)
    
    def getIntTuple(self) -> tuple[int, int, int]:
        """"""

class Vector2(TypedDict):
    """
    Represents a two-directional vector.
    """

    x: float
    y: float

    def __str__(self):
        data = {
            "x": self.x,
            "y": self.y
        }
        return "<Vector2> %s" % data


class VectorXZ(TypedDict):
    """
    Contains a description of a vector in xz.
    """

    x: float
    z: float

    def __str__(self):
        return "<VectorXZ> %s" % {"x": self.x, "z": self.z}
        self.x = data['x'] if 'x' in data else 0.0
        self.z = data['z'] if 'z' in data else 0.0

    def __str__(self):
        data = {
            "x": self.x,
            "z": self.z
        }
        return "<VectorXZ> %s" % data


class Motion(object):
    """
    运动器
    """
    
    @property
    def type(self):
        return self.__type
    
    @property
    def id(self):
        return self.__motionId

class DimensionLocation(TypedDict):
    """An exact coordinate within the world, including its dimension and location."""

    dimension: Dimension
    
    @dimension.setter
    def dimension(self, value):
        # type: (Dimension) -> None
        self.__dimension = value

    @property
    def x(self):
        return self.__location.x

    @x.setter
    def x(self, value):
        self.__location.x = value
    
    @property
    def y(self):
        return self.__location.y
    
    @y.setter
    def y(self, value):
        self.__location.y = value
    
    @property
    def z(self):
        return self.__location.z

    @z.setter
    def z(self, value):
        self.__location.z = value
