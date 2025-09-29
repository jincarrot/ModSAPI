# -*- coding: utf-8 -*-
# from typing import List, Dict, Union

import mod.server.extraServerApi as serverApi

comp = serverApi.GetEngineCompFactory()


class Vector3(object):

    def __init__(self, data):
        # type: (dict | tuple) -> None
        """
        Contains a description of a vector.
        """
        if type(data) == dict:
            self.x = data['x'] if 'x' in data else 0 # type: float
            self.y = data['y'] if 'y' in data else 0 # type: float
            self.z = data['z'] if 'z' in data else 0 # type: float
        elif type(data) == tuple:
            self.x = data[0]
            self.y = data[1]
            self.z = data[2]

    def __str__(self):
        data = {
            "x": self.x,
            "y": self.y,
            "z": self.z
        }
        return "<Vector3> %s" % data
    
    def __eq__(self, data):
        # type: (Vector3 | dict) -> bool
        if type(data) == dict:
            data = Vector3(data)
        return data.x == self.x and data.y == self.y and data.z == self.z

    def __sub__(self, data):
        # type: (Vector3 | dict | tuple) -> Vector3
        if type(data) != Vector3:
            data = Vector3(data)
        data = {
            "x": self.x - data.x,
            "y": self.y - data.y,
            "z": self.z - data.z
        }
        return Vector3(data)
    
    def __add__(self, data):
        # type: (Vector3 | dict | tuple) -> Vector3
        if type(data) != Vector3:
            data = Vector3(data)
        data = {
            "x": self.x + data.x,
            "y": self.y + data.y,
            "z": self.z + data.z
        }
        return Vector3(data)
    
    def getData(self):
        # type: () -> dict
        """获取字典数据"""
        return {"x": self.x, "y": self.y, "z": self.z}
    
    def getTuple(self):
        return (self.x, self.y, self.z)


class Vector2(object):
    """
    Represents a two-directional vector.
    """

    def __init__(self, data):
        # type: (dict | tuple) -> None
        if type(data) == dict:
            self.x = data['x'] if 'x' in data else 0
            self.y = data['y'] if 'y' in data else 0
        else:
            self.x = data[0]
            self.y = data[1]

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
