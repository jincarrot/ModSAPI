# -*- coding: utf-8 -*-
# from typing import List, Dict, Union

import mod.server.extraServerApi as serverApi

comp = serverApi.GetEngineCompFactory()


class Vector3(object):

    def __init__(self, data):
        # type: (dict) -> None
        """
        Contains a description of a vector.
        """
        self.x = data['x'] if 'x' in data else 0
        self.y = data['y'] if 'y' in data else 0
        self.z = data['z'] if 'z' in data else 0

    def __str__(self):
        data = {
            "x": self.x,
            "y": self.y,
            "z": self.z
        }
        return "<Vector3> %s" % data
    
    def __sub__(self, data):
        data = {
            "x": self.x - data.x,
            "y": self.y - data.y,
            "z": self.z - data.z
        }
        return Vector3(data)


class Vector2(object):
    """
    Represents a two-directional vector.
    """

    def __init__(self, data):
        self.x = data['x'] if 'x' in data else 0
        self.y = data['y'] if 'y' in data else 0

    def __str__(self):
        data = {
            "x": self.x,
            "y": self.y
        }
        return "<Vector2> %s" % data


class VectorXZ(object):
    """
    Contains a description of a vector in xz.
    """

    def __init__(self, data):
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

    def __init__(self, type, id):
        self.__motionId = id
        self.__type = type
    
    @property
    def type(self):
        return self.__type
    
    @property
    def id(self):
        return self.__motionId
