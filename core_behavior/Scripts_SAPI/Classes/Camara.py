# coding = utf-8

# from typing import Union, Dict, List
from ..Interfaces.Vector import *
from ..Interfaces.CameraOptions import *
import mod.client.extraClientApi as clientApi

CComp = clientApi.GetEngineCompFactory()

class CameraPlus(object):
    """
    Note: This class is different from SAPI. It's based on Mod-api Client.

    Contains methods relating to the active camera for the specified player.
    """

    def __init__(self, playerId):
        self.__playerId = playerId
        self.__comp = CComp.CreateCamera(self.__playerId)

    @property
    def anchor(self):
        # type: () -> Vector3
        """
        获取锚点
        """
        anchor = self.__comp.GetCameraAnchor()
        return Vector3({"x": anchor[0], "y": anchor[1], "z": anchor[2]})
    
    @anchor.setter
    def anchor(self, data):
        # type: (Vector3) -> None
        self.__comp.SetCameraAnchor((data.x, data.y, data.z))
    
    @property
    def offset(self):
        # type: () -> Vector3
        """
        获取偏移量
        """
        offset = self.__comp.GetCameraOffset()
        return Vector3({"x": offset[0], "y": offset[1], "z": offset[2]})
    
    @offset.setter
    def offset(self, data):
        # type: (Vector3) -> None
        self.__comp.SetCameraOffset((data.x, data.y, data.z))
    
    @property
    def rotation(self):
        # type: () -> Vector3
        """
        获取旋转角度
        """
        rotation = self.__comp.GetCameraRotation()
        return Vector3({"x": rotation[0], "y": rotation[1], "z": rotation[2]})
    
    @rotation.setter
    def rotation(self, data):
        # type: (Vector3) -> None
        self.__comp.SetCameraRotation((data.x, data.y, data.z))

    @property
    def position(self):
        # type: () -> Vector3
        """
        获取位置
        """
        position = self.__comp.GetPosition()
        return Vector3({"x": position[0], "y": position[1], "z": position[2]})
    
    @position.setter
    def position(self, data):
        # type: (Vector3) -> None
        self.__comp.SetPosition((data.x, data.y, data.z))

    @property
    def fov(self):
         # type: () -> float
        """
        获取视野
        """
        return self.__comp.GetFov()
    
    @fov.setter
    def fov(self, data):
        # type: (float) -> None
        data = 30 if data < 30 else data
        data = 110 if data > 110 else data
        self.__comp.SetFov(data)
    
    @property
    def rangeY(self):
        # type: () -> Tuple[float]
        """
        获取范围
        """
        return self.__comp.GetCameraPitchLimit()
    
    @rangeY.setter
    def rangeY(self, data):
        # type: (Tuple[float]) -> None
        self.__comp.SetCameraPitchLimit((data[0], data[1]))
    
    def getAllMotions(self):
        # type: () -> list[Motion]
        """
        获取该摄像机上存在的所有运动器
        """
        res = []
        motions = self.__comp.GetCameraMotions()
        for id in motions:
            res.append(Motion(motions[id], id))
        return res
    

class Camera(object):
    """
    Contains methods relating to the active camera for the specified player.

    Doc: https://learn.microsoft.com/en-us/minecraft/creator/scriptapi/minecraft/server/camera?view=minecraft-bedrock-experimental
    """

    def __init__(self, playerId):
        self.playerId = playerId

    def clear(self):
        # type: () -> None
        """
        Clears the active camera for the specified player. 
        Causes the specified players to end any in-progress camera perspectives, 
        including any eased camera motions, and return to their normal perspective.
        """
        pass

    def fade(self, fadeCameraOptions=None):
        # type: (CameraFadeOptions) -> None
        """
        Begins a camera fade transition. A fade transition is a full-screen color that fades-in, holds, and then fades-out.
        """
        pass

    def setCamera(self, cameraPreset, setOptions=None):
        # type: (str, Union[CameraFixedBoomOptions]) -> None
        """
        Sets the current active camera for the specified player.
        """
        pass

    def setDefaultCamera(self, cameraPreset, easeOptions=None):
        # type: (str, EaseOptions) -> None
        """
        Sets the current active camera for the specified player and resets the position and rotation to the values defined in the JSON.
        """
        pass