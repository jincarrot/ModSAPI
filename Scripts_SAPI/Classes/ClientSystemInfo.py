# -*- coding: utf-8 -*-
# from typing import Any, List, Union, Dict

class ClientSystemInfo(object):
    """
    Contains the device information for a client instance.
    """

    def __init__(self, data):
        self.__maxRenderDistance = data['maxRenderDistance']
        self.__platformType = data['platformType']
        self.__platformType = "Desktop" if not self.__platformType else ("Mobile" if not (self.__platformType % 2) else "Console")

    @property
    def maxRenderDistance(self):
        # type: () -> int
        """
        The max render distance for the device in chunks.
        """
        return self.__maxRenderDistance
    
    @property
    def platformType(self):
        # type: () -> str
        """
        The platform type of the device.
        """
        return self.__platformType